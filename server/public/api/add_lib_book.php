<?php
require_once('config.php');

// Show PHP errors (dev only)
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// JSON response setup
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

// Decode incoming JSON
$data = json_decode(file_get_contents("php://input"), true);

// Validate required fields
if (!isset($data['library_id']) || !isset($data['book_id'])) {
    http_response_code(400);
    echo json_encode(["error" => "Missing required fields: library_id and/or book_id"]);
    exit();
}

// Extract values
$library_id = $data['library_id'];
$book_id = $data['book_id'];
$added_on = date('Y-m-d');

try {
    // Step 1: Insert into belongs
    $stmt = $db->prepare("
        INSERT INTO belongs (library_id, book_id, added_on)
        VALUES (:library_id, :book_id, :added_on)
    ");
    $stmt->bindValue(':library_id', $library_id, SQLITE3_INTEGER);
    $stmt->bindValue(':book_id', $book_id, SQLITE3_INTEGER);
    $stmt->bindValue(':added_on', $added_on, SQLITE3_TEXT);

    $insert_result = $stmt->execute();

    if (!$insert_result) {
        throw new Exception("Insert failed: " . $db->lastErrorMsg());
    }

    // Step 2: Increment num_books in library
    $update_stmt = $db->prepare("
        UPDATE library SET num_books = num_books + 1 WHERE library_id = :library_id
    ");
    $update_stmt->bindValue(':library_id', $library_id, SQLITE3_INTEGER);

    $update_result = $update_stmt->execute();

    if (!$update_result) {
        throw new Exception("Failed to update num_books: " . $db->lastErrorMsg());
    }

    echo json_encode([
        "success" => true,
        "library_id" => $library_id,
        "book_id" => $book_id,
        "added_on" => $added_on
    ]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(["error" => "Could not add book to library: " . $e->getMessage()]);
}
?>

