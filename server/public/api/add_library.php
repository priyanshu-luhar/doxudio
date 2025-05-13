<?php
require_once('config.php');

// Show errors during development
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Enable JSON response
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

// Decode incoming JSON
$data = json_decode(file_get_contents("php://input"), true);

// Validate required fields
if (!isset($data['name']) || !isset($data['creator_id'])) {
    http_response_code(400);
    echo json_encode(["error" => "Missing required fields: name and/or creator_id"]);
    exit();
}

$name = $data['name'];
$creator_id = $data['creator_id'];
$num_books = 0;  // Optional, let DB default handle it

try {
    $stmt = $db->prepare("
        INSERT INTO library (name, creator_id, num_books)
        VALUES (:name, :creator_id, :num_books)
    ");
    $stmt->bindValue(':name', $name, SQLITE3_TEXT);
    $stmt->bindValue(':creator_id', $creator_id, SQLITE3_INTEGER);
    $stmt->bindValue(':num_books', $num_books, SQLITE3_INTEGER);

    $result = $stmt->execute();

    if ($result) {
        echo json_encode([
            "success" => true,
            "library_id" => $db->lastInsertRowID()
        ]);
    } else {
        throw new Exception($db->lastErrorMsg());
    }

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        "error" => "Could not add library: " . $e->getMessage()
    ]);
}
?>

