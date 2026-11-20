"""Límite de peticiones con ventana fija por cliente y reloj inyectable."""

import logging
import math
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Request, Response

from wine_api.errors import RateLimitExceededError
from wine_api.schemas import ErrorResponse
from wine_api.security import ClientDep

logger = logging.getLogger("wine_api.rate_limit")

RATE_LIMIT_RESPONSES: dict[int | str, dict] = {
    429: {
        "model": ErrorResponse,
        "description": "Se ha superado la cuota de peticiones por minuto.",
        "headers": {
            "Retry-After": {
                "description": "Segundos que faltan para que la ventana se reinicie.",
                "schema": {"type": "integer"},
            }
        },
    }
}


@dataclass(frozen=True)
class RateLimitDecision:
    """Resultado de consultar el límite."""

    allowed: bool
    remaining: int
    retry_after: int | None = None


class FixedWindowRateLimiter:
    """Ventana fija de 60 segundos con cerrojo para concurrencia."""

    def __init__(
        self,
        clock: Callable[[], float] = time.time,
        window_seconds: int = 60,
    ) -> None:
        self.window_seconds = window_seconds
        self.clock = clock
        self._windows: dict[str, tuple[float, int]] = {}
        self._lock = threading.Lock()

    def hit(self, key: str, limit: int) -> RateLimitDecision:
        """Registra una petición y devuelve si pasa y cuántas quedan."""

        # TODO S10.4b: implementa la ventana fija dentro de `with self._lock:`.
        # - calcula la ventana actual: `window = int(now // self._window_seconds)`.
        # - si `self._counts[client]` tiene otra ventana, empieza de cero.
        # - si las peticiones igualan o superan `limit`, calcula los segundos
        #   hasta la siguiente ventana (`(window + 1) * 60 - now`) y devuelve
        #   `RateLimitDecision(allowed=False, retry_after=..., remaining=0)`.
        # - si hay margen, incrementa y devuelve `allowed=True`.
        # ¿Por qué este contador en memoria NO escala a varios workers?
        # Comprobación: tests/test_s10_4_rate_limit.py
        with self._lock:
            now = self.clock()
            start, count = self._windows.get(key, (now, 0))
            if now - start >= self.window_seconds:
                start, count = now, 0
            if count >= limit:
                remaining_window = self.window_seconds - (now - start)
                return RateLimitDecision(
                    allowed=False,
                    remaining=0,
                    retry_after=math.ceil(remaining_window),
                )
            self._windows[key] = (start, count + 1)
            return RateLimitDecision(
                allowed=True, remaining=limit - count - 1, retry_after=0
            )

    def usage(self, key: str) -> int:
        """Peticiones acumuladas en la ventana actual (no incrementa)."""

        with self._lock:
            start, count = self._windows.get(key, (0.0, 0))
            if self.clock() - start >= self.window_seconds:
                return 0
            return count


def get_rate_limiter(request: Request) -> FixedWindowRateLimiter:
    return request.app.state.rate_limiter


RateLimiterDep = Annotated[FixedWindowRateLimiter, Depends(get_rate_limiter)]


def enforce_rate_limit(
    client: ClientDep, limiter: RateLimiterDep, response: Response
) -> None:
    """Dependencia de FastAPI: cuenta la petición y añade cabeceras."""

    # TODO S10.4c: cuenta la petición con `limiter.hit(...)` usando el nombre
    # y la cuota del cliente autenticado.
    # - si la decisión rechaza la petición, lanza `RateLimitExceededError` con
    #   los segundos de espera y el límite.
    # - si la acepta, añade `X-RateLimit-Limit` y `X-RateLimit-Remaining` a
    #   las cabeceras de `response`.
    # Comprobación: tests/test_s10_4_rate_limit.py::test_rate_limit_per_client
    decision = limiter.hit(client.name, limit=client.rate_limit_per_minute)
    if not decision.allowed:
        logger.warning("Rate limit exceeded for client %s", client.name)
        raise RateLimitExceededError(
            retry_after=decision.retry_after or 1,
            limit=client.rate_limit_per_minute,
        )
    response.headers["X-RateLimit-Limit"] = str(client.rate_limit_per_minute)
    response.headers["X-RateLimit-Remaining"] = str(decision.remaining)
