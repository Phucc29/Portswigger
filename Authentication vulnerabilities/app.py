# Password brute-force via password change
from flask import Flask, request, redirect, render_template_string, url_for, session

app = Flask(__name__)
# Cấu hình Secret Key để sử dụng Session mã hóa dữ liệu phía Client Cookie
app.secret_key = 'super-secret-key-for-portswigger-lab-simulation'

# Giả lập cơ sở dữ liệu hệ thống
USER_DB = {
    "wiener": "peter",
    "carlos": "nicole"  # Mật khẩu cần brute-force
}

# --- CÁC GIAO DIỆN HTML ---

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Login</h2>
    {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
    <form method="POST" action="/login">
        Username: <input type="text" name="username" required><br><br>
        Password: <input type="password" name="password" required><br><br>
        <button type="submit">Log in</button>
    </form>
</body>
</html>
"""

MY_ACCOUNT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>My Account</title></head>
<body>
    <div style="float: right;">
        <a href="/logout"><button>Log out</button></a>
    </div>
    
    <h2>My Account - {{ username }}</h2>
    <hr>
    <h3>Change Password</h3>
    
    {% if msg %}<p style="color:red; font-weight:bold;">{{ msg }}</p>{% endif %}
    {% if success %}<p style="color:green; font-weight:bold;">{{ success }}</p>{% endif %}
    
    <form method="POST" action="/my-account/change-password">
        <input type="hidden" name="username" value="{{ username }}">
        
        Current password:<br>
        <input type="password" name="current-password" required><br><br>
        
        New password:<br>
        <input type="password" name="new-password-1" required><br><br>
        
        Confirm new password:<br>
        <input type="password" name="new-password-2" required><br><br>
        
        <button type="submit">Change password</button>
    </form>
</body>
</html>
"""

# --- CÁC ROUTE XỬ LÝ ENDPOINT ---

@app.route('/')
def index():
    return redirect(url_for('login'))


# 1. GET /login & POST /login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Nếu đã đăng nhập rồi thì vào thẳng My Account
        if 'username' in session:
            return redirect(url_for('my_account'))
        return render_template_string(LOGIN_TEMPLATE)
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in USER_DB and USER_DB[username] == password:
        # Lưu thông tin đăng nhập vào Session
        session['username'] = username
        return redirect(url_for('my_account', id=username))
    else:
        return render_template_string(LOGIN_TEMPLATE, error="Invalid username or password.")


# 2. GET /logout
@app.route('/logout', methods=['GET'])
def logout():
    # Xóa thông tin session và chuyển hướng về trang login
    session.pop('username', None)
    return redirect(url_for('login'))


# 3. GET /my-account
@app.route('/my-account', methods=['GET'])
def my_account():
    # Kiểm tra quyền truy cập qua Session thay vì tham số id trên URL để an toàn hơn
    if 'username' not in session:
        return redirect(url_for('login'))
        
    username = session['username']
    success = request.args.get('success')
    
    return render_template_string(MY_ACCOUNT_TEMPLATE, username=username, success=success)


# 4. POST /my-account/change-password
@app.route('/my-account/change-password', methods=['POST'])
def change_password():
    # Bảo vệ endpoint: Nếu chưa có session đăng nhập thì không cho đổi mật khẩu
    if 'username' not in session:
        return redirect(url_for('login'))

    username = request.form.get('username')
    current_password = request.form.get('current-password')
    new_password_1 = request.form.get('new-password-1')
    new_password_2 = request.form.get('new-password-2')

    # [BƯỚC LỖ HỔNG LOGIC]: Vẫn tin tưởng tuyệt đối vào tham số 'username' lấy từ body form POST 
    # chứ không lấy từ session['username'], tạo điều kiện cho kẻ tấn công thao túng đổi tên thành 'carlos'.
    if username not in USER_DB:
        return "User không tồn tại", 400

    # --- LOGIC KIỂM TRA THEO THỨ TỰ (SEQUENTIAL VALIDATION) ---
    
    # Bước A: Kiểm tra mật khẩu cũ trước
    if USER_DB[username] != current_password:
        # Nếu SAI: Render trực tiếp kết quả tại chỗ (URL trình duyệt vẫn giữ nguyên POST /my-account/change-password)
        return render_template_string(MY_ACCOUNT_TEMPLATE, username=username, msg="Current password is incorrect")
    
    # Bước B: Mật khẩu cũ ĐÚNG rồi mới kiểm tra mật khẩu mới khớp nhau không
    if new_password_1 != new_password_2:
        # Nếu SAI: Render trực tiếp kết quả tại chỗ (URL trình duyệt vẫn giữ nguyên POST /my-account/change-password)
        return render_template_string(MY_ACCOUNT_TEMPLATE, username=username, msg="New passwords do not match")
    
    # Bước C: Mọi thứ hợp lệ -> Đổi mật khẩu thành công vào DB
    USER_DB[username] = new_password_1
    
    # KHI UPDATE XONG: Chuyển hướng (Redirect) về giao diện GET /my-account kèm thông báo thành công
    return redirect(url_for('my_account', success="Password changed successfully!"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)