from flask import Flask, request, render_template_string, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'portswigger_lab_secret_key'

# Cơ sở dữ liệu giả lập
users_db = {
    "admin": {"password": "password123", "role": "Administrator"},
    "carlos": {"password": "password123", "role": "User"},
    "wiener": {"password": "password123", "role": "User"}
}

# 1. TRANG CHỦ & LOGIN
@app.route('/')
def home():
    if 'username' not in session:
        return 'Chưa đăng nhập. <a href="/login">Đăng nhập tại đây</a>'
    
    u = session['username']
    status = "".join([f"<li>{user}: {users_db[user]['role']}</li>" for user in users_db])
    return f"""
    <p>Logged in as: <b>{u}</b> ({users_db[u]['role']}) | <a href="/logout">Logout</a></p>
    <h3>User List:</h3><ul>{status}</ul>
    <p><a href="/admin-roles">Go to Admin Panel</a></p>
    """

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users_db and users_db[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        return 'Wrong credentials! <a href="/login">Try again</a>'
    return '<form method="POST">User: <input name="username"><br>Pass: <input type="password" name="password"><br><button>Login</button></form>'

# BƯỚC 1: ADMIN PANEL - CHỈ ADMIN VÀO ĐƯỢC (Ứng với bước "Browse to the admin panel")
@app.route('/admin-roles', methods=['GET'])
def admin_roles_page():
    if 'username' not in session or users_db[session['username']]['role'] != 'Administrator':
        return '403 Unauthorized (Chỉ Admin mới được vào trang này)', 403

    options = "".join([f'<option value="{u}">{u} ({users_db[u]["role"]})</option>' for u in users_db])
    return f"""
    <h3>Admin Role Management</h3>
    <form action="/admin-roles/confirm" method="POST">
        User: <select name="username">{options}</select><br><br>
        Action: <select name="action"><option value="upgrade">Upgrade</option><option value="downgrade">Downgrade</option></select><br><br>
        <button type="submit">Next</button>
    </form>
    """

# BƯỚC 2: CONFIRMATION PAGE - CHỈ ADMIN VÀO ĐƯỢC 
@app.route('/admin-roles/confirm', methods=['POST'])
def admin_roles_confirm():
    if 'username' not in session or users_db[session['username']]['role'] != 'Administrator':
        return '403 Unauthorized (Chỉ Admin mới được xác nhận)', 403
        
    username = request.form.get('username')
    action = request.form.get('action')
    return f"""
    <h3>Are you sure you want to {action} {username}?</h3>
    <form action="/admin-roles/execute" method="POST">
        <input type="hidden" name="username" value="{username}">
        <input type="hidden" name="action" value="{action}">
        <input type="hidden" name="confirmed" value="true">
        <button type="submit">Yes, Confirm</button>
    </form>
    """

# 4. BƯỚC 3: ENDPOINT THỰC THI (MÔ PHỎNG CHUẨN KỊCH BẢN PORTSWIGGER)
@app.route('/admin-roles/execute', methods=['POST'])
def admin_roles_execute():
    # 1. Kiểm tra xem có session đăng nhập hợp lệ không (Nếu không có -> 401)
    if 'username' not in session:
        return '["Unauthorized"]', 401

    # Lấy ra tên của người ĐANG GỬI REQUEST (thông qua Cookie Session)
    current_session_user = session['username']
    
    # Lấy ra tên của người ĐƯỢC CHỌN ĐỂ NÂNG CẤP (thông qua Body Request)
    target_user = request.form.get('username')
    action = request.form.get('action')
    confirmed = request.form.get('confirmed')

    # 💥 BẢN CHẤT LỖ HỔNG CỦA BÀI LAB:
    # Lẽ ra ở đây phải check: if users_db[current_session_user]['role'] != 'Administrator': return 403
    # Nhưng lập trình viên QUÊN CHECK QUYỀN ADMIN. 
    # Họ chỉ thực thi thăng chức dựa trên data gửi lên từ form!
    
    if confirmed == 'true' and target_user in users_db:
        if action == 'upgrade':
            users_db[target_user]['role'] = 'Administrator'
        elif action == 'downgrade':
            users_db[target_user]['role'] = 'User'
            
        # Trả về thông báo thành công hiển thị rõ AI đã nâng cấp cho AI để bạn dễ theo dõi trong Burp
        return f"Success! User '{current_session_user}' updated role for '{target_user}'. <a href='/'>Go Home</a>"
        
    return "Invalid request", 400

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)