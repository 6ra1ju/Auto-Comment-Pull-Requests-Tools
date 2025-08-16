# Chạy Temporal server (nền)
temporal server start-dev &
# Chạy worker (nền)
python -m AI_reviewer.temporal.worker &
# Chạy FastAPI (nền)
uvicorn AI_reviewer.main:app --reload &
# Chạy ngrok (nền)
ngrok http --domain=rhino-exciting-baboon.ngrok-free.app 8000 &
# Đợi tất cả process
wait
