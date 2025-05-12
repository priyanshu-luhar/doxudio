<?php
require_once('config.php');

// Enable error display (development only)
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Set JSON headers
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

// Decode input
$data = json_decode(file_get_contents("php://input"), true);

// Validate fields
if (!isset($data['uname']) || !isset($data['password_hash'])) {
    http_response_code(400);
    echo json_encode(["error" => "Missing username or password hash"]);
    exit();
}

$uname = $data['uname'];
$password_hash = $data['password_hash'];

try {
    // Look up user
    $stmt = $db->prepare("SELECT * FROM person WHERE uname = :uname");
    $stmt->bindValue(':uname', $uname, SQLITE3_TEXT);
    $result = $stmt->execute();
    $user = $result->fetchArray(SQLITE3_ASSOC);

    if (!$user) {
        echo json_encode(["status" => "no_user"]);
    } elseif ($user['hash'] !== $password_hash) {
        echo json_encode(["status" => "wrong_password"]);
    } else {
        echo json_encode([
            "status" => "success",
            "user" => [
                "user_id" => $user["user_id"],
                "uname" => $user["uname"],
                "fname" => $user["fname"],
                "lname" => $user["lname"]
            ]
        ]);
    }

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(["error" => "Authentication failed: " . $e->getMessage()]);
}
?>

