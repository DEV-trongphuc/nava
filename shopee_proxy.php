<?php
// Cho phép gọi từ mọi domain (Bypass CORS)
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Accept');

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    http_response_code(200);
    exit(0);
}

header('Content-Type: application/json; charset=utf-8');

$type = isset($_GET['type']) ? $_GET['type'] : 'reviews';

$ch = curl_init();
$headers = [
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept: application/json"
];

if ($type === 'shop_base') {
    $url = "https://shopee.vn/api/v4/shop/get_shop_detail?shopid=65856601&username=navastore.vn";
} elseif ($type === 'summary') {
    $url = "https://shopee.vn/api/v4/seller_operation/get_rating_summary_new?shop_id=65856601&userid=65858058";
} else {
    $url = "https://shopee.vn/api/v4/seller_operation/get_shop_ratings_new?userid=65858058&shopid=65856601&limit=6&offset=0&replied=undefined";
}

curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

// Bỏ qua check SSL nếu hosting cấu hình cũ
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); 

$response = curl_exec($ch);
$httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpcode == 200) {
    echo $response;
} else {
    echo json_encode(["error" => "PHP_PROXY_ERROR", "http_code" => $httpcode]);
}
?>
