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

## Embedded local model

มีตัวอย่างโปรเจ็กต์ `local_model/` สำหรับรันหรือฝังโมเดล `.gguf` ด้วย Python:

```bash
cd local_model
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py path/to/model.gguf
```

ถ้าต้องการรวมโมเดลเข้าไปในไบนารีไฟล์เดียวใช้ PyInstaller:

```bash
pyinstaller --onefile \
  --add-data "path/to/model.gguf:model.gguf" \
  app.py
```

ใน `docker-compose.yml` มีบริการ `embedded` ที่รันสคริปต์นี้และคาดหวังให้วางโมเดลไว้ในโฟลเดอร์ `./models` ก่อนสั่ง `docker compose up`.

## สร้างไฟล์ปฏิบัติการบน Windows

### API หลัก (`cortex`)

1. ติดตั้ง [Python 3.10+ แบบ 64‑bit](https://www.python.org/downloads/windows/) และ Git
2. เปิด PowerShell แล้วรันคำสั่งต่อไปนี้:

    ```powershell
    cd cortex
    python -m venv .venv
    .\.venv\Scripts\activate
    pip install -r requirements.txt pyinstaller
    pyinstaller --onefile --name valcortex-api app.py
    .\dist\valcortex-api.exe
    ```

### ฝังโมเดล `.gguf`

1. วางไฟล์โมเดลไว้ตามต้องการ เช่น `C:\models\model.gguf`
2. รันจากโฟลเดอร์ `local_model`:

    ```powershell
    cd local_model
    python -m venv .venv
    .\.venv\Scripts\activate
    pip install -r requirements.txt pyinstaller
    pyinstaller --onefile \
      --add-data "C:\\models\\model.gguf;model.gguf" \
      --name local-model app.py
    .\dist\local-model.exe
    ```

## สร้างไฟล์ปฏิบัติการบน Ubuntu

### API หลัก (`cortex`)

1. ติดตั้ง Python และเครื่องมือพื้นฐาน: `sudo apt update && sudo apt install -y python3 python3-venv python3-pip`
2. รันคำสั่ง:

    ```bash
    cd cortex
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt pyinstaller
    pyinstaller --onefile --name valcortex-api app.py
    ./dist/valcortex-api
    ```

### ฝังโมเดล `.gguf`

1. วางไฟล์โมเดลไว้ในเครื่อง เช่น `/models/model.gguf`
2. รันจากโฟลเดอร์ `local_model`:

    ```bash
    cd local_model
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt pyinstaller
    pyinstaller --onefile \
      --add-data "/models/model.gguf:model.gguf" \
      --name local-model app.py
    ./dist/local-model
    ```