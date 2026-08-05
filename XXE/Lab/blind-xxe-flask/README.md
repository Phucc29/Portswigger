https://drive.google.com/file/d/1LHY_NvojYEI-y8XBRGF1HlrVkQswiM5f/view?usp=sharing

Thư viện `lxml`:

Là bộ thư viện xử lý và phân tích dữ liệu XML/HTML dành cho Python.

Mối liên hệ với XXE:
- Lỗ hổng XXE xuất phát từ cơ chế phân tích cú pháp XML. `lxml` chính là thành phần thực hiện việc đọc, giải mã và xử lý cú pháp của chuỗi XML mà người dùng gửi lên.
- Trong mã nguồn Flask, cấu hình của `lxml.etree.XMLParser` quyết định ứng dụng có bị lỗ hổng XXE hay không:
    - `resolve_entities=True`: Cho phép parser giải mã các thực thể bên ngoài
    - `no_network=False`: Cho phép parser thực hiện các kết nối mạng ra ngoài

