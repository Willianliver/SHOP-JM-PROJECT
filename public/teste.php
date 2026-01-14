<?php

$access_token = "b4ad51a743ed25eb391ac9c2e91955a7a970de54";

$url = "https://www.bling.com.br/Api/v3/produtos";

$curl = curl_init();

curl_setopt_array($curl, [
    CURLOPT_URL => $url,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HTTPHEADER => [
        "Authorization: Bearer $access_token",
        "Content-Type: application/json"
    ],
]);

$response = curl_exec($curl);
$httpcode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
curl_close($curl);

echo "<h3>HTTP Code: $httpcode</h3>";
echo "<pre>";
print_r(json_decode($response, true));
