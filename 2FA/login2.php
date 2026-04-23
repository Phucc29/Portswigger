<?php
session_start();
if (!isset($_SESSION['temp_user'])) { header("Location: login.php"); exit; }

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if ($_POST['otp'] === '0000') {
        $_SESSION['authenticated_user'] = $_SESSION['temp_user']; 
        header("Location: account.php?id=" . $_SESSION['authenticated_user']);
        exit;
    } else {
        $error = "Mã OTP sai!";
    }
}
?>
<!DOCTYPE html>
<html>
<head><title>2FA Verification</title></head>
<body>
    <section>
        <h1>Xác thực 2FA</h1>
        <p>Email xác thực đã được gửi cho: <b><?php echo $_SESSION['temp_user']; ?></b></p>
        <form method="POST" action="login2.php">
            <label>Mã xác thực</label>
            <input type="text" name="otp" required>
            <button type="submit" class="button">Submit</button>
        </form>
    </section>
</body>
</html>