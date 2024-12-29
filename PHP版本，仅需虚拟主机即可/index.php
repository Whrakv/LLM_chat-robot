<?php

// 检查是否存在text参数
if(isset($_GET['text'])){
    // 获取text参数的值
    $text = $_GET['text'];

    // 设置 Google API key
    $apiKey = "AIzaSyA0nqzN9lp4xsgJZFZF6qs9oZBELdzCkIw";

    // 设置请求 URL
    $url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=$apiKey";

    // 设置请求参数
    $contents = [
        "parts" => [
            [
                "text" => $text
            ]
        ]
    ];

    // 使用 cURL 发起 POST 请求
    $curl = curl_init();

    // 设置 cURL 选项
    curl_setopt_array($curl, [
        CURLOPT_URL => $url,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_ENCODING => "",
        CURLOPT_MAXREDIRS => 10,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
        CURLOPT_CUSTOMREQUEST => "POST",
        CURLOPT_POSTFIELDS => json_encode(["contents" => [$contents]]),
        CURLOPT_HTTPHEADER => [
            "Content-Type: application/json"
        ],
    ]);

    // 发起请求并获取响应
    $response = curl_exec($curl);
    $err = curl_error($curl);

    // 关闭 cURL 资源
    curl_close($curl);

    // 处理响应
    if ($err) {
        echo "cURL Error #:" . $err;
    } else {
        // 输出响应
        $responseData = json_decode($response, true);
        $text = $responseData['candidates'][0]['content']['parts'][0]['text'];
        echo $text;
    }
} else {
    echo "Text parameter is missing.";
}

?>

