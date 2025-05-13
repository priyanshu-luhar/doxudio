<?php
require_once('config.php');

// Show errors during development
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Enable JSON response
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

// Decode JSON input
$data = json_decode(file_get_contents("php://input"), true);

// Validate required fields
if (
    !isset($data['book_id']) ||
    !isset($data['reviewer_id']) ||
    !isset($data['rating']) ||
    !isset($data['content'])
) {
    http_response_code(400);
    echo json_encode(["error" => "Missing one or more required fields: book_id, reviewer_id, rating, content"]);
    exit();
}

// Assign variables
$book_id = $data['book_id'];
$reviewer_id = $data['reviewer_id'];
$rating = $data['rating'];
$content = $data['content'];

// Validate rating range
if ($rating < 1 || $rating > 5) {
    http_response_code(400);
    echo json_encode(["error" => "Rating must be between 1 and 5"]);
    exit();
}

try {
    $stmt = $db->prepare("
        INSERT INTO review (book_id, reviewer_id, rating, content)
        VALUES (:book_id, :reviewer_id, :rating, :content)
    ");

    $stmt->bindValue(':book_id', $book_id, SQLITE3_INTEGER);
    $stmt->bindValue(':reviewer_id', $reviewer_id, SQLITE3_INTEGER);
    $stmt->bindValue(':rating', $rating, SQLITE3_INTEGER);
    $stmt->bindValue(':content', $content, SQLITE3_TEXT);

    $result = $stmt->execute();

    if ($result) {
        echo json_encode([
            "success" => true,
            "review_id" => $db->lastInsertRowID()
        ]);
    } else {
        throw new Exception($db->lastErrorMsg());
    }

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(["error" => "Could not add review: " . $e->getMessage()]);
}
?>

