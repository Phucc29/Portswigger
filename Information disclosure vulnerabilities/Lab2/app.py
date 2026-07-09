from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cgi-bin/phpinfo.php")
def phpinfo():
    return render_template(
        "phpinfo.html",
        secret_key=os.getenv("SECRET_KEY"),
        db_password=os.getenv("DATABASE_PASSWORD"),
        api_key=os.getenv("API_KEY")
    )


if __name__ == "__main__":
    app.run(debug=True)