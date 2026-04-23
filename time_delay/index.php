<?php
// 1. Tự động tạo cookie khi người dùng truy cập hoặc gửi form
// Trong thực tế, cookie này thường được set sau khi server xử lý một hành động nào đó.
if (!isset($_COOKIE['TrackingId'])) {
    setcookie('TrackingId', 'tester_id_' . uniqid(), time() + 3600, "/");
}

// 2. Cấu hình kết nối tới PostgreSQL
$host = "127.0.0.1";
$port = "5432";
$dbname = "time_delays";
$user = "postgres"; 
$password = "1";

$db = pg_connect("host=$host port=$port dbname=$dbname user=$user password=$password");

if (!$db) {
    die("Internal Server Error: Không thể kết nối Database");
}

// 3. Xử lý logic SQL Injection thông qua Cookie
$trackingId = $_COOKIE['TrackingId'] ?? '';

if ($trackingId) {
    // LỖ HỔNG: Nối chuỗi trực tiếp từ dữ liệu người dùng kiểm soát (Cookie)
    $sql = "SELECT username FROM users WHERE username = '$trackingId'";
    
    // Nếu SQL chứa pg_sleep(5), trang web sẽ bị treo 5 giây trước khi phản hồi
    pg_query($db, $sql);
}

// 4. Xử lý thao tác Đăng nhập (Chỉ để tạo Request POST cho Burp Suite)
$login_message = "";
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Không quan tâm đúng sai, chỉ cần thực hiện để tạo traffic
    $login_message = "Hệ thống đang xử lý đăng nhập cho: " . htmlspecialchars($_POST['username'] ?? '');
}
?>

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Security Lab - Login Page</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 350px; text-align: center; }
        h1 { color: #333; font-size: 24px; margin-bottom: 20px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #007bff; border: none; color: white; border-radius: 6px; cursor: pointer; font-size: 16px; transition: 0.3s; }
        button:hover { background-color: #0056b3; }
        .status { margin-top: 15px; font-size: 14px; color: #666; font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Vulnerable Shop</h1>
        <p>Đăng nhập để tiếp tục</p>
        
        <form method="POST" action="">
            <input type="text" name="username" placeholder="Tên đăng nhập" required>
            <input type="password" name="password" placeholder="Mật khẩu" required>
            <button type="submit">Đăng nhập</button>
        </form>

        <?php if ($login_message): ?>
            <p class="status"><?php echo $login_message; ?></p>
        <?php endif; ?>

    </div>
</body>
</html>