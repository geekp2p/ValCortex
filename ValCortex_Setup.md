# ValCortex + vicuna-13b Setup (Windows)

## 0. ดาวน์โหลดโมเดล (.gguf)

แนะนำเริ่มด้วย quant Q4_K_M (สมดุลคุณภาพ/แรม)

# โฟลเดอร์ปลายทาง
```powershell
New-Item -ItemType Directory -Force -Path G:\models | Out-Null
```

# ดาวน์โหลดไฟล์เดียว (Q4_K_M ~7.9GB)
```powershell
curl.exe -L "https://huggingface.co/cjpais/llava-v1.6-vicuna-13b-gguf/resolve/main/llava-v1.6-vicuna-13b.Q4_K_M.gguf?download=true" -o "G:\models\llava-v1.6-vicuna-13b.Q4_K_M.gguf"
```


# ValCortex + GPT-OSS-20B Setup (Windows)

## 1. ดาวน์โหลดโมเดล (.gguf)

> โมเดลจะถูกเก็บไว้ที่ `G:\models`

```powershell
# สร้างโฟลเดอร์เก็บโมเดล (ถ้ายังไม่มี)
New-Item -ItemType Directory -Force -Path G:\models | Out-Null
```

```powershell
# ดาวน์โหลดไฟล์ quant แบบ Q4_K_M (ประหยัดแรม ~16GB+)
curl.exe -L "https://huggingface.co/unsloth/gpt-oss-20b-GGUF/resolve/main/gpt-oss-20b-Q4_K_M.gguf?download=true" -o "G:\models\gpt-oss-20b-Q4_K_M.gguf"
```

📌 ที่มา Hugging Face: [unsloth/gpt-oss-20b-GGUF](https://huggingface.co/unsloth/gpt-oss-20b-GGUF)  
(เลือก quant อื่นๆ ได้ เช่น Q5_K_M, Q8_0 ตามสเปกเครื่อง)

---

## 2. เตรียมโฟลเดอร์สำหรับ Binary

> ไบนารี/EXE ของคุณจะอยู่ที่ `G:\ai`

```powershell
New-Item -ItemType Directory -Force -Path G:\ai | Out-Null
cd G:\ai
git clone https://github.com/geekp2p/ValCortex
```

---

## 3. Build API Binary (valcortex-api.exe)
wget "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" -OutFile "G:\ai\Miniconda3-latest-Windows-x86_64.exe"

```powershell
cd G:\ai\ValCortex\cortex
# conda create -n valcortex python=3.10 -y
conda create -n valcortex -c conda-forge python=3.10 -y
conda activate valcortex
pip install -r requirements.txt pyinstaller
pyinstaller --onefile --name valcortex-api start_api.py
```

set OLLAMA_BASE_URL=http://127.0.0.1:11434
set OLLAMA_TEXT_MODEL=gpt-oss:20b
set OLLAMA_VISION_MODEL=llava:13b



### รันทดสอบ
```powershell
cd dist
.\valcortex-api.exe
```

---

## 4. Build Local Model Binary (ฝังโมเดล)

```powershell
cd G:\ai\ValCortex\local_model
conda create -n valmodel python=3.10 -y
conda activate valmodel
pip install -r requirements.txt pyinstaller
pyinstaller --onefile --add-data "G:\models\gpt-oss-20b-Q4_K_M.gguf;gpt-oss-20b-Q4_K_M.gguf" --name local-model app.py
```

### รันทดสอบ
```powershell
cd dist
.\local-model.exe
```

---

## 5. Notes

- `valcortex-api.exe` → ให้บริการ HTTP API (สำหรับเชื่อมต่อภายนอก)  
- `local-model.exe` → โหลดโมเดล `.gguf` ที่ฝังไว้ภายใน binary  
- หากใช้ Ollama → ตรวจสอบว่า Ollama service ทำงานอยู่ และตั้งค่า `OLLAMA_MODELS=G:\models`  
- แนะนำให้ทดสอบโมเดลใน [LM Studio](https://lmstudio.ai) หรือ [llama.cpp](https://github.com/ggerganov/llama.cpp) ได้เช่นกัน  

---

✅ ตอนนี้คุณสามารถโหลดโมเดล, build binary และวางในตำแหน่งที่ต้องการ (`G:\models` / `G:\ai`) ได้ครบแล้ว
