# Starter — Refactor avanzado de la app de S5

Este starter es un snapshot de la primera interfaz de S5. El formulario y el
gateway básico ya están preparados; no los vuelvas a implementar.

Los `TODO` del trabajo avanzado están en:

- `src/model_ui/session.py`;
- `src/model_ui/policies.py`;
- `src/model_ui/presentation.py`;
- `src/model_ui/controller.py`;
- `app.py`, para caché y renderizado de estados.

Las pruebas describen las transiciones y los contratos públicos. La app debe
conservar el comportamiento de S5 y añadir estado, reintento, limpieza y
telemetría.
