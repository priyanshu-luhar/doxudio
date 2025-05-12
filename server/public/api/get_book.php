<?php
require_once('config.php');

// Show errors during development
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Set headers
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

// Decode request JSON
$data = json_decode(file_get_contents("php://input"), true);

// No filters provided
if (!$data || (!isset($data['isbn']) && !isset($data['title']) && !isset($data['author']))) {
    http_response_code(400);
    echo json_encode(["error" => "Provide at least one of: isbn, title, or author."]);
    exit();
}

$conditions = [];
$params = [];

// Build WHERE clause dynamically
if (isset($data['isbn'])) {
    $conditions[] = "(isbn10 = :isbn OR isbn13 = :isbn)";
    $params[':isbn'] = $data['isbn'];
}
if (isset($data['title'])) {
    $conditions[] = "LOWER(title) LIKE :title";
    $params[':title'] = '%' . strtolower($data['title']) . '%';
}
if (isset($data['author'])) {
    $conditions[] = "LOWER(author) LIKE :author";
    $params[':author'] = '%' . strtolower($data['author']) . '%';
}

$whereClause = implode(' AND ', $conditions);
$sql = "SELECT * FROM book WHERE $whereClause";

try {
    $stmt = $db->prepare($sql);
    foreach ($params as $key => $value) {
        $stmt->bindValue($key, $value, SQLITE3_TEXT);
    }

    $result = $stmt->execute();
    $books = [];

    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $books[] = $row;
    }

    echo json_encode($books);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(["error" => "Query failed: " . $e->getMessage()]);
}
?>

