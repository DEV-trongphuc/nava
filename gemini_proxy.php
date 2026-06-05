<?php
/**
 * PHP Proxy for Sapo BWT AI Search utilizing Google Gemini API.
 * This proxy handles CORS, parses search queries, matches against the provided product list,
 * and calls Gemini 2.5 Flash / 2.0 Flash to return structured recommendations.
 */

// Allow CORS from any domain (Bypass CORS)
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Accept, X-Requested-With');

// Handle preflight OPTIONS request
if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    http_response_code(200);
    exit(0);
}

header('Content-Type: application/json; charset=utf-8');

// --- CONFIGURATION ---
// Fill in your Gemini API key here (preferred):
$apiKey = "YOUR_GEMINI_API_KEY_HERE"; 

// If not filled above, try reading from environment variable:
if (empty($apiKey) || $apiKey === "YOUR_GEMINI_API_KEY_HERE") {
    $apiKey = getenv('GEMINI_API_KEY');
}

// Model to use
$model = "gemini-2.5-flash";

// API Base URL (can be changed to a reverse proxy mirror if Google is blocked on your server)
$apiBaseUrl = "https://generativelanguage.googleapis.com";

// Optional: HTTP Proxy server if your host needs a proxy to reach Google APIs (e.g. "http://127.0.0.1:8080")
$proxy = "";


// Validate API Key
if (empty($apiKey) || $apiKey === "YOUR_GEMINI_API_KEY_HERE") {
    http_response_code(400);
    echo json_encode([
        "error" => "CONFIGURATION_ERROR",
        "message" => "Vui lòng cấu hình GEMINI_API_KEY trong file gemini_proxy.php hoặc biến môi trường."
    ]);
    exit;
}

// Only allow POST request containing JSON body
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode([
        "error" => "METHOD_NOT_ALLOWED",
        "message" => "Chỉ chấp nhận phương thức POST."
    ]);
    exit;
}

// Read raw inputs
$rawInput = file_get_contents('php://input');
$input = json_decode($rawInput, true);

if (!$input || empty($input['query']) || !isset($input['products']) || !is_array($input['products'])) {
    http_response_code(400);
    echo json_encode([
        "error" => "INVALID_INPUT",
        "message" => "Yêu cầu phải chứa JSON body với các thuộc tính 'query' và 'products' (mảng)."
    ]);
    exit;
}

$query = trim($input['query']);
$products = $input['products'];

// Limit products list to prevent payload size overflow (max 40 products)
if (count($products) > 40) {
    $products = array_slice($products, 0, 40);
}

// Construct prompt for Gemini
$formattedProducts = "";
foreach ($products as $index => $prod) {
    $formattedProducts .= sprintf(
        "[%d] Tên: %s | Giá: %s | Mô tả: %s\n",
        $index,
        $prod['name'] ?? '',
        $prod['price'] ?? '',
        $prod['desc'] ?? ''
    );
}

$prompt = "Bạn là trợ lý AI tìm kiếm sản phẩm thông minh của cửa hàng Nava Store (chuyên Mini PC, eGPU, phần cứng cao cấp).\n";
$prompt .= "Nhiệm vụ của bạn là phân tích nhu cầu của khách hàng thông qua câu truy vấn dưới đây và tìm ra những sản phẩm phù hợp nhất trong danh sách sản phẩm được cung cấp.\n\n";
$prompt .= "Câu truy vấn của khách hàng: \"" . $query . "\"\n\n";
$prompt .= "Danh sách sản phẩm cửa hàng đang có:\n" . $formattedProducts . "\n";
$prompt .= "Hãy thực hiện các bước sau:\n";
$prompt .= "1. Tìm từ 1 đến 5 sản phẩm phù hợp nhất trong danh sách. Nếu không có sản phẩm nào phù hợp trực tiếp, hãy tìm sản phẩm gần đúng nhất.\n";
$prompt .= "2. Viết một đoạn phân tích ngắn (tối đa 3 câu) bằng tiếng Việt, giải thích vì sao chọn những sản phẩm này hoặc gợi ý thêm cho khách hàng một cách tự nhiên, thân thiện.\n";
$prompt .= "3. Trả về kết quả dưới dạng JSON tuân thủ cấu trúc schema yêu cầu.";

// Structure request body for Gemini API with structured JSON output schema
$geminiPayload = [
    "contents" => [
        [
            "parts" => [
                [
                    "text" => $prompt
                ]
            ]
        ]
    ],
    "generationConfig" => [
        "responseMimeType" => "application/json",
        "responseSchema" => [
            "type" => "OBJECT",
            "properties" => [
                "explanation" => [
                    "type" => "STRING",
                    "description" => "Tóm tắt phân tích nhu cầu ngắn gọn bằng tiếng Việt (1-3 câu) giải thích vì sao đề xuất các sản phẩm này."
                ],
                "recommended_indexes" => [
                    "type" => "ARRAY",
                    "items" => [
                        "type" => "INTEGER"
                    ],
                    "description" => "Mảng chứa các chỉ số (index) của sản phẩm trong danh sách đầu vào được đề xuất, xếp theo độ ưu tiên giảm dần."
                ]
            ],
            "required" => ["explanation", "recommended_indexes"]
        ]
    ]
];

// Execute API call via Curl
$url = $apiBaseUrl . "/v1beta/models/" . $model . ":generateContent?key=" . $apiKey;

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($geminiPayload));
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json'
]);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); // Bypass SSL verification for legacy server environments if needed
curl_setopt($ch, CURLOPT_TIMEOUT, 15); // 15 seconds timeout

// Set proxy if configured
if (!empty($proxy)) {
    curl_setopt($ch, CURLOPT_PROXY, $proxy);
}


$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlError = curl_error($ch);
curl_close($ch);

if ($response === false) {
    http_response_code(502);
    echo json_encode([
        "error" => "CURL_ERROR",
        "message" => "Không thể kết nối đến Gemini API: " . $curlError
    ]);
    exit;
}

if ($httpCode !== 200) {
    http_response_code($httpCode);
    $errorData = json_decode($response, true);
    echo json_encode([
        "error" => "GEMINI_API_ERROR",
        "message" => "Lỗi từ phía Gemini API (HTTP $httpCode)",
        "details" => $errorData
    ]);
    exit;
}

// Parse Gemini's response
$responseDecoded = json_decode($response, true);
$candidateText = $responseDecoded['candidates'][0]['content']['parts'][0]['text'] ?? '';

if (empty($candidateText)) {
    http_response_code(500);
    echo json_encode([
        "error" => "PARSE_ERROR",
        "message" => "Không tìm thấy nội dung phản hồi từ Gemini API.",
        "raw" => $responseDecoded
    ]);
    exit;
}

// The response text is a JSON string matching our schema. Output it directly.
echo $candidateText;
?>
