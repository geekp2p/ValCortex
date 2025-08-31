# file: embed_cli.py
import os
import sys
import argparse
from pathlib import Path

import llama_cpp


CANDIDATE_NAMES = [
    "gpt-oss-20b-Q4_K_M.gguf",
    "llava-v1.6-vicuna-13b.Q4_K_M.gguf",
    "model.gguf",
]

def default_model_path() -> Path:
    env_model = os.environ.get("EMBED_CLI_MODEL")
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
        help="path to .gguf (optional, overrides EMBED_CLI_MODEL)",
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
    llm = llama_cpp.Llama(
        model_path=str(model_path),
        n_threads=args.threads,
        n_ctx=args.ctx,
        verbose=False,
    )
    out = llm(args.prompt)
    print(out)

if __name__ == "__main__":
    main()