# File Upload Vulnerabilities

## 1. File Upload Vulnerabilities là gì?

Lỗ hổng file upload xảy ra khi máy chủ cho phép người dùng tải tệp lên nhưng không kiểm tra đủ chặt chẽ hoặc kiểm tra sai cách.

Các thuộc tính cần kiểm tra thường gồm:

- Tên file
- Phần mở rộng
- Loại file / MIME type
- Nội dung thực tế của file
- Kích thước file

Hậu quả có thể là:

- Upload được file độc hại
- Ghi đè file quan trọng
- Làm đầy dung lượng lưu trữ để gây DoS
- Upload web shell để dẫn tới RCE

## 2. Vì sao file upload nguy hiểm?

Mức độ ảnh hưởng phụ thuộc vào hai câu hỏi chính:

- Website kiểm tra những gì của file
- Sau khi upload, server có cho phép file đó được thực thi hay không

Trường hợp nghiêm trọng nhất là:

- Server không kiểm tra loại file
- Cho phép thực thi các file như `.php`, `.jsp`, `.aspx`
- Kẻ tấn công upload web shell và chiếm quyền thực thi trên máy chủ

Nếu không kiểm tra tên file, kẻ tấn công có thể:

- Ghi đè file hiện có
- Kết hợp với path traversal để ghi file ra ngoài thư mục dự kiến

Nếu không giới hạn kích thước, kẻ tấn công có thể:

- Upload file rất lớn
- Upload hàng loạt file
- Làm cạn tài nguyên lưu trữ

## 3. Nguyên nhân thường gặp

Các cơ chế kiểm tra file upload thường bị lỗi vì:

- Blacklist không đầy đủ hoặc xử lý sai phần mở rộng
- Tin tưởng dữ liệu do client gửi lên, nhất là `Content-Type`
- Validation không nhất quán giữa các thư mục hoặc backend khác nhau

## 4. Web server xử lý file tĩnh như thế nào?

Trước đây, website chủ yếu là file tĩnh nên URL thường ánh xạ trực tiếp tới file trên hệ thống. Ngày nay website chủ yếu là động, nhưng web server vẫn phải phục vụ file tĩnh như CSS, JS, ảnh, và xử lý chúng theo cơ chế riêng.

Quy trình cơ bản:

1. Server nhận HTTP request
2. Phân tích URL
3. Xác định extension
4. So sánh extension với bảng ánh xạ MIME type
5. Quyết định cách xử lý theo cấu hình server

### 4.1 File không thực thi

Ví dụ: `.jpg`, `.png`, `.gif`, `.css`, `.html`

Server thường:

- Không thực thi mã
- Đọc nội dung file
- Trả nguyên nội dung cho client

### 4.2 File thực thi

Ví dụ: `.php`, `.jsp`, `.py`, `.asp`

Nếu server được cấu hình để chạy loại file đó, nó sẽ:

- Đọc header
- Đọc cookie
- Đọc tham số GET/POST
- Gán dữ liệu vào biến của chương trình
- Thực thi script
- Trả kết quả thực thi cho client

### 4.3 File thực thi nhưng server không hỗ trợ

Nếu server không được cấu hình để chạy loại file đó:

- Có thể trả lỗi 404, 500, hoặc tương tự
- Có trường hợp trả nguyên source code dưới dạng text do cấu hình sai
- Điều này có thể dẫn tới information disclosure

## 5. Content-Type và multipart/form-data

Khi submit form thông thường, trình duyệt hay dùng:

- `Content-Type: application/x-www-form-urlencoded`

Khi upload file, trình duyệt thường dùng:

- `Content-Type: multipart/form-data`

Trong multipart request, body được chia thành nhiều part riêng biệt. Mỗi input của form sẽ là một part.

Ví dụ một part upload file thường có:

- `Content-Disposition`
- Tên field
- `filename`
- `Content-Type`

`Content-Disposition` cho server biết:

- Đây là field nào
- File được đặt tên gì
- Nó thuộc input nào

Điểm yếu thường gặp là server tin hoàn toàn vào `Content-Type` do client gửi lên. Đây là giá trị có thể bị sửa bằng Burp Suite hoặc bất kỳ proxy nào.

Biện pháp kiểm tra tốt hơn nên gồm:

- Kiểm tra extension
- Kiểm tra MIME type thực tế
- Kiểm tra magic bytes / file signature
- Kiểm tra nội dung file
- Đổi tên file khi lưu
- Không cho thực thi file đã upload

## 6. Khai thác bằng web shell

Web shell là một script độc hại chạy trên web server và cho phép thực thi lệnh từ xa thông qua HTTP request.

Nếu website cho phép upload file thực thi và server cũng cho phép chạy chúng, kẻ tấn công có thể:

- Đọc file tùy ý
- Ghi hoặc sửa file
- Đánh cắp dữ liệu
- Upload thêm mã độc
- Thực thi lệnh hệ điều hành
- Pivot sang các máy khác trong mạng nội bộ

Ví dụ web shell PHP:

```php
<?php
echo file_get_contents('/path/to/target/file');
?>
```

Script này đọc nội dung file trên server và trả kết quả qua response.

Một web shell linh hoạt hơn:

```php
<?php echo system($_GET['command']); ?>
```

Khi đó có thể gọi như:

```http
GET /example/exploit.php?command=id HTTP/1.1
```

## 7. Cách server bảo vệ thư mục upload

Một lớp phòng thủ quan trọng là không cho phép server thực thi file do người dùng upload, đặc biệt trong các thư mục public.

Nếu file không được phép thực thi, server sẽ:

- Trả lỗi
- Hoặc trả file dưới dạng plain text

Lưu ý rằng cấu hình thực thi có thể khác nhau giữa các thư mục. Thư mục upload thường chỉ để lưu file người dùng và không cho chạy script, trong khi các thư mục ứng dụng có thể cho phép thực thi.

Nếu kẻ tấn công tìm được cách ghi file vào thư mục cho phép thực thi, web shell vẫn có thể chạy và dẫn tới RCE.

Trong multipart/form-data, trường `filename=` đôi khi còn ảnh hưởng tới cách server lưu file trên đĩa, nên cần đặc biệt chú ý khi kiểm tra và khi pentest.

Reverse proxy cũng có thể khiến cùng một request đi tới các backend khác nhau với hành vi khác nhau, tạo ra sự không nhất quán có thể khai thác được.

## 8. Kỹ thuật bypass thường gặp

### 8.1 Flawed file type validation

Đây là nhóm lỗi khi server chỉ kiểm tra một thuộc tính dễ giả mạo, đặc biệt là `Content-Type`.

### 8.2 Path traversal khi lưu file

Nếu giá trị tên file hoặc đường dẫn lưu file không được xử lý an toàn, kẻ tấn công có thể ghi file ra ngoài thư mục upload dự kiến.

### 8.3 Blacklist không đủ mạnh

Chặn một vài extension nguy hiểm không có nghĩa là an toàn. Một số server vẫn thực thi các biến thể khác như `.php5`.

### 8.4 Tải lên file cấu hình

Nếu website cho phép upload `.htaccess` hoặc `web.config`, kẻ tấn công có thể thay đổi cách server xử lý file trong thư mục đó.

Ví dụ với Apache:

```apache
AddType application/x-httpd-php .abc
```

Lúc này file `.abc` có thể bị xử lý như PHP.

### 8.5 Làm rối phần mở rộng

Các kỹ thuật phổ biến gồm:

- Thay đổi chữ hoa/chữ thường
- Dùng nhiều extension
- Thêm dấu chấm hoặc khoảng trắng ở cuối
- URL encode hoặc double URL encode
- Chèn `;` hoặc null byte `%00`
- Dùng Unicode đa byte
- Tận dụng cơ chế xóa extension lỗi

## 9. Các lab đã làm

### Lab 1: Remote code execution via web shell upload

![Lab 1](images/image.png)

Upload file PHP chứa web shell:

![Web shell PHP](images/image-1.png)

Khi bắt request upload thành công, secret được phản hồi:

![Secret phản hồi](images/image-2.png)

Nộp secret và hoàn thành lab:

![Hoàn thành lab 1](images/image-3.png)

### Lab 2: Web shell upload via Content-Type restriction bypass

![Lab 2](images/image-4.png)

Ban đầu server từ chối vì sai `Content-Type`:

![Từ chối upload](images/image-5.png)

Sửa `Content-Type` trong request:

![Sửa Content-Type](images/image-6.png)

Sau đó upload thành công web shell và đọc được `/home/carlos/secret`:

![Đọc secret](images/image-7.png)

Hoàn thành lab:

![Hoàn thành lab 2](images/image-8.png)

### Lab 3: Web shell upload via path traversal

![Lab 3](images/image-9.png)

Upload file và bắt request sau khi upload thành công:

![Request upload](images/image-10.png)

Sửa đường dẫn để file được lưu thành `/files/a.php`:

![Path traversal](images/image-11.png)

Nộp secret và hoàn thành lab:

![Hoàn thành lab 3](images/image-12.png)

### Lab 4: Web shell upload via extension blacklist bypass

![Lab 4](images/image-13.png)

Upload file text để kiểm tra cơ chế xác thực:

![Upload text](images/image-14.png)

Tạo file `.htaccess` với nội dung:

```apache
AddType application/x-httpd-php .abc
```

![Tạo htaccess](images/image-15.png)

Đổi đuôi file web shell thành `.abc`:

![Đổi extension](images/image-16.png)

Upload thành công và lấy secret:

![Upload thành công](images/image-17.png)

Hoàn thành lab:

![Hoàn thành lab 4](images/image-18.png)

### Lab 5: Web shell upload via obfuscated file extension

![Lab 5](images/image-19.png)

Server chỉ cho phép upload file có đuôi hợp lệ như `.jpg` hoặc `.png`.

Ta có thể đổi đuôi `php` sang một dạng obfuscate như `%00.jpg` để bypass bộ lọc trong một số cấu hình cũ:

![Đổi đuôi](images/image-20.png)

Upload file thành công và kiểm tra secret:

![Upload thành công](images/image-21.png)

Submit secret để solve bài lab:

![Hoàn thành lab 5](images/image-22.png)

### Lab 6: Remote code execution via polyglot web shell upload

Server kiểm tra nội dung file thay vì chỉ nhìn extension hay `Content-Type`:

![Lab 6](images/image-24.png)

Upload file không hợp lệ sẽ bị từ chối:

![Từ chối upload](images/image-25.png)

Sử dụng `exiftool` để tạo polyglot file từ ảnh `.jpg` và chèn payload PHP vào metadata comment:

![Tạo polyglot](images/image-26.png)

Upload file polyglot thành công:

![Upload polyglot](images/image-27.png)

Tìm secret và submit để hoàn thành lab:

![Hoàn thành lab 6](images/image-28.png)

## 10. Kiểm tra nội dung file

Không tin `Content-Type` trong request.

- Server có thể kiểm tra nội dung thực tế của file để xác định loại file
- Với ảnh, có thể kiểm tra kích thước hoặc thuộc tính đặc trưng
- File không khớp với định dạng mong đợi sẽ bị từ chối

### Magic bytes

Mỗi định dạng file thường có chuỗi byte đặc trưng ở đầu hoặc cuối file.

- JPEG thường bắt đầu bằng `FF D8 FF`
- Nếu chữ ký không đúng, server có thể từ chối upload

Kỹ thuật này vẫn có thể bị bypass bằng polyglot file. Công cụ như `ExifTool` có thể nhúng payload vào metadata để tạo file vừa hợp lệ về mặt định dạng, vừa chứa mã độc.

## 11. Khai thác race condition trong upload file

Framework hiện đại thường an toàn hơn vì:

- Upload file vào thư mục tạm
- Đổi tên ngẫu nhiên
- Kiểm tra hợp lệ rồi mới chuyển sang thư mục chính

Lỗi thường xuất hiện khi lập trình viên tự xử lý upload:

- File được lưu ngay vào thư mục chính
- Sau đó mới quét hoặc kiểm tra
- Nếu không hợp lệ thì mới xóa

Trong khoảng thời gian rất ngắn trước khi file bị xóa, kẻ tấn công có thể truy cập hoặc kích hoạt file đó.

Race condition thường khó phát hiện bằng black-box testing và dễ bị bỏ sót nếu không xem được mã nguồn hoặc không có dấu hiệu rõ ràng từ hành vi hệ thống.

## 12. Ghi nhớ nhanh

- Không tin vào `Content-Type` do client gửi lên
- Không chỉ dùng blacklist để chặn extension
- Luôn kiểm tra nội dung file và magic bytes
- Không cho thực thi file upload trong thư mục public
- Cẩn thận với path traversal và cấu hình theo thư mục
- Khi pentest, luôn thử khác biệt giữa frontend, reverse proxy và backend
