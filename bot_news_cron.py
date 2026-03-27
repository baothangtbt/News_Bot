import os
import time
import requests
import feedparser
import json
from datetime import datetime

# ================= CẤU HÌNH TỪ GITHUB SECRETS =================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

WATCH_KEYWORDS = [
    "bitcoin", "giá vàng", "chiến tranh", "thương mại", 
    "chứng khoán", "fed", "lãi suất", "lạm phát", "dầu mỏ", "ngân hàng",
    "bất động sản", "nhà ở", "sắt thép", "đầu tư công", "xuất khẩu", "tỷ giá",
    "vnindex", "vn-index", "cổ phiếu", "trái phiếu", "krx", "tiền ảo", 
    "crypto", "ngoại tệ", "fdi", "thuế", "chính phủ", "Israel", "Iran"
]

RSS_SOURCES = {
    "VnEx_KinhDoanh": "https://vnexpress.net/rss/kinh-doanh.rss",
    "CafeF_TaiChinh": "https://cafef.vn/tai-chinh-quoc-te.rss",
    "CafeF_ChungKhoan": "https://cafef.vn/thi-truong-chung-khoan.rss",
    "CafeF_BatDongSan": "https://cafef.vn/bat-dong-san.rss",
    "VnEx_TheGioi": "https://vnexpress.net/rss/the-gioi.rss"
  
}
# ==============================================================

def send_telegram_message(text):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("⚠️ Thiếu cấu hình Telegram.")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"⚠️ Lỗi gửi Telegram: {e}")

def call_gemini_api(prompt):
    models_to_try = [
        "gemini-3-pro-preview",       
        "gemini-3-flash-preview",     
        "gemini-2.5-pro",             
        "gemini-2.5-flash",           
        "gemini-1.5-flash-002"        
    ]
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1000
        }
    }

    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
        try:
            current_timeout = 25 if "pro" in model_name else 15
            response = requests.post(url, headers=headers, json=payload, timeout=current_timeout)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return result['candidates'][0]['content']['parts'][0]['text']
            elif response.status_code in [404, 429]:
                continue
        except Exception:
            continue
    return "⚠️ Lỗi phân tích từ AI."

def ai_analyze(text):
    prompt = (
        f"Tin tức tài chính: {text}\n"
        "Đóng vai chuyên gia Trading (phong cách ngắn gọn, súc tích). Hãy:\n"
        "1. Tóm tắt nội dung chính (1 câu).\n"
        "2. Dự báo xu hướng VÀNG (XAU/USD) & DXY nếu tin này ảnh hưởng.\n"
        "3. Chấm điểm Tác động thị trường (1-10).\n"
        "4. Gợi ý mã cổ phiếu Việt Nam (Ticker) hưởng lợi/bất lợi.\n"
        "TRẢ LỜI ĐÚNG ĐỊNH DẠNG SAU:\n"
        "📝 Tóm tắt: [Nội dung]\n"
        "🟡 Vàng/DXY: [Xu hướng] - [Lý do 3 chữ]\n"
        "🌡️ Tác động: [Điểm]/10\n"
        "🎯 Mã liên quan:\n"
        "[Mã 1] (Lý do)\n"
        "[Mã 2] (Lý do)"
    )
    return call_gemini_api(prompt)

def scan_news():
    print("🚀 Bắt đầu quét tin tức (Cron Job)...")
    # Tính thời gian cutoff: Lấy tin xuất bản trong vòng 130 phút trước
    # Cho dư ra 10 phút so với chu kỳ 120 phút của cron để tránh sót tin
    cutoff_time = time.time() - (420 * 60) 
    
    for source, url in RSS_SOURCES.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                # Kiểm tra thời gian xuất bản
                if hasattr(entry, 'published_parsed'):
                    entry_time = time.mktime(entry.published_parsed)
                    if entry_time < cutoff_time:
                        continue # Bỏ qua tin cũ
                
                title_lower = entry.title.lower()
                for keyword in WATCH_KEYWORDS:
                    if keyword in title_lower:
                        print(f"👉 Tìm thấy tin: {entry.title}")
                        time.sleep(2) # Chống spam API
                        analysis = ai_analyze(entry.title)
                        
                        msg = (
                            f"🚨 <b>TIN NÓNG ({source})</b>\n"
                            f"📰 <b>{entry.title}</b>\n"
                            f"------------------------\n"
                            f"{analysis}\n"
                            f"------------------------\n"
                            f"👉 <a href='{entry.link}'>Xem chi tiết</a>"
                        )
                        send_telegram_message(msg)
                        break # Tìm thấy 1 keyword thì dừng xét keyword khác cho bài này
        except Exception as e:
            print(f"Lỗi quét RSS {source}: {e}")

if __name__ == '__main__':
    scan_news()
    print("✅ Hoàn tất chu kỳ.")
