1. ดาวน์โหลดโมเดล gpt-oss:20b (ไฟล์ .gguf)
# สร้างโฟลเดอร์สำหรับโมเดล
mkdir C:\models
cd C:\models

# ดาวน์โหลดโมเดลจาก HuggingFace (ตัวอย่าง URL)
Invoke-WebRequest `
  -Uri https://huggingface.co/.../gpt-oss-20b.Q4_K_M.gguf `
  -OutFile gpt-oss-20b.gguf
2. สร้างไฟล์ปฏิบัติการสำหรับ API (cortex)
# เปิด Anaconda Prompt
git clone https://github.com/.../ValCortex.git
cd ValCortex\cortex

conda create -n valcortex python=3.10 -y
conda activate valcortex

pip install -r requirements.txt pyinstaller

pyinstaller --onefile --name valcortex-api app.py

# ทดสอบรัน
.\dist\valcortex-api.exe
ใส่ไฟล์ .env (หรือตัวแปรแวดล้อม) ในโฟลเดอร์เดียวกับ .exe เพื่อกำหนดค่า config ต่าง ๆ

3. สร้างไฟล์ปฏิบัติการฝังโมเดล (local_model)
cd ..\local_model

conda create -n valmodel python=3.10 -y
conda activate valmodel

pip install -r requirements.txt pyinstaller

pyinstaller --onefile `
  --add-data "C:\models\gpt-oss-20b.gguf;gpt-oss-20b.gguf" `
  --name local-model app.py

# ทดสอบรัน
.\dist\local-model.exe
ไบนารี local-model.exe จะมีโมเดล gpt-oss-20b.gguf ฝังอยู่ภายในแล้ว

🐧 Ubuntu
1. ดาวน์โหลดโมเดล gpt-oss:20b
mkdir -p ~/models
cd ~/models

# ดาวน์โหลดโมเดลจาก HuggingFace (ตัวอย่าง URL)
wget -O gpt-oss-20b.gguf \
  https://huggingface.co/.../gpt-oss-20b.Q4_K_M.gguf
2. สร้างไฟล์ปฏิบัติการสำหรับ API (cortex)
git clone https://github.com/.../ValCortex.git
cd ValCortex/cortex

conda create -n valcortex python=3.10 -y
conda activate valcortex

pip install -r requirements.txt pyinstaller

pyinstaller --onefile --name valcortex-api app.py

# ทดสอบรัน
./dist/valcortex-api
3. สร้างไฟล์ปฏิบัติการฝังโมเดล (local_model)
cd ../local_model

conda create -n valmodel python=3.10 -y
conda activate valmodel

pip install -r requirements.txt pyinstaller

pyinstaller --onefile \
  --add-data "$HOME/models/gpt-oss-20b.gguf:gpt-oss-20b.gguf" \
  --name local-model app.py

# ทดสอบรัน
./dist/local-model
✅ สรุป
ใช้ conda สร้าง environment แยกสำหรับ API และโปรแกรมฝังโมเดล

ดาวน์โหลดโมเดล .gguf ใหม่ทั้งหมดก่อนคอมไพล์

ใช้ PyInstaller สร้างไฟล์ปฏิบัติการ .exe (Windows) หรือไฟล์เดียวบน Ubuntu

valcortex-api ให้บริการ HTTP API

local-model โหลดโมเดล gpt-oss:20b ที่ฝังไว้และพร้อมรัน inference ทันที

นำขั้นตอนเหล่านี้ไปใช้โดยตรงบนเครื่องของคุณเพื่อสร้างไบนารีที่มี AI รวมอยู่ในตัวครับ!