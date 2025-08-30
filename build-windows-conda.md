# เปิด Anaconda Prompt
git clone https://github.com/.../ValCortex.git
cd ValCortex\cortex

# สร้าง environment ชื่อ valcortex
conda create -n valcortex python=3.10 -y
conda activate valcortex

# ติดตั้งไลบรารีและ PyInstaller
pip install -r requirements.txt pyinstaller

# สร้างไฟล์ปฏิบัติการ
pyinstaller --onefile --name valcortex-api app.py

# รันเพื่อทดสอบ
.\dist\valcortex-api.exe
