import secrets
from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-lab'

# Cấu hình PostgreSQL (Đổi thông tin cho phù hợp với máy bạn)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost/xss_csrf_lab'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ================= MODEL =================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text, nullable=False) # Cố tình không sanitize để tạo XSS

# ================= CSRF TOKEN =================
def get_csrf_token():
    if 'csrf' not in session:
        session['csrf'] = secrets.token_hex(16)
    return session['csrf']

@app.context_processor
def inject_csrf():
    return dict(csrf_token=get_csrf_token())

# ================= ROUTES =================
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/my-account', methods=['GET'])
def my_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('my_account.html', user=user)

@app.route('/my-account/change-email', methods=['POST'])
def change_email():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Kiểm tra CSRF Token
    token = request.form.get('csrf')
    if not token or token != session.get('csrf'):
        return "CSRF Token missing or incorrect", 403
    
    new_email = request.form.get('email')
    user = User.query.get(session['user_id'])
    user.email = new_email
    db.session.commit()
    flash('Email changed successfully!', 'success')
    return redirect(url_for('my_account'))

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        author = request.form.get('author', 'Anonymous')
        body = request.form.get('body')
        
        # LƯU Ý: Lưu trực tiếp không filter -> Tạo lỗ hổng Stored XSS
        new_comment = Comment(post_id=post.id, author=author, body=body)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('view_post', post_id=post.id))
        
    comments = Comment.query.filter_by(post_id=post.id).all()
    return render_template('post.html', post=post, comments=comments)

# ================= INIT DATABASE =================
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='wiener').first():
        db.session.add(User(username='wiener', password='peter', email='wiener@normal-user.net'))
        db.session.add(User(username='admin', password='password123', email='admin@site.com'))
        db.session.add(Post(title='Welcome to the Blog', content='This is the first post. Feel free to leave a comment!'))
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=5000)