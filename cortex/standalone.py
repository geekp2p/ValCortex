import os
import subprocess
import sys
import atexit
import shutil
import uvicorn
from app import app


def _find_ollama_binary() -> str:
    """Return path to bundled or system ollama binary."""
    if getattr(sys, "frozen", False):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        candidate = os.path.join(base_path, "ollama.exe" if os.name == "nt" else "ollama")
        if os.path.exists(candidate):
            return candidate
    return shutil.which("ollama") or "ollama"


def _start_ollama(models_path: str) -> subprocess.Popen:
    env = os.environ.copy()
    env["OLLAMA_MODELS"] = models_path
    return subprocess.Popen([_find_ollama_binary(), "serve"], env=env)


if __name__ == "__main__":
    models_path = os.getenv("OLLAMA_MODELS", "G:\\models" if os.name == "nt" else "/models")
    ollama_proc = _start_ollama(models_path)

    def _cleanup() -> None:
        if ollama_proc.poll() is None:
            ollama_proc.terminate()
            try:
                ollama_proc.wait(timeout=10)
            except Exception:
                ollama_proc.kill()

    atexit.register(_cleanup)

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8080"))
    uvicorn.run(app, host=host, port=port, log_level="info")