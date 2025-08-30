ดาวน์โหลดโมเดล gpt-oss:20b (ไฟล์ .gguf)

# สร้างโฟลเดอร์สำหรับโมเดล
mkdir C:\models
cd C:\models

# ดาวน์โหลดโมเดลจาก HuggingFace (ตัวอย่าง URL)
Invoke-WebRequest `
  -Uri https://huggingface.co/.../gpt-oss-20b.Q4_K_M.gguf `
  -OutFile gpt-oss-20b.gguf





สร้างไฟล์ปฏิบัติการสำหรับ API

# เปิด Anaconda Prompt
git clone https://github.com/.../ValCortex.git
cd ValCortex\cortex

# สร้าง environment ชื่อ valcortex
conda create -n valcortex python=3.10 -y
conda activate valcortex

# ติดตั้งไลบรารีและ PyInstaller
pip install -r requirements.txt pyinstaller

# สร้างไฟล์ปฏิบัติการ
pyinstaller --onefile --name valcortex-api start_api.py

# รันเพื่อทดสอบ
.\dist\valcortex-api.exe

สร้างไฟล์ปฏิบัติการฝังโมเดล gpt-oss:20b

cd ..\local_model

# สร้าง environment แยกสำหรับโมเดล
conda create -n valmodel python=3.10 -y
conda activate valmodel

# ติดตั้งไลบรารีและ PyInstaller
pip install -r requirements.txt pyinstaller

# สร้างไฟล์ปฏิบัติการพร้อมฝังโมเดล gpt-oss:20b
pyinstaller --onefile `
  --add-data "C:\models\gpt-oss-20b.gguf;gpt-oss-20b.gguf" `
  --name local-model app.py

# รันเพื่อทดสอบ
.\dist\local-model.exe
