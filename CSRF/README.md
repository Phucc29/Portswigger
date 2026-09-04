## CSRF là gì?

Cross-Site Request Forgery (CSRF), còn được gọi là giả mạo yêu cầu liên trang, là một lỗ hổng bảo mật web cho phép kẻ tấn công khiến người dùng thực hiện những hành động mà họ không chủ ý thực hiện. Nó cho phép kẻ tấn công phần nào vượt qua cơ chế Same-Origin Policy, vốn được thiết kế để ngăn các website khác nhau can thiệp vào nhau.

## Tác động của một cuộc tấn công CSRF là gì?

Trong một cuộc tấn công CSRF thành công, kẻ tấn công khiến người dùng thực hiện một hành động mà họ không hề chủ ý. Ví dụ, hành động đó có thể là thay đổi địa chỉ email, thay đổi mật khẩu hoặc chuyển tiền.

Tùy thuộc vào tính chất của hành động, kẻ tấn công có thể chiếm toàn quyền kiểm soát tài khoản của người dùng. Nếu người dùng bị tấn công có quyền quản trị trong ứng dụng, kẻ tấn công thậm chí có thể kiểm soát toàn bộ dữ liệu và chức năng của ứng dụng.

## CSRF hoạt động thế nào?

Để một cuộc tấn công CSRF có thể xảy ra, cần có 3 điều kiện chính:
- Có một hành động phù hợp: Ứng dụng có một chức năng mà kẻ tấn công muốn khiến nạn nhân thực hiện. Đây có thể là hành động có quyền cao, chẳng hạn thay đổi quyền của người dùng khác, hoặc bất kỳ hành động nào liên quan đến dữ liệu riêng của người dùng, chẳng hạn đổi mật khẩu của chính họ.
- Quản lý phiên dựa trên Cookie: Khi thực hiện hành động, trình duyệt gửi một hoặc nhiều HTTP request và ứng dụng chỉ dựa vào session cookie để xác định người dùng gửi request. Không có cơ chế nào khác để theo dõi phiên hoặc xác thực request.
- Không có tham số request không thể đoán trước: Request thực hiện hành động không chứa tham số nào mà kẻ tấn công không thể biết hoặc đoán được. Ví dụ, nếu muốn đổi mật khẩu mà kẻ tấn công phải biết mật khẩu hiện tại của nạn nhân thì chức năng đó không dễ bị CSRF theo cách này.

VD: Giả sử ứng dụng có chức năng cho phép người dùng thay đổi email tài khoản. Khi người dùng thực hiện, trình duyệt gửi request:

```
POST /email/change HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded
Cookie: session=yvthwsztyeQkAPzeQ5gHgTvlyxHfsAfE

email=wiener@normal-user.com
```

Request này đáp ứng đủ điều kiện để thực hiện CSRF:
- Đổi email là hành động có lợi cho kẻ tấn công. Sau khi email bị thay đổi, kẻ tấn công có thể kích hoạt chức năng reset mật khẩu và chiếm tài khoản.
- Ứng dụng sử dụng session cookie để xác định người gửi request. Không có token hoặc cơ chế khác để xác thực request.
- Kẻ tấn công biết được các tham số cần thiết, ở đây chỉ cần biết giá trị của email.

Kẻ tấn công có thể tạo một trang HTML như sau:

```
<html>
<body>
    <form action="https://vulnerable-website.com/email/change" method="POST">
        <input type="hidden" name="email" value="pwned@evil-user.net" />
    </form>

    <script>
        document.forms[0].submit();
    </script>
</body>
</html>
```

Ý nghĩa:
- `<form>` tạo một request POST tới chức năng đổi email.
- email được đặt thành email của kẻ tấn công.
- JavaScript submit() tự động gửi form mà nạn nhân không cần bấm nút.

Khi nạn nhân truy cập trang độc hại, sẽ xảy ra:
- Trang của kẻ tấn công kích hoạt HTTP request tới website dễ bị CSRF.
- Nếu nạn nhân đang đăng nhập vào website đó, trình duyệt sẽ tự động gửi session cookie của nạn nhân kèm request (giả sử Cookie không sử dụng cơ chế SameSite để chống CSRF).
- Website nhận request và tin rằng request được gửi bởi chính nạn nhân, sau đó thay đổi email tài khoản thành: `pwned@evil-user.net`

## Cách tạo một cuộc tấn công CSRF

Việc tự tạo thủ công HTML cần thiết cho một khai thác CSRF có thể khá mất công, đặc biệt khi request cần gửi có nhiều tham số hoặc có những đặc điểm đặc biệt trong request. Cách dễ nhất để tạo CSRF exploit là sử dụng CSRF PoC Generator được tích hợp trong Burp Suite Professional:
- Trong Burp Suite Professional, chọn một request muốn kiểm tra hoặc khai thác.
- Nhấp chuột phải vào request → chọn: Engagement tools → Generate CSRF PoC.
- Burp Suite sẽ tự động tạo HTML có khả năng gửi request đã chọn (trừ Cookie, vì Cookie sẽ được trình duyệt của nạn nhân tự động thêm vào).
- Có thể điều chỉnh các tùy chọn trong CSRF PoC Generator để tinh chỉnh cách thức tấn công. Điều này có thể cần thiết trong một số trường hợp đặc biệt khi request có những đặc điểm bất thường.
- Copy HTML được tạo vào một trang web, sau đó mở trang đó bằng trình duyệt đang đăng nhập vào website dễ bị tấn công và kiểm tra xem request có được gửi thành công hay không, đồng thời hành động mong muốn có xảy ra hay không.

Lab 1: CSRF vulnerability with no defenses

![alt text](image.png)

