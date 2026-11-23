# Docker Challenge — De código a contenedores

**Modalidad:** individual | **Duración:** 2 horas | **Nivel:** básico

## Situación
Recibes una aplicación Flask para registrar tareas. Los datos se guardan en PostgreSQL. Tu reto es contenerizar la aplicación y ejecutar ambos servicios con Docker Compose. No debes programar la aplicación: concéntrate en Docker.

## Misión 1 — Dockerfile (25 puntos)
Crea `Dockerfile` en la raíz. Debe:
- Usar `python:3.11-slim`.
- Definir `/app` como `WORKDIR`.
- Copiar `requirements.txt` e instalar dependencias.
- Copiar el código de la aplicación.
- Exponer el puerto `5000`.
- Iniciar con `python app.py`.

Crea `.dockerignore` que excluya `.git`, `__pycache__` y archivos `.pyc`.

## Misión 2 — Docker Compose (30 puntos)
Crea `docker-compose.yml` con dos servicios:
- `web`: construye desde el directorio actual, publica `5000:5000` y define `DATABASE_URL`.
- `db`: usa una imagen oficial PostgreSQL y configura usuario, contraseña y base de datos.

La URL de conexión debe usar el hostname `db`, no `localhost`. Ejemplo:
`postgresql://usuario:contraseña@db:5432/nombre_base_datos`

Docker Compose crea una red predeterminada para que los servicios se comuniquen.

## Misión 3 — Persistencia (25 puntos)
Declara un volumen nombrado y móntalo en el servicio PostgreSQL en:
`/var/lib/postgresql/data`
No uses Bind Mount para esta misión.

## Misión 4 — Pruebas y documentación (20 puntos)
1. `docker compose config`
2. `docker compose up --build -d`
3. Abre `http://localhost:5000`.
4. Comprueba `http://localhost:5000/health`.
5. Registra una tarea en la página o con la API.
6. Ejecuta `docker compose down` (sin `-v`), inicia de nuevo y comprueba que la tarea sigue allí.
7. Completa la sección **Mi solución** de tu README.

## Comandos útiles

```bash
docker --version
docker compose version
docker compose config
docker compose up --build -d
docker compose ps
docker compose logs web
docker compose logs db
docker compose down
curl http://localhost:5000/health
curl http://localhost:5000/tasks
curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"title":"Mi primera tarea"}'
```

## Evidencias en README
Incluye:
- Enlace a tu repositorio.
- Captura o transcripción de `docker compose ps`.
- Resultado de `docker compose config`.
- Dos o tres frases explicando por qué `DATABASE_URL` usa `db` y no `localhost`.
- Explicación de qué ocurre con los datos al ejecutar `docker compose down` y volver a iniciar.

## Distribución de los 120 minutos

| Tiempo | Actividad |
|---|---|
| 0–10 | Revisar aplicación y reto |
| 10–35 | Dockerfile y .dockerignore |
| 35–70 | Compose y comunicación |
| 70–90 | Volumen y persistencia |
| 90–105 | Pruebas y correcciones |
| 105–115 | README y Actions |
| 115–120 | Entrega del enlace |

**Entrega final:** repositorio GitHub individual. La evaluación automática debe finalizar correctamente y debes poder explicar tus decisiones.
