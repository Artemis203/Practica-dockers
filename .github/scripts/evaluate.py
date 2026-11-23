import json, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
C = ["docker", "compose", "-f", str(ROOT / "docker-compose.yml")]
checks = []

def run(args, ok=True):
    return subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=ok)

def result(label, passed, detail=""):
    checks.append(bool(passed))
    print(("PASS" if passed else "FAIL") + " | " + label + ((" | " + detail) if detail else ""))

def request(method, path, data=None):
    body = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request("http://127.0.0.1:5000"+path, data=body, method=method,
                                 headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=4) as r:
        text = r.read().decode()
        return r.status, json.loads(text) if text else None

def wait_health():
    until = time.time()+90
    while time.time() < until:
        try:
            code, body = request("GET", "/health")
            if code == 200 and body.get("status") == "ok": return True
        except Exception:
            pass
        time.sleep(2)
    return False

def main():
    df, cf = ROOT/"Dockerfile", ROOT/"docker-compose.yml"
    result("Existe Dockerfile", df.is_file())
    result("Existe docker-compose.yml", cf.is_file())
    if not df.is_file() or not cf.is_file(): return 1

    d = df.read_text().lower()
    for label, passed in [
        ("Imagen base python:3.11-slim", "python:3.11-slim" in d),
        ("WORKDIR definido", "workdir" in d),
        ("Instala requirements.txt", "requirements.txt" in d and "pip install" in d),
        ("Copia el código", "copy" in d),
        ("Expone puerto 5000", "expose 5000" in d),
        ("Comando de inicio app.py", "app.py" in d and ("cmd" in d or "entrypoint" in d))
    ]: result(label, passed)

    try:
        cfg = json.loads(run(C+["config","--format","json"]).stdout)
        result("docker compose config válido", True)
    except Exception as e:
        result("docker compose config válido", False, str(e))
        return 1

    sv = cfg.get("services", {})
    web, db = sv.get("web", {}), sv.get("db", {})
    result("Servicios web y db", "web" in sv and "db" in sv)
    result("Puerto 5000:5000", any(str(p.get("target"))=="5000" and str(p.get("published"))=="5000" for p in web.get("ports",[])))
    env = web.get("environment", {})
    url = str(env.get("DATABASE_URL","")) if isinstance(env,dict) else ""
    result("DATABASE_URL usa hostname db", "@db:" in url and "localhost" not in url)
    result("Imagen PostgreSQL", "postgres" in str(db.get("image","")).lower())
    persistent = any(isinstance(m,dict) and m.get("type")=="volume" and
                     m.get("target")=="/var/lib/postgresql/data" and
                     m.get("source") in cfg.get("volumes",{}) for m in db.get("volumes",[]))
    result("Volumen nombrado para PostgreSQL", persistent)

    try:
        up = run(C+["up","--build","-d"], ok=False)
        if up.returncode:
            result("Build e inicio", False, up.stdout[-1500:]); return 1
        result("Build e inicio", True)
        healthy = wait_health()
        result("Flask responde y conecta con PostgreSQL", healthy)
        if not healthy:
            print(run(C+["logs","--no-color"],ok=False).stdout[-2500:]); return 1
        code, task = request("POST","/tasks",{"title":"persistencia-docker-challenge"})
        result("API permite insertar tarea", code==201 and task.get("title")=="persistencia-docker-challenge")
        run(C+["down"])
        result("docker compose down", True)
        up2 = run(C+["up","-d"],ok=False)
        result("Servicios reinician", up2.returncode==0)
        if up2.returncode: return 1
        healthy = wait_health()
        result("Base de datos vuelve a estar disponible", healthy)
        if not healthy: return 1
        _, tasks = request("GET","/tasks")
        result("Datos persisten después de down y up",
               any(x.get("title")=="persistencia-docker-challenge" for x in tasks))
    except Exception as e:
        result("Ejecución de servicios y pruebas", False, str(e))
    finally:
        run(C+["down","-v","--remove-orphans"],ok=False)

    total, passed = len(checks), sum(checks)
    print(f"RESULTADO: {passed}/{total} comprobaciones satisfactorias.")
    return 0 if passed==total else 1

if __name__ == "__main__":
    sys.exit(main())
