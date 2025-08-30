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
