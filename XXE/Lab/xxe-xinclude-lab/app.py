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
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, stock FROM products;")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
    # except Exception as e:
    #     # Fallback nếu DB chưa khởi chạy
    #     products = [(1, "Product A", 100), (2, "Product B", 50)]

    return render_template('index.html', products=products)

@app.route('/check-stock', methods=['POST'])
def check_stock():
    # Nhận dữ liệu dưới dạng URL-encoded Form Data (application/x-www-form-urlencoded)
    product_id = request.form.get('productId', '')
    store_id = request.form.get('storeId', '1')

    if not product_id:
        return Response("Missing productId", status=400)

    # LỖ HỔNG: Back-end tự chèn input của user vào template XML ở phía Server
    server_side_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
    <productId>{product_id}</productId>
    <storeId>{store_id}</storeId>
</stockCheck>"""

    try:
        # Khởi tạo XML Parser
        parser = etree.XMLParser(resolve_entities=True)
        xml_doc = etree.fromstring(server_side_xml.encode('utf-8'), parser=parser)

        # Bật xử lý XInclude (Cho phép nhúng file qua thẻ XInclude)
        # Bật xử lý XInclude
        xml_doc.getroottree().xinclude()

        # Lấy toàn bộ văn bản bên trong thẻ productId (kể cả trong thẻ con <foo>)
        product_id_elem = xml_doc.find('productId')
        
        if product_id_elem is not None:
            result_text = product_id_elem.xpath('string()')
        else:
            result_text = ""

        return Response(f"Stock check result for product: {result_text}", status=200)

    except etree.XMLSyntaxError as e:
        return Response(f"XML Parsing Error: {str(e)}", status=500)
    except Exception as e:
        return Response(f"Error: {str(e)}", status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)