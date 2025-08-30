# ValCortex 🧠

**ValCortex** คือ “สมอง” ของโลก **PixelVal**
ทำหน้าที่เป็น AI Decision Engine สำหรับ **Game8** และแอป/ระบบอื่น ๆ

## Features
- 🌐 HTTP API เดียว รับได้ทั้งข้อความ (`/v1/chat`) และรูปภาพ (`/v1/vision`)
- 🤖 ใช้ **gpt-oss:20b** เป็นโมเดลข้อความหลัก
- 👁️ ใช้ **llama3.2-vision:11b** (หรือ llava/minicpm-v) สำหรับการวิเคราะห์ภาพ
- 🔄 รองรับ CORS → Game8 ยิงมาได้ทันที (port 8082)

## Quick Start
```bash
cd ValCortex
cp cortex/.env.example cortex/.env
docker compose up -d --build
```

## Standalone executable

ต้องการรัน API แบบไม่พึ่ง Docker ก็ทำได้โดยใช้ [PyInstaller](https://www.pyinstaller.org/) สร้างไฟล์ไบนารีตัวเดียว:

```bash
cd cortex
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pyinstaller
pyinstaller --onefile --name valcortex-api app.py
./dist/valcortex-api
```

ไฟล์จะอ่านค่าคอนฟิกจากตัวแปรแวดล้อมหรือไฟล์ `.env` ในไดเรกทอรีเดียวกัน