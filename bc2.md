ValCortex + GPT-OSS-20B Setup (Windows)
1. ดาวน์โหลดโมเดล (.gguf)

โมเดลจะถูกเก็บไว้ที่ G:\models

# สร้างโฟลเดอร์เก็บโมเดล
New-Item -ItemType Directory -Force -Path G:\models | Out-Null

# ดาวน์โหลดไฟล์ quant แบบ Q4_K_M (ประหยัดแรม ~16GB+)
curl.exe -L ^
  "https://huggingface.co/unsloth/gpt-oss-20b-GGUF/resolve/main/gpt-oss-20b-Q4_K_M.gguf?download=true" ^
  -o "G:\models\gpt-oss-20b-Q4_K_M.gguf"


📌 ที่มา Hugging Face: unsloth/gpt-oss-20b-GGUF

(เลือก quant อื่นๆ ได้ เช่น Q5_K_M, Q8_0 ตามสเปกเครื่อง)

2. เตรียมโฟลเดอร์สำหรับ Binary

ไบนารี/EXE ของคุณจะอยู่ที่ G:\ai

# สร้างโฟลเดอร์หลักสำหรับงาน
New-Item -ItemType Directory -Force -Path G:\ai | Out-Null
cd G:\ai

# โคลนโปรเจกต์ ValCortex
git clone https://github.com/geekp2p/ValCortex

3. Build API Binary (valcortex-api.exe)
cd G:\ai\ValCortex\cortex

# สร้าง environment แยก
conda create -n valcortex python=3.10 -y
conda activate valcortex

# ติดตั้ง dependencies
pip install -r requirements.txt pyinstaller

# สร้าง binary API
pyinstaller --onefile --name valcortex-api app.py

# ไฟล์จะออกที่ dist\valcortex-api.exe

รันทดสอบ
cd dist
.\valcortex-api.exe

4. Build Local Model Binary (ฝังโมเดล)
cd G:\ai\ValCortex\local_model

conda create -n valmodel python=3.10 -y
conda activate valmodel

pip install -r requirements.txt pyinstaller

# สร้าง binary ที่ฝังโมเดล .gguf เข้าไปด้วย
pyinstaller --onefile `
  --add-data "G:\models\gpt-oss-20b-Q4_K_M.gguf;gpt-oss-20b-Q4_K_M.gguf" `
  --name local-model app.py

รันทดสอบ
cd dist
.\local-model.exe

5. Notes

valcortex-api.exe → ให้บริการ HTTP API (สำหรับเชื่อมต่อภายนอก)

local-model.exe → โหลดโมเดล .gguf ที่ฝังไว้ภายใน binary

หากใช้ Ollama → ตรวจสอบว่า Ollama service ทำงานอยู่ และตั้งค่า OLLAMA_MODELS=G:\models

แนะนำให้ทดสอบโมเดลใน LM Studio
 หรือ llama.cpp
 ได้เช่นกัน

✅ ตอนนี้คุณสามารถโหลดโมเดล, build binary และวางในตำแหน่งที่ต้องการ (G:\models / G:\ai) ได้ครบแล้ว

คุณอยากให้ผมเพิ่ม ส่วน .env config ตัวอย่าง (เช่น พอร์ต API, เส้นทางโมเดล, key อื่นๆ) ไว้ใน README.md นี้เลยไหมครับ?