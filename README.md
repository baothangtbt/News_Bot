# 🤖 Bot Điểm Tin & Phân Tích Tài Chính bằng AI (Gemini)

Bot Telegram tự động quét tin tức tài chính, chứng khoán từ các trang báo lớn (CafeF, VnExpress) và sử dụng trí tuệ nhân tạo **Google Gemini (Gen 3 / 2.5)** để phân tích, tóm tắt và đánh giá tác động thị trường. Hệ thống chạy hoàn toàn tự động (Serverless) thông qua **GitHub Actions**.

## ✨ Tính năng nổi bật

* **🕵️‍♂️ Quét tin tự động (Cron Job):** Tự động lọc các bài báo mới nhất dựa trên bộ từ khóa mục tiêu (vàng, chứng khoán, fed, lãi suất, bất động sản...) mỗi 2 tiếng.
* **🧠 Phân tích sâu bằng AI (Gemini 3 Pro/Flash):**
    * Tóm tắt nhanh nội dung bài báo trong 1 câu.
    * Dự báo xu hướng ngắn hạn của Vàng (XAU/USD) và DXY.
    * Chấm điểm tác động đến tâm lý thị trường (Thang điểm 1-10).
    * Gợi ý các mã cổ phiếu Việt Nam (Ticker) có thể hưởng lợi hoặc chịu bất lợi.
* **🔄 Cơ chế Fallback an toàn:** Tự động chuyển đổi giữa các model AI (từ Gemini 3 Pro -> 3 Flash -> 2.5) nếu máy chủ Google quá tải, đảm bảo bot luôn hoạt động.
* **☁️ Miễn phí Server 100%:** Hoạt động hoàn toàn dựa trên GitHub Actions, không cần treo máy, không tốn chi phí duy trì.

## 🛠️ Yêu cầu chuẩn bị

Để tự cài đặt và chạy bot này, bạn cần có 3 thông tin bảo mật sau:
1.  **TELEGRAM_TOKEN:** Lấy từ `@BotFather` trên Telegram.
2.  **CHAT_ID:** ID cá nhân (lấy từ `@userinfobot`) hoặc ID của Group/Channel Telegram (bắt đầu bằng dấu `-`).
3.  **GEMINI_API_KEY:** Tạo miễn phí tại [Google AI Studio](https://aistudio.google.com/).

## 🚀 Hướng dẫn cài đặt

**Bước 1:** Fork (Sao chép) kho lưu trữ này về tài khoản GitHub của bạn.

**Bước 2:** Truy cập vào kho lưu trữ vừa Fork, chọn mục **Settings** > **Secrets and variables** > **Actions**.

**Bước 3:** Bấm **New repository secret** và lần lượt tạo 3 biến môi trường với tên chính xác như sau:
* `TELEGRAM_TOKEN` (Giá trị: Token bot của bạn)
* `GEMINI_API_KEY` (Giá trị: Key Google AI của bạn)
* `CHAT_ID` (Giá trị: Dãy số ID Telegram)

**Bước 4:** Đừng quên gửi lệnh `/start` cho con bot trên Telegram để cho phép nó gửi tin nhắn cho bạn.

**Bước 5:** Bật GitHub Actions bằng cách chuyển sang tab **Actions** > Chọn **Financial News Bot** > Bấm **Run workflow** để kích hoạt chạy thử lần đầu. Sau đó, bot sẽ tự động chạy theo lịch trình (2 tiếng/lần).

## ⚙️ Tùy chỉnh (Cá nhân hóa Bot)

Bạn có thể chỉnh sửa file `bot_news_cron.py` để bot phục vụ đúng nhu cầu của mình:
* **Thêm/Sửa từ khóa:** Tìm biến `WATCH_KEYWORDS` và thêm các từ khóa bạn quan tâm (ví dụ: `"vnindex"`, `"fdi"`, `"thuế"`...).
* **Đổi lịch chạy:** Mở file `bot.yml` và sửa dòng `cron: '0 */2 * * *'` (Mặc định: 2 tiếng 1 lần).
* **Thêm nguồn báo (RSS):** Cập nhật thêm các link RSS vào biến `RSS_SOURCES`.

## ⚠️ Khuyến cáo rủi ro
*Mọi phân tích, nhận định xu hướng Vàng/Cổ phiếu từ Bot AI chỉ mang tính chất tham khảo thông tin nhanh. Không được xem đây là lời khuyên đầu tư tài chính. Bạn tự chịu trách nhiệm với các quyết định giao dịch của mình.*
