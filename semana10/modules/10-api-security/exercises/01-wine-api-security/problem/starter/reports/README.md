# S10.7 — Informe de carga

> **TODO S10.7c:** ejecuta Locust con `--csv reports/s10`, versiona los CSV
> generados y completa las tablas y el análisis de este archivo.

Plantilla del informe. Rellénala con **tus** resultados: dependen de la máquina,
del número de workers y de la configuración de `.env`. No copies cifras de otra
persona ni de la solución, que no incluye resultados.

## Cómo se ha medido

| Dato | Valor |
| --- | --- |
| Comando de la API | `uv run fastapi dev` (1 proceso) |
| Comando de Locust | `uv run --group load locust -f locustfile.py --headless -u 20 -r 5 -t 1m --host http://127.0.0.1:8000 --csv reports/s10` |
| Cliente usado | `front` |
| `rate_limit_per_minute` del cliente | 60 |
| Máquina | Windows, x86_64 |

Archivos generados por Locust y versionados junto a este informe:
`s10_stats.csv`, `s10_failures.csv` y `s10_stats_history.csv`.

## Resultados

Copia los valores de la fila `POST /v1/predictions` y de `Aggregated` de
`s10_stats.csv`.

| Endpoint | Peticiones | RPS | p50 (ms) | p95 (ms) | Fallos | % 429 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `POST /v1/predictions` | 706 | 12.06 | 9 | 27 | 652 | 89.8 % |
| `/v1/predictions [422]` | 84 | 1.43 | 10 | 1000 | 78 | — |
| `GET /health` | 80 | 1.37 | 7 | 14 | 0 | — |
| Aggregated | 870 | 14.86 | 9 | 36 | 730 | 81.5 % |

`% 429` = fallos `429` de `s10_failures.csv` / peticiones de
`POST /v1/predictions` × 100 (634 / 706 × 100 = 89.8 %).

## Análisis (5–10 líneas)

- El cliente `front` tiene un límite configurado de 60 peticiones por minuto. Locust ha solicitado 706 predicciones en ese minuto, por lo que el limitador ha dejado pasar las primeras y ha devuelto 429 en 634 de ellas. Esto representa un 89.8 % de rechazo por cuota, lo que cuadra exactamente con el comportamiento esperado.
- El endpoint `GET /health` tiene una latencia menor (p50 de 7 ms y p95 de 14 ms) en comparación con `POST /v1/predictions` (p50 de 9 ms y p95 de 27 ms), ya que no pasa por autenticación, no valida el cuerpo del JSON ni compite por el cerrojo del contador de tasa.
- Con dos workers (`fastapi run --workers 2`), cada proceso tendría su propio contador en memoria independiente. Al repartirse las peticiones entre los dos procesos, el cliente podría llegar a enviar el doble de peticiones (unas 120 por minuto) antes de ser bloqueado. Para varios workers en producción se necesitaría un almacén compartido como Redis.
- Para medir la capacidad real del servicio y no el filtro de cuotas, usaríamos un cliente con permisos de administración (como `ops`) con un `rate_limit_per_minute` muy elevado o deshabilitado, de forma que el limitador no corte las peticiones y podamos observar la latencia y rendimiento máximo del servidor.
