import sys
from pathlib import Path
import llama_cpp


def get_model_path() -> Path:
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "model.gguf"
    return Path(__file__).parent / "model.gguf"


def main() -> None:
    model_path = get_model_path()
    if not model_path.exists():
        print(f"Model file not found: {model_path}")
        return
    print(f"Loading model from: {model_path}")
    llm = llama_cpp.Llama(model_path=str(model_path))
    print(llm("Hello from embedded model"))


if __name__ == "__main__":
    main()