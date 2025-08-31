# file: embed_cli.py
import os
import sys
import argparse
from pathlib import Path

import llama_cpp


ENV_VAR_NAME = "EMBED_CLI_MODEL"
"""Environment variable that specifies a model path override."""

CANDIDATE_NAMES = [
    "gpt-oss-20b-Q4_K_M.gguf",
    "llava-v1.6-vicuna-13b.Q4_K_M.gguf",
    "model.gguf",
]


def default_model_path() -> Path:
    """Return the first existing model path from env var or default locations."""

    env_model = os.environ.get(ENV_VAR_NAME)
    if env_model:
        candidate = Path(env_model)
        if candidate.exists():
            return candidate

    if hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS) / "models"
    else:
        base = Path(__file__).parent / "models"

    for name in CANDIDATE_NAMES:
        p = base / name
        if p.exists():
            return p

    return base / CANDIDATE_NAMES[-1]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--model",
        type=Path,
        help=f"path to .gguf (optional, overrides {ENV_VAR_NAME})",
    )
    ap.add_argument("--prompt", type=str, default="Hello from embedded model")
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--ctx", type=int, default=4096)
    args = ap.parse_args()

    model_path = args.model or default_model_path()
    if not model_path.exists():
        print(f"[!] Model file not found: {model_path}")
        sys.exit(1)

    print(f"[+] Loading model: {model_path}")
    try:
        llm = llama_cpp.Llama(
            model_path=str(model_path),
            n_threads=args.threads,
            n_ctx=args.ctx,
            verbose=False,
        )
    except ValueError as e:
        msg = str(e)
        if "invalid type" in msg.lower() or "failed to load" in msg.lower():
            print(f"[!] {msg}")
            print(
                "[!] Tip: verify checksum, re-download the model, or upgrade llama-cpp-python."
            )
        else:
            print(f"[!] {msg}")
        sys.exit(1)
    out = llm(args.prompt)
    print(out)

if __name__ == "__main__":
    main()