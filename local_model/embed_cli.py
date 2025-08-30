# file: embed_cli.py
import sys
import argparse
from pathlib import Path

import llama_cpp

def default_model_path() -> Path:
    # หากเป็น EXE แบบ onefile -> ใช้โฟลเดอร์ชั่วคราวของ PyInstaller
    if hasattr(sys, "_MEIPASS"):
        # ดีฟอลต์หาที่ models\model.gguf ถ้าอยากชี้ไฟล์เฉพาะ ให้ส่ง --model
        cand = Path(sys._MEIPASS) / "models" / "model.gguf"
        if cand.exists():
            return cand
        # เผื่อชื่อไฟล์จริง
        for name in ["gpt-oss-20b-Q4_K_M.gguf", "llava-v1.6-vicuna-13b.Q4_K_M.gguf"]:
            p = Path(sys._MEIPASS) / "models" / name
            if p.exists():
                return p
        # ฟอลล์แบ็กสุดท้าย
        return Path(sys._MEIPASS) / "model.gguf"

    # โหมดสคริปต์ปกติ: หาข้างไฟล์สคริปต์
    here = Path(__file__).parent
    cand = here / "models" / "model.gguf"
    if cand.exists():
        return cand
    for name in ["gpt-oss-20b-Q4_K_M.gguf", "llava-v1.6-vicuna-13b.Q4_K_M.gguf"]:
        p = here / "models" / name
        if p.exists():
            return p
    return here / "model.gguf"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=Path, help="path to .gguf (optional)")
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
