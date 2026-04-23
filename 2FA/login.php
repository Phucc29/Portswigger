<?php
session_start();
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Giả lập: mật khẩu luôn là '123' cho mọi user
    if ($password === '123') {
        $_SESSION['temp_user'] = $username; // Lưu user đang đăng nhập dở dang
        header("Location: login2.php"); // Tự động chuyển hướng sang bước 2
        exit;
    } else {
        $error = "Sai mật khẩu (Thử lại với 123)";
    }
}
?>
<!DOCTYPE html>
<html>
<head><title>Login - Step 1</title></head>
<body>
    <section>
        <h1>Login</h1>
        <?php if(isset($error)) echo "<p style='color:red'>$error</p>"; ?>
        <form method="POST" action="login.php">
            <label>Username</label>
            <input type="text" name="username" required>
            <label>Password</label>
            <input type="password" name="password" required>
            <button type="submit" class="button">Log in</button>
        </form>
    </section>
</body>
</html>