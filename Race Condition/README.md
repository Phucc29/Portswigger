## Race Condition

Race condition là một loại lỗ hổng bảo mật phổ biến, có liên quan chặt chẽ đến business logic flaws

Xảy ra khi một website xử lý nhiều request đồng thời nhưng không có các cơ chế bảo vệ thích hợp để đảm bảo dữ liệu được xử lý an toàn.

Khi đó, nhiều luồng thực thi khác nhau có thể cùng lúc tương tác với cùng một dữ liệu, dẫn đến hiện tượng va chạm. Sự va chạm này khiến ứng dụng hoạt động không đúng như mong đợi và tạo ra các hành vi ngoài ý muốn

Một cuộc tấn công Race Condition là việc kẻ tấn công gửi các request được canh thời gian rất chính xác nhằm cố tình tạo ra những va chạm này, từ đó khai thác hành vi bất thường

Khoảng thời gian mà trong đó hiện tượng va chạm có thể xảy ra được gọi là "race window"

Ví dụ, race window có thể chỉ kéo dài một phần nghìn hoặc một phần triệu giây, chẳng hạn như khoảng thời gian giữa hai lần ứng dụng tương tác với cơ sở dữ liệu. Trong khoảng thời gian rất ngắn này, nếu nhiều request cùng truy cập hoặc thay đổi dữ liệu, race condition có thể xảy ra.

### Race Condition kiểu vượt quá giới hạn

Cho phép kẻ tấn công vượt qua một giới hạn nào đó được áp đặt bởi logic nghiệp vụ của ứng dụng

Nói cách khác, ứng dụng đặt ra một quy tắc như:
- Chỉ được dùng mã giảm giá 1 lần.
- Chỉ được đổi quà 1 lần.
- Chỉ được rút tiền tối đa 100 triệu/ngày.
- Chỉ được đăng ký 1 tài khoản bằng một email.

Tuy nhiên, bằng cách gửi nhiều request cùng lúc, kẻ tấn công có thể khiến ứng dụng không kịp cập nhật trạng thái, từ đó vượt qua giới hạn này.

Có rất nhiều biến thể của kiểu tấn công này, bao gồm:
- Đổi cùng một thẻ quà tặng nhiều lần.
- Đánh giá cùng một sản phẩm nhiều lần, mặc dù mỗi tài khoản chỉ được đánh giá một lần.
- Rút hoặc chuyển tiền vượt quá số dư thực tế trong tài khoản.
- Tái sử dụng một mã CAPTCHA duy nhất nhiều lần, mặc dù CAPTCHA chỉ nên có hiệu lực cho một request.
- Vượt qua cơ chế giới hạn tốc độ được thiết kế để chống tấn công brute-force.

Limit overrun là một dạng con của nhóm lỗ hổng được gọi là Time-of-Check to Time-of-Use (TOCTOU).

### Phát hiện và khai thác Limit Overrun Race Condition bằng Burp Repeater

Quá trình phát hiện và khai thác các Limit Overrun Race Condition tương đối đơn giản.

Ở mức tổng quát, chỉ cần thực hiện hai bước:
1. Xác định một endpoint chỉ được phép sử dụng một lần hoặc bị giới hạn số lần thực hiện, đồng thời endpoint này phải có ý nghĩa về mặt bảo mật hoặc mang lại một lợi ích nào đó nếu khai thác thành công.
2. Gửi nhiều request đến endpoint đó trong khoảng thời gian cực ngắn, để kiểm tra xem liệu bạn có thể vượt qua giới hạn mà ứng dụng đặt ra hay không

Thách thức

Khó khăn lớn nhất nằm ở việc canh thời gian của các request.

Mục tiêu là làm sao để ít nhất hai race window trùng lên nhau, từ đó tạo ra một va chạm trong quá trình xử lý của máy chủ

Ngay cả khi bạn cố gắng gửi tất cả các request cùng một thời điểm, trên thực tế vẫn tồn tại rất nhiều yếu tố bên ngoài mà bạn không thể kiểm soát hoặc dự đoán được.

Do đó, dù các request được gửi gần như đồng thời từ phía client, chúng không nhất thiết sẽ được server nhận và xử lý cùng lúc.

Burp sẽ tự động lựa chọn kỹ thuật phù hợp dựa trên phiên bản HTTP mà máy chủ hỗ trợ:
- Đối với HTTP/1, Burp sử dụng kỹ thuật truyền thống gọi là last-byte synchronization.
- Đối với HTTP/2, Burp sử dụng kỹ thuật single-packet attack

Kỹ thuật single-packet attack cho phép loại bỏ gần như hoàn toàn ảnh hưởng của network jitter bằng cách sử dụng một gói tin TCP duy nhất để hoàn thành 20–30 request gần như đồng thời.

Lab 1: Limit overrun race conditions

![alt text](image.png)

Đăng nhập vào tài khoản wiener, sau đó thực hiện thêm gift code ta thấy api áp gift code là `/cart/coupon`, đoán race condition diễn ra ở đây. Gửi nhiều request này tới Repeater

![alt text](image-1.png)

Sử dụng Custom actions để gửi nhiều request đi cùng lúc. Sử dụng trigger race condition

![alt text](image-2.png)

Sau đó play và ta thành công sử dụng nhiều mã giảm giá

![alt text](image-3.png)

Tiến hành play trigger race condition rồi lại gỡ mã giảm giá cho đến khi mã giảm giá giảm số lượng tiền xuống mức mua được

![alt text](image-4.png)

### Phát hiện và khai thác các race condition vượt quá giới hạn bằng Turbo Intruder


Turbo Intruder yêu cầu người dùng có một số kiến thức về Python, nhưng lại rất phù hợp để thực hiện các cuộc tấn công phức tạp hơn, chẳng hạn như:
- Cần thử lại nhiều lần.
- Cần gửi các request với thời điểm lệch nhau
- Cần gửi một số lượng request cực lớn

Để sử dụng kỹ thuật single-packet attack trong Turbo Intruder:
1. Đảm bảo máy chủ mục tiêu hỗ trợ HTTP/2, kỹ thuật single-packet attack không tương thích với HTTP/1.
2. Thiết lập các tùy chọn cấu hình cho Request Engine như sau:
    - engine = Engine.BURP2
    - concurrentConnections = 1
3. Khi đưa các request vào hàng đợi, hãy nhóm chúng lại bằng cách gán cùng một "gate" thông qua tham số gate của phương thức engine.queue()
4. Để gửi đồng thời tất cả các request trong một nhóm, hãy mở gate tương ứng bằng phương thức engine.openGate()

```
def queueRequests(target, wordlists):
    # Khởi tạo Request Engine
    engine = RequestEngine(
        endpoint=target.endpoint,
        concurrentConnections=1,   # Chỉ sử dụng một kết nối HTTP/2
        # Sử dụng engine BURP2 để hỗ trợ single-packet attack
        engine=Engine.BURP2        
    )

    # Đưa 20 request vào hàng đợi thuộc gate có tên '1'
    for i in range(20):
        engine.queue(target.req, gate='1')

    # Mở gate '1' để gửi đồng thời toàn bộ 20 request
    engine.openGate('1')
```

Lab 2: Bypassing rate limits via race conditions

![alt text](image-5.png)

Từ đề bài ta đoán lỗ hổng nằm ở mật khẩu. Đăng nhập bằng carlos với mật khẩu sai và gửi tới Burp Turbo Intruder

![alt text](image-6.png)

Đổi nội dung payload và copy list mật khẩu sau đó bấm attack

![alt text](image-7.png)

Ta thấy có payload `mustang` với status là 302 ta đoán đây là mật khẩu. Thử đăng nhập để kiểm tra.

![alt text](image-8.png)

### Phương pháp

Để phát hiện và khai thác các chuỗi nhiều bước bị ẩn, khuyến nghị sử dụng phương pháp dưới đây

`Dự đoán -> Thăm dò -> Chứng minh`

#### Dự đoán các va chạm tiềm năng

Việc kiểm thử mọi endpoint là không thực tế. Sau khi đã lập bản đồ website mục tiêu như bình thường, bạn có thể giảm số lượng endpoint cần kiểm thử bằng cách tự đặt ra các câu hỏi sau:
- Endpoint này có quan trọng về mặt bảo mật không?
- Endpoint này có khả năng xảy ra va chạm không? Để xảy ra một va chạm thành công, thông thường bạn cần hai hoặc nhiều request cùng kích hoạt các thao tác trên cùng một bản ghi.

#### Thăm dò để tìm manh mối

Để nhận ra các dấu hiệu bất thường, trước tiên cần xác định cách endpoint hoạt động trong điều kiện bình thường.

Có thể thực hiện việc này trong Burp Repeater bằng cách nhóm tất cả các request lại và sử dụng tùy chọn: `Send group in sequence`

Tiếp theo, hãy gửi chính nhóm request đó đồng thời bằng kỹ thuật single-packet attack (hoặc last-byte sync nếu máy chủ không hỗ trợ HTTP/2) nhằm giảm thiểu ảnh hưởng của network jitter (độ trễ dao động trên mạng).

Trong Burp Repeater, bạn có thể thực hiện bằng cách chọn: `Send group in parallel`

Ngoài ra, cũng có thể sử dụng tiện ích mở rộng Turbo Intruder

Bất kỳ điều gì cũng có thể là một manh mối. Điều này bao gồm:
- sự thay đổi ở một hoặc nhiều response,
- nhưng đừng quên các second-order effects (tác động gián tiếp xuất hiện sau đó), chẳng hạn như:
    - nội dung email được gửi đi khác bình thường,
    - hành vi của ứng dụng thay đổi rõ rệt sau khi các request được xử lý.

#### Chứng minh ý tưởng

Hãy cố gắng hiểu chính xác những gì đang xảy ra. Sau đó:
- Loại bỏ những request không cần thiết
- Kiểm tra xem bạn vẫn có thể tái tạo được hiệu ứng đó hay không.

Các race condition nâng cao có thể tạo ra những primitive (khả năng khai thác cơ bản) rất đặc biệt và khác thường. Vì vậy, con đường để đạt được mức ảnh hưởng lớn nhất thường không phải lúc nào cũng rõ ràng ngay từ đầu.

### Race condition giữa nhiều endpoint

Có lẽ dạng race condition dễ hình dung nhất là những race condition xảy ra khi gửi đồng thời các request tới nhiều endpoint khác nhau. Hãy nghĩ đến lỗi logic kinh điển trên các cửa hàng trực tuyến: Bạn thêm một món hàng vào giỏ hàng, thanh toán cho món hàng đó, sau đó thêm nhiều món khác vào giỏ trước khi truy cập trực tiếp đến trang xác nhận đơn hàng.

Một biến thể của lỗ hổng này có thể xảy ra khi việc xác thực thanh toán và xác nhận đơn hàng đều được thực hiện trong quá trình xử lý của cùng một request.

Trong trường hợp này, bạn có thể thêm nhiều sản phẩm hơn vào giỏ hàng trong khoảng thời gian race window — tức là khoảng thời gian sau khi hệ thống đã xác thực việc thanh toán nhưng trước khi đơn hàng được xác nhận hoàn toàn.

#### Căn chỉnh các race window giữa nhiều endpoint