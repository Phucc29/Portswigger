import html
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

DB_CONFIG = {
    'dbname': 'xss_lab',
    'user': 'postgres',
    'password': '1', 
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def custom_escape(val: str) -> str:
    """
    Mô phỏng bộ lọc của PortSwigger:
    1. Thêm dấu slash vào trước nháy đơn (')
    2. Mã hóa HTML cho <, >, "
    3. CỐ TÌNH BỎ QUA ký tự &
    """
    if not val:
        return ""
    
    val = val.replace("'", "\\'")
    val = val.replace('<', '&lt;')
    val = val.replace('>', '&gt;')
    val = val.replace('"', '&quot;')
    
    return val

@app.template_filter('portswigger_escape')
def portswigger_escape_filter(s):
    return custom_escape(s)

# --- ĐỊNH TUYẾN MỚI ---

# 1. Trang chủ: Hiển thị danh sách bài viết
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# 2. Trang chi tiết bài viết & Xử lý comment
@app.route('/post', methods=['GET', 'POST'])
def view_post():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        website = request.form.get('website', '')
        comment = request.form.get('comment', '')

        # Lưu vào DB không qua bộ lọc
        cur.execute(
            "INSERT INTO comments (name, email, website, comment) VALUES (%s, %s, %s, %s)",
            (name, email, website, comment)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        # Reload lại trang bài viết sau khi comment
        return redirect(url_for('view_post'))

    # Lấy danh sách comment
    cur.execute("SELECT * FROM comments ORDER BY id ASC")
    comments = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('post.html', comments=comments)

if __name__ == '__main__':
    app.run(debug=True, port=5000)