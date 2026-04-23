<?php
session_start();

// 1. Kiểm tra xem đã qua bước đăng nhập 1 chưa
if (!isset($_SESSION['temp_user'])) {
    header("Location: login.php");
    exit;
}

// 2. Lấy ID từ URL (nếu có)
$get_id = $_GET['id'] ?? null;

// 3. KIỂM TRA BẢO MẬT: 
// Nếu người dùng nhập ID trên URL mà ID đó KHÁC với tên đã lưu trong Session
if ($get_id !== null && $get_id !== $_SESSION['temp_user']) {
    // Hủy phiên làm việc (xóa hết thẻ tên tạm) để bắt login lại từ đầu
    session_destroy(); 
    header("Location: login.php");
    exit;
}

// Nếu mọi thứ hợp lệ, gán vào biến để hiển thị
$display_user = $_SESSION['temp_user'];
?>
<!DOCTYPE html>
<html>
<head><title>My Account</title></head>
<body>
    <header>
        <h1>Trang cá nhân của: <?php echo htmlspecialchars($display_user); ?></h1>
    </header>
    <section>
        <div>
            <p>Email của bạn: <?php echo htmlspecialchars($display_user); ?>@portswigger.net</p>
            <p style="color: blue;">Mức độ bảo mật: 2FA đang được bật.</p>
        </div>
        <br>
        <a href="login.php" style="color: red;">Đăng xuất (Reset Lab)</a>
    </section>
</body>
</html>