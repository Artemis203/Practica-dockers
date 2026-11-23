# Rúbrica docente — Docker Challenge

**Puntaje total: 100 puntos.** Modalidad individual, 2 horas.

## A. Evaluación automática — 80 puntos

| Criterio | Evidencia | Puntos |
|---|---|---:|
| Dockerfile | Imagen base, WORKDIR, instalación, COPY, puerto y comando | 20 |
| Compose válido | `docker compose config` y servicios `web` y `db` | 10 |
| Servicio web | Puerto 5000:5000 y `DATABASE_URL` con hostname `db` | 15 |
| PostgreSQL | Imagen oficial y configuración de base de datos | 10 |
| Volumen nombrado | Declarado y montado en `/var/lib/postgresql/data` | 10 |
| Construcción y ejecución | Servicios construyen e inician | 5 |
| Aplicación funcional | `/health` y API de tareas funcionan | 5 |
| Persistencia | La tarea sobrevive a `down` y `up` | 5 |
| **Subtotal** | | **80** |

## B. Revisión docente — 20 puntos

| Criterio | Evidencia | Puntos |
|---|---|---:|
| README | Enlace, comandos y evidencias solicitadas | 5 |
| Imagen vs. contenedor | Explicación propia y correcta | 5 |
| Red | Explica por qué `db` y no `localhost` | 5 |
| Persistencia | Explica el volumen y diferencia `down` de `down -v` | 5 |
| **Subtotal** | | **20** |

## Escala sugerida

| Puntaje | Desempeño | Nota sobre 5 |
|---:|---|---:|
| 90–100 | Superior | 4.5–5.0 |
| 80–89 | Alto | 4.0–4.4 |
| 60–79 | Básico | 3.0–3.9 |
| 0–59 | Bajo | 0.0–2.9 |

Conversión proporcional alternativa: **nota = puntaje / 20**.

## Preguntas rápidas de verificación
Escoge una o dos por estudiante:
1. ¿Por qué `localhost` dentro de `web` no apunta al contenedor PostgreSQL?
2. ¿Cuál es la diferencia entre imagen y contenedor?
3. ¿Qué función cumple `WORKDIR`?
4. ¿Qué conserva `docker compose down`?
5. ¿Qué diferencia hay al ejecutar `docker compose down -v`?
6. ¿Por qué el volumen se monta en `/var/lib/postgresql/data`?
7. Si cambias `requirements.txt`, ¿cómo reconstruyes la imagen?

## Protocolo ágil
1. Abrir el repositorio.
2. Revisar último workflow en Actions.
3. Registrar resultado automático sobre 80.
4. Revisar README (30–45 segundos).
5. Hacer una pregunta conceptual (30 segundos).
6. Registrar los 20 puntos docentes.

Tiempo estimado: 1–2 minutos por entrega cuando Actions ya terminó.

## Integridad
El workflow facilita la revisión, pero no demuestra por sí solo la autoría. Contrasta el resultado con los archivos, el historial de commits y una breve explicación oral. No aceptes una captura aislada como única evidencia.
