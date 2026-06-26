File Upload Vulnerabilities là gì?

Xảy ra khi máy chủ web cho phép người dùng tải tệp lên nhưng không kiểm tra hoặc kiểm tra không đầy đủ.

Các yếu tố cần được kiểm tra:
- Tên tệp
- Loại tệp
- Nội dung tệp
- Kích thước tệp

Nguy cơ:
- Kẻ tấn công có thể tải lên bất kỳ tệp nào, kể cả tệp độc hại.
- Có thể tải lên server-side script (ví dụ: .php, .jsp, .aspx) để thực thi mã trên máy chủ (RCE)

Mức độ ảnh hưởng:
- Chỉ cần upload thành công cũng có thể gây hại (ví dụ: làm đầy dung lượng ổ đĩa)
- Hoặc cần gửi thêm một HTTP request để truy cập tệp đã upload, từ đó kích hoạt việc thực thi mã trên server.

Tác động của lỗ hổng File Upload

Mức độ ảnh hưởng phụ thuộc vào 2 yếu tố chính:
- Website kiểm tra những gì của tệp
- Các hạn chế được áp dụng sau khi tệp được upload thành công.

Trường hợp nghiêm trọng nhất:
- Server không kiểm tra loại tệp.
- Cho phép thực thi các file như .php, .jsp
- Kẻ tấn công upload web shell → RCE → chiếm toàn quyền máy chủ.

Nếu không kiểm tra tên tệp:
- Có thể ghi đè các tệp quan trọng bằng cách upload tệp cùng tên.
- Nếu kết hợp với Directory Traversal, có thể upload tệp vào những thư mục ngoài dự kiến.

Nếu không giới hạn kích thước tệp:
- Kẻ tấn công upload các tệp rất lớn hoặc nhiều tệp.
- Làm đầy dung lượng ổ đĩa → DoS.

Nguyên nhân phát sinh lỗ hổng File Upload

Thông thường, lập trình viên có triển khai cơ chế kiểm tra, nhưng thiết kế sai hoặc có thể bị bypass.

Blacklist không đầy đủ hoặc không an toàn.
- Chỉ chặn một số đuôi file nguy hiểm.
- Bỏ sót các đuôi file khác hoặc xử lý sai khi kiểm tra phần mở rộng

Kiểm tra dựa trên thông tin dễ giả mạo.
- Ví dụ: chỉ kiểm tra MIME Type hoặc các thuộc tính trong HTTP request.
- Kẻ tấn công có thể dễ dàng sửa các giá trị này bằng Burp Suite

Validation không nhất quán.
- Các máy chủ hoặc thư mục khác nhau áp dụng quy tắc kiểm tra khác nhau.
- Sự không đồng nhất này tạo ra các điểm yếu có thể bị khai thác.
