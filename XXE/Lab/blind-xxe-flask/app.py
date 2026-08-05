from flask import Flask, request, render_template, Response
from lxml import etree
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    "dbname": "xxelab",
    "user": "postgres",
    "password": "1",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM products ORDER BY id")
    products = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", products=products)

@app.route('/check-stock', methods=['POST'])
def check_stock():
    xml_data = request.data

    try:
        parser = etree.XMLParser(resolve_entities=True, no_network=False)
        xml_doc = etree.fromstring(xml_data, parser)

        product_id = xml_doc.findtext("productId")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT stock FROM products WHERE id=%s",
            (product_id,)
        )

        cur.fetchone()

        cur.close()
        conn.close()

    except Exception:
        pass

    return Response("Stock check processed successfully.", status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)