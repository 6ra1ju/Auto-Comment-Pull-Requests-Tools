# 🤖 AI Pull Request Reviewer

Tự động review và comment Pull Request bằng AI, tích hợp trực tiếp với GitHub và workflow của Temporal

---

## Tổng quan

**AI Pull Request Reviewer** là tool tự động giúp các team phát triển phần mềm nhận được phản hồi code review chất lượng cao ngay khi có Pull Request mới.  
Công cụ sử dụng AI (Groq/OpenAI) để phân tích diff code, tạo nhận xét review sắc sảo và **tự động comment lên Pull Request trên GitHub**.

Hệ thống được xây dựng với kiến trúc hiện đại, sử dụng **Temporal Workflow** để đảm bảo độ tin cậy, tự động retry khi gặp lỗi mạng, timeout hoặc bị rate limit.

---

## Tính năng nổi bật

- 🤖 **Review tự động bằng AI**: Phân tích diff code và sinh nhận xét thông minh, sắc sảo.
- 🔄 **Tự động retry**: Workflow tự động retry khi gặp timeout, mất mạng hoặc rate limit
- 📝 **Tích hợp GitHub**: Tự động comment lên Pull Request khi có thay đổi mới.
- ⚙️ **Workflow bền vững**: Sử dụng Temporal để orchestrate quá trình review, không mất task khi gặp sự cố.
- 🪝 **Webhook GitHub**: Nhận sự kiện Pull Request mới qua webhook và xử lý hoàn toàn tự động.
- 🌍 **Hỗ trợ đa ngôn ngữ**: Prompt AI có thể tùy chỉnh tiếng Việt hoặc tiếng Anh.

---


## Điều kiện tiên quyết
* Python 3.8+

* Temporal Server (temporal server start-dev)

* Groq hoặc OpenAI API Key

* GitHub token có quyền comment Pull requests

* ngrok hoặc cloudflared để expose webhook nếu chạy local

* FastAPI

## Thiết lập GitHub Webhook
* Vào GitHub repository của bạn → Settings → Webhooks → Add webhook

* Thiết lập:

  * Payload URL: `http://<ngrok-domain>/webhook`

  * Content type: application/json

  * Secret: Trùng với biến môi trường GITHUB_WEBHOOK_SECRET

  * Events: Chọn Pull requests

## Cách hoạt động
* Khi có PR mới hoặc được cập nhật, GitHub gửi sự kiện tới backend thông qua webhook.

* Backend (FastAPI) lấy diff code của Pull requests và khởi chạy Temporal Workflow.

* Workflow thực hiện:

  * Gọi AI (Groq/OpenAI) để phân tích diff và tạo review.

  * Gửi nhận xét tự động lên GitHub Pull Request.

  * Nếu có lỗi như mất mạng, timeout, rate limit: Workflow sẽ tự động retry theo chính sách cấu hình.


## Cấu trúc dự án

* Auto-Comment-Pull-Requests-Tools
  * AI_reviewer/
    * main.py               # FastAPI backend
    * github_api.py         # Tương tác với GitHub API
    * config.py             # Biến môi trường, cấu hình
    * ai_reviewer.py        # Gọi AI (Groq/OpenAI)
    * temporal/
      * worker.py         # Temporal worker
      * activities.py     # Review & comment activities
      * temporal_review_workflow.py  # Workflow logic
  * requirements.txt # Package dependencies
  * .env
  * README.md
# Hướng dẫn chạy thử

## Clone dự án
* git clone <repo-url>
* cd Auto-Comment-Pull-Requests-Tools

## Tạo môi trường ảo & cài đặt dependencies
* Trên MacOS / Linux
  * python -m venv venv
  * source venv/bin/activate
  * pip install -r requirements.txt
* Trên Windows
  * python -m venv venv
  * venv\Scripts\activate
  * pip install -r requirements.txt

## Cài đặt biến môi trường
* cp .env.example .env
* Điền các biến như GITHUB_TOKEN, GITHUB_WEBHOOK_SECRET, GROQ_API_KEY, ...

## Chạy dự án cách 1
* Chạy Temporal server : temporal server start-dev

* Khởi động worker Temporal : python -m AI_reviewer.temporal.worker

* Chạy FastAPI backend : uvicorn AI_reviewer.main:app --reload

* Expose webhook ra internet : ngrok http://<ngrok-domain>/ 8000

## Chạy dự án cách 2:
* Chạy lệnh chmod +x run_all.sh
./run_all.sh


  
## Xử lý lỗi & Retry
| Sự cố       | Cơ chế xử lý   |
|:-----------|:---------:|
| Timeout / mất mạng | Workflow tự động retry với backoff |
| GitHub rate limit | Retry + backoff exponential |

## Demo
[Video Demo Tool](https://drive.google.com/drive/u/7/folders/1QFsDL6VPz5n6I8VhuoGgKEP3tvqEW4Wm)
