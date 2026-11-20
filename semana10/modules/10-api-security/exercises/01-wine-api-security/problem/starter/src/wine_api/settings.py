"""Configuración validada en arranque (pydantic-settings y SecretStr)."""

from typing import Literal

from pydantic import BaseModel, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

Scope = Literal["predict", "admin"]


class ClientConfig(BaseModel):
    """Credencial, permisos y cuota de un cliente de la API."""

    # TODO S10.1a: declara los tres campos de un cliente:
    # - `key`: la API key. ¿Qué tipo de Pydantic evita que aparezca en un
    #   `repr`, en un `print` o en un log? Investiga `SecretStr` y cómo se lee
    #   su valor cuando de verdad lo necesitas.
    # - `scopes`: lista de `Scope`; un scope desconocido debe fallar al arrancar.
    # - `rate_limit_per_minute`: entero estrictamente positivo, 60 por defecto
    #   (`Field` con una restricción numérica).
    # Comprobación: tests/test_s10_1_settings.py (repr y configuración inválida).
    key: SecretStr = Field(description="API key del cliente; oculta en `repr`.")
    scopes: list[Scope] = Field(description="Operaciones que la clave autoriza.")
    rate_limit_per_minute: int = Field(
        default=60, gt=0, description="Peticiones de predicción por minuto."
    )


class Settings(BaseSettings):
    """Configuración validada al arrancar: si algo es inválido, no arranca."""

    model_config = SettingsConfigDict(
        env_prefix="WINE_API_", env_file=".env", extra="ignore"
    )

    mode: Literal["ready", "unavailable"] = "ready"

    # TODO S10.1b: añade el resto de la configuración con valores por defecto
    # SEGUROS (la API debe arrancar sin `.env`, pero sin abrir nada):
    # - `clients`: diccionario nombre -> ClientConfig, vacío por defecto. Sin
    #   clientes no hay claves válidas: es la decisión «fail closed».
    # - `cors_origins`: lista de orígenes; por defecto solo el front de
    #   Streamlit (`http://localhost:8501`).
    # - `docs_enabled`: booleano, activado por defecto.
    # Además, rechaza `"*"` en `cors_origins` con un `field_validator`: la
    # configuración debe obligar a listar los orígenes.
    # ¿Por qué un error de configuración debe impedir arrancar en lugar de
    # aparecer en la primera petición?
    # Comprobación: uv run pytest -q tests/test_s10_1_settings.py
    clients: dict[str, ClientConfig] = {}
    cors_origins: list[str] = ["http://localhost:8501"]
    docs_enabled: bool = True

    @field_validator("cors_origins")
    @classmethod
    def _reject_wildcard(cls, origins: list[str]) -> list[str]:
        if "*" in origins:
            raise ValueError("list the allowed origins explicitly; '*' is not allowed")
        return origins
