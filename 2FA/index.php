<?php
session_start();

$page = $_GET['page'] ?? 'login';

// --- RESET LAB ---
if ($page == 'logout') {
    session_destroy();
    header("Location: index.php?page=login");
    exit;
}

// --- HANDLE POST ---
if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    // STEP 1: LOGIN
    if ($page == 'login') {
        $username = $_POST['username'];
        $password = $_POST['password'];

        if ($password === '123') {
            // ✅ Đánh dấu đã qua bước 1
            $_SESSION['pre_2fa_user'] = $username;

            header("Location: index.php?page=login2");
            exit;
        } else {
            $error = "Sai mật khẩu (Thử lại với 123)";
        }
    }

    // STEP 2: OTP
    if ($page == 'login2') {

        if (!isset($_SESSION['pre_2fa_user'])) {
            header("Location: index.php?page=login");
            exit;
        }

        if ($_POST['otp'] === '0000') {
            // ✅ Đánh dấu đã xác thực
            $_SESSION['authenticated_user'] = $_SESSION['pre_2fa_user'];

            // ✅ Redirect có id trên URL
            header("Location: index.php?page=account&id=" . $_SESSION['authenticated_user']);
            exit;
        } else {
            $error = "Mã OTP sai!";
        }
    }
}

// --- ACCESS CONTROL (CỐ TÌNH SAI → BYPASS 2FA) ---
// ❗ BUG: chỉ cần pre_2fa_user là vào được account
if ($page == 'login2' || $page == 'account') {
    if (!isset($_SESSION['pre_2fa_user'])) {
        header("Location: index.php?page=login");
        exit;
    }
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>2FA Bypass Lab - <?php echo ucfirst($page); ?></title>
    <style>
        body { font-family: sans-serif; padding: 20px; line-height: 1.5; }
        .container { max-width: 400px; margin: auto; border: 1px solid #ccc; padding: 20px; border-radius: 8px;}
        input { display: block; width: 90%; margin-bottom: 10px; padding: 8px; }
        button { padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; width: 95%;}
    </style>
</head>
<body>
<div class="container">

<?php if ($page == 'login'): ?>

    <h1>Login - Step 1</h1>
    <?php if(isset($error)) echo "<p style='color:red'>$error</p>"; ?>
    <form method="POST" action="index.php?page=login">
        <label>Username</label>
        <input type="text" name="username" required>

        <label>Password (Mặc định: 123)</label>
        <input type="password" name="password" required>

        <button type="submit">Log in</button>
    </form>

<?php elseif ($page == 'login2'): ?>

    <h1>Xác thực 2FA</h1>
    <p>Email xác thực đã được gửi cho:
        <b><?php echo htmlspecialchars($_SESSION['pre_2fa_user']); ?></b>
    </p>

    <?php if(isset($error)) echo "<p style='color:red'>$error</p>"; ?>

    <form method="POST" action="index.php?page=login2">
        <label>Mã xác thực 4 số (OTP)</label>
        <input type="text" name="otp" required>
        <button type="submit">Submit</button>
    </form>

<?php elseif ($page == 'account'): ?>

    <?php
        $session_user = $_SESSION['pre_2fa_user'];
        $url_id = $_GET['id'] ?? '';

        // 🔒 Nếu sửa id khác với session → đá về login
        if ($url_id && $url_id !== $session_user) {
            session_destroy(); // optional: reset luôn
            header("Location: index.php?page=login");
            exit;
        }

        // ❗ Không dùng id để xác thực
        $display_user = $session_user;
    ?>

    <header>
        <h1>Trang cá nhân của:
            <span style="color: green;">
                <?php echo htmlspecialchars($display_user); ?>
            </span>
        </h1>
    </header>

    <section>
        <div style="background: #f4f4f4; padding: 10px; border-left: 4px solid #007bff;">
            <p><b>Email:</b> <?php echo htmlspecialchars($display_user); ?>@portswigger.net</p>
        </div>

        <?php if ($url_id): ?>
            <p style="color: gray;">(URL id = <?php echo htmlspecialchars($url_id); ?>)</p>
        <?php endif; ?>

        <br>

        <a href="index.php?page=logout" style="color: red; font-weight: bold;">
            Đăng xuất (Reset Lab)
        </a>
    </section>

<?php else: ?>

    <h1>404 Not Found</h1>

<?php endif; ?>

</div>
</body>
</html>