<?php
// Kết nối PostgreSQL
$host = "localhost";
$db = "xml_encode";
$user = "postgres";
$pass = "1";
$dsn = "pgsql:host=$host;port=5432;dbname=$db;user=$user;password=$pass";

try {
    $pdo = new PDO($dsn);
} catch (PDOException $e) {
    die("Lỗi kết nối: " . $e->getMessage());
}

// Xử lý request POST (API Check Stock)
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $xml_raw = file_get_contents('php://input');

    // WAF giả lập: Chặn từ khóa SELECT/UNION viết thường hoặc viết hoa
    if (preg_match('/UNION|SELECT/i', $xml_raw)) {
        http_response_code(403);
        die("Attack detected and blocked by WAF!");
    }

    // Parse XML (Tự động giải mã các thực thể như &#x55; -> U)
    $xml = simplexml_load_string($xml_raw, 'SimpleXMLElement', LIBXML_NOENT);
    $product_id = (string)$xml->productId;
    $store_id = (string)$xml->storeId;

    // LỖ HỔNG: Nối chuỗi trực tiếp vào query PostgreSQL
    // Chúng ta inject qua store_id
    $sql = "SELECT count::text FROM stocks WHERE product_id = $product_id AND store_id = $store_id";

    try {
        $stmt = $pdo->query($sql);
        $results = $stmt->fetchAll(PDO::FETCH_COLUMN);
        if ($results) {
            echo implode("<br>", $results);
        } else {
            echo "0 units";
        }
    } catch (Exception $e) {
        echo "Error: " . $e->getMessage();
    }
    exit;
}

// Giao diện trang sản phẩm (GET)
$product_id = $_GET['productId'] ?? 1;
$stmt = $pdo->prepare("SELECT * FROM products WHERE id = ?");
$stmt->execute([$product_id]);
$product = $stmt->fetch();
?>

<!DOCTYPE html>
<html>
<head>
    <title>Product Page</title>
</head>
<body>
    <h1><?php echo $product['name']; ?></h1>
    <p><?php echo $product['description']; ?></p>

    <hr>
    <h3>Check Stock</h3>
    <button onclick="checkStock()">Check Stock</button>
    <p id="stockResult"></p>

    <script>
    function checkStock() {
        const url = window.location.href;
        const xmlData = `<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId><?php echo $product_id; ?></productId><storeId>1</storeId></stockCheck>`;

        fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'text/xml' },
            body: xmlData
        })
        .then(response => response.text())
        .then(data => {
            document.getElementById('stockResult').innerText = data;
        });
    }
    </script>
</body>
</html>