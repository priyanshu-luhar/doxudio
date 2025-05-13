<?php
require_once('config.php');

// Enable CORS and JSON response
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

// Decode the incoming JSON
$data = json_decode(file_get_contents("php://input"), true);

if (!$data || !is_array($data)) {
    http_response_code(400);
    echo json_encode(["error" => "Invalid or empty JSON payload"]);
    exit();
}

$required = ['title', 'author', 'published', 'abstract', 'isbn10', 'isbn13'];
foreach ($required as $field) {
    if (!array_key_exists($field, $data)) {
        http_response_code(400);
        echo json_encode(["error" => "Missing required field: $field"]);
        exit();
    }
}

// Extract data
$title = $data['title'];
$author = $data['author'];
$published = $data['published'];
$abstract = $data['abstract'];
$isbn10 = $data['isbn10'];
$isbn13 = $data['isbn13'];
$coverpath = isset($data['coverpath']) ? $data['coverpath'] : null;

try {
    $stmt = $db->prepare("
        INSERT INTO book (title, author, published, abstract, isbn10, isbn13, coverpath)
        VALUES (:title, :author, :published, :abstract, :isbn10, :isbn13, :coverpath)
    ");

    $stmt->bindValue(':title', $title, SQLITE3_TEXT);
    $stmt->bindValue(':author', $author, SQLITE3_TEXT);
    $stmt->bindValue(':published', $published, SQLITE3_TEXT);  // SQLite accepts date as TEXT
    $stmt->bindValue(':abstract', $abstract, SQLITE3_TEXT);
    $stmt->bindValue(':isbn10', $isbn10, SQLITE3_TEXT);
    $stmt->bindValue(':isbn13', $isbn13, SQLITE3_TEXT);
    $stmt->bindValue(':coverpath', $coverpath, SQLITE3_TEXT);

    $result = $stmt->execute();

    if ($result) {
        echo json_encode(["success" => true, "book_id" => $db->lastInsertRowID()]);
    } else {
        throw new Exception($db->lastErrorMsg());
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(["error" => "Could not add book: " . $e->getMessage()]);
}
?>

