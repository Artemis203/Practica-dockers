import os, time
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
DB = os.environ.get("DATABASE_URL", "postgresql://challenge:challengepass@localhost:5432/challenge")

def connect():
    return psycopg2.connect(DB, connect_timeout=3)

def initialize():
    last = None
    for _ in range(30):
        try:
            with connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("CREATE TABLE IF NOT EXISTS tasks (id SERIAL PRIMARY KEY, title VARCHAR(200) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            return
        except psycopg2.OperationalError as exc:
            last = exc
            time.sleep(1)
    raise RuntimeError(f"No se pudo conectar a PostgreSQL: {last}")

@app.get("/")
def home():
    return """<!doctype html><html lang='es'><meta charset='utf-8'><title>Docker Challenge</title>
    <body style='font-family: sans-serif; max-width:700px; margin:3rem auto'>
    <h1>Lista de tareas</h1><p>Flask + PostgreSQL</p>
    <form id='f'><input id='t' required placeholder='Nueva tarea'><button>Agregar</button></form>
    <ul id='list'></ul><script>
    async function load(){let r=await fetch('/tasks');let a=await r.json();document.querySelector('#list').innerHTML=a.map(x=>'<li>'+x.title+'</li>').join('')}
    document.querySelector('#f').onsubmit=async e=>{e.preventDefault();await fetch('/tasks',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title:document.querySelector('#t').value})});document.querySelector('#t').value='';load()};load();
    </script></body></html>"""

@app.get("/health")
def health():
    try:
        with connect() as conn:
            with conn.cursor() as cur: cur.execute("SELECT 1")
        return jsonify(status="ok", database="connected")
    except Exception as exc:
        return jsonify(status="error", detail=str(exc)), 503

@app.get("/tasks")
def tasks():
    with connect() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, title FROM tasks ORDER BY id")
            rows = cur.fetchall()
    return jsonify([dict(row) for row in rows])

@app.post("/tasks")
def add_task():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title: return jsonify(error="title es obligatorio"), 400
    with connect() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("INSERT INTO tasks(title) VALUES (%s) RETURNING id, title", (title[:200],))
            row = cur.fetchone()
    return jsonify(dict(row)), 201

if __name__ == "__main__":
    initialize()
    app.run(host="0.0.0.0", port=5000)
