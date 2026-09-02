import requests, psycopg2
from flask import Flask, request, render_template

app = Flask(__name__)

# Config db 
DB_URI = "dbname=ssrf_lab user=postgres password=1 host=localhost"

# -- GIAO DIỆN CHÍNH --
@app.route('/')
def index():
    # Lấy data sản phẩm thật từ DB
    with psycopg2.connect(DB_URI) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, description FROM products ORDER BY id")
            products = cur.fetchall()
            
    return render_template('index.html', products=products)

# -- LỖ HỔNG SSRF NẰM Ở ĐÂY --
@app.route('/check', methods=['POST'])
def check():
    url = request.form.get('url', '')
    
    # filter lởm
    if '127.0.0.1' in url or 'localhost' in url:
        return "Localhost blocked", 403
    if 'admin' in url:
        return "Admin access blocked", 403

    try:
        # Lên đường! (Gửi request HTTP thật sự tới URL)
        return requests.get(url, timeout=3).text
    except Exception as e:
        return f"Fetch error: {str(e)}", 500

# -- INTERNAL API (Hệ thống nội bộ check kho) --
@app.route('/api/stock')
def api_stock():
    # Thực tế cái API này có thể nằm ở server khác (ví dụ port 8080)
    # Ở đây gom chung vào port 5000 cho dễ chạy lab
    pid = request.args.get('productId')
    if not pid: 
        return "Missing productId", 400
        
    with psycopg2.connect(DB_URI) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT stock FROM products WHERE id = %s", (pid,))
            res = cur.fetchone()
            
    if res:
        return f"Còn {res[0]} sản phẩm trong kho"
    return "Sản phẩm không tồn tại", 404

# -- ADMIN PANEL VÀ CHỨC NĂNG XÓA --
@app.route('/admin')
def admin():
    if request.remote_addr != '127.0.0.1':
        return "Only for local admin", 403
    return render_template('admin.html')

@app.route('/admin/delete')
def delete_user():
    if request.remote_addr != '127.0.0.1':
        return "Only for local admin", 403
        
    u = request.args.get('u')
    if not u: 
        return "Missing u", 400

    # Execute delete thật
    with psycopg2.connect(DB_URI) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE username = %s RETURNING id", (u,))
            res = cur.fetchone()
            
    return f"Deleted {u}" if res else "User not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)