<?php
// Cho phép gọi từ mọi domain (Bypass CORS)
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json; charset=utf-8');

$type = isset($_GET['type']) ? $_GET['type'] : 'reviews';

// --- THAY COOKIE CỦA BẠN VÀO ĐÂY ---
// Đăng nhập vào Kênh Người Bán Shopee (seller.shopee.vn)
// F12 -> Network -> chọn Request bất kỳ -> copy toàn bộ chuỗi Cookie dán vào biến này
$shopeeCookie = "YOUR_SHOPEE_SELLER_COOKIE_HERE";

if ($type === 'summary') {
    $url = "https://shopee.vn/api/v4/seller_operation/get_rating_summary_new?shop_id=65856601&userid=65858058";
} else {
    $url = "https://shopee.vn/api/v4/seller_operation/get_shop_ratings_new?userid=65858058&shopid=65856601&limit=6&offset=0&replied=undefined";
}

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept: application/json",
    "Cookie: " . $shopeeCookie
]);

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
