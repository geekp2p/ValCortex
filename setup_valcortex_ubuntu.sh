#!/usr/bin/env bash
set -euo pipefail

# ========= Config (แก้ได้) =========
PROJECT_DIR="${PWD}"              # โฟลเดอร์ที่มี docker-compose.yml (ตอนนี้คุณอยู่ใน ~/ValCortex แล้วก็ดี)
CORTEX_ENV="${PROJECT_DIR}/cortex/.env"
DEFAULT_CORS="http://localhost:8083,http://127.0.0.1:8083,*"
TEXT_MODEL="gpt-oss:20b"
VISION_MODEL="llama3.2-vision:11b"
API_PORT_OUT=8088                  # พอร์ตรับจากภายนอก (ตาม compose ปัจจุบัน)
OLLAMA_PORT_OUT=11434
# ===================================

echo "==> Updating apt package index..."
sudo apt update -y

echo "==> Installing prerequisites..."
sudo apt install -y ca-certificates curl gnupg lsb-release jq

# ---- Install Docker (official repo) ----
if ! command -v docker >/dev/null 2>&1; then
  echo "==> Installing Docker Engine + Compose plugin (official repo)..."
  sudo install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  sudo chmod a+r /etc/apt/keyrings/docker.gpg

  codename="$(. /etc/os-release && echo "$UBUNTU_CODENAME")"
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    ${codename} stable" | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null

  sudo apt update -y
  sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  sudo systemctl enable --now docker
else
  echo "==> Docker already installed."
fi

# ---- Add current user to 'docker' group (no sudo) ----
if ! groups "$USER" | grep -q "\bdocker\b"; then
  echo "==> Adding $USER to 'docker' group..."
  sudo groupadd -f docker
  sudo usermod -aG docker "$USER"
  ADDED_TO_DOCKER_GROUP=1
else
  ADDED_TO_DOCKER_GROUP=0
fi

# ---- Make sure we're in the project dir ----
cd "$PROJECT_DIR"

# ---- Create cortex/.env if missing ----
if [ ! -f "$CORTEX_ENV" ]; then
  echo "==> Creating default cortex/.env ..."
  mkdir -p "$(dirname "$CORTEX_ENV")"
  cat > "$CORTEX_ENV" <<EOF
# Text model
OLLAMA_TEXT_MODEL=${TEXT_MODEL}

# Vision model
OLLAMA_VISION_MODEL=${VISION_MODEL}

# Ollama endpoint
OLLAMA_BASE_URL=http://ollama:11434

# CORS allow origins for Game (8083)
CORS_ALLOW_ORIGINS=${DEFAULT_CORS}
EOF
else
  echo "==> cortex/.env already exists. Skipping creation."
fi

# ---- Optional: open firewall (UFW) ----
if command -v ufw >/dev/null 2>&1; then
  echo "==> Opening firewall ports via UFW (if enabled)..."
  sudo ufw allow "${API_PORT_OUT}/tcp" || true
  sudo ufw allow "${OLLAMA_PORT_OUT}/tcp" || true
fi

# ---- Build & Run ----
echo "==> Bringing up ValCortex with Docker Compose..."
# ถ้ายังไม่ได้ re-login หลังเพิ่มกลุ่ม docker ให้ใช้ sudo docker ชั่วคราว
if [ "$ADDED_TO_DOCKER_GROUP" -eq 1 ]; then
  echo "NOTE: You were just added to the 'docker' group."
  echo "      Current shell session may still need sudo. Using 'sudo docker' for this run."
  sudo docker compose down || true
  sudo docker compose up -d --build
else
  docker compose down || true
  docker compose up -d --build
fi

# ---- Health check ----
echo "==> Waiting a few seconds before health check..."
sleep 3
HEALTH_URL="http://localhost:${API_PORT_OUT}/health"
echo "==> Curl: ${HEALTH_URL}"
set +e
curl -sS "${HEALTH_URL}" | jq . || curl -sS "${HEALTH_URL}" || true
set -e

cat <<'TIP'

=== DONE ===
- API:  http://localhost:8088  (ปรับใน docker-compose.yml ถ้าต้องการ)
- Ollama: http://localhost:11434

ทดสอบ:
  curl -s -X POST http://localhost:8088/v1/chat \
    -H "Content-Type: application/json" \
    -d '{"messages":[{"role":"user","content":"ทักจาก Game8"}]}'

  curl -s -X POST http://localhost:8088/v1/vision \
    -F "prompt=อธิบายภาพนี้" \
    -F "image=@/path/to/image.jpg;type=image/jpeg"

หมายเหตุ:
- ถ้าเพิ่งถูกเพิ่มเข้า group 'docker' ให้ 'log out / log in' หรือเปิด shell ใหม่ก่อนใช้คำสั่ง docker โดยไม่ต้อง sudo
- ครั้งแรกที่เรียกใช้แต่ละโมเดล Ollama จะดาวน์โหลดโมเดล อาจใช้เวลาสักครู่
TIP
