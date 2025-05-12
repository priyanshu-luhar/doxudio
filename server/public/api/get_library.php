<?php
require_once('config.php');

// Show errors during development
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Enable JSON response
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

// Parse JSON input
$data = json_decode(file_get_contents("php://input"), true);

// Validate input
if (!isset($data['library_id'])) {
    http_response_code(400);
    echo json_encode(["error" => "Missing required field: library_id"]);
    exit();
}

$library_id = $data['library_id'];

try {
    // Step 1: Fetch library info
    $stmt = $db->prepare("SELECT * FROM library WHERE library_id = :library_id");
    $stmt->bindValue(':library_id', $library_id, SQLITE3_INTEGER);
    $library_result = $stmt->execute();
    $library = $library_result->fetchArray(SQLITE3_ASSOC);

    if (!$library) {
        http_response_code(404);
        echo json_encode(["error" => "Library not found"]);
        exit();
    }

    // Step 2: Fetch books in library via 'belongs' table
    $stmt_books = $db->prepare("
        SELECT b.* FROM book b
        INNER JOIN belongs bl ON b.book_id = bl.book_id
        WHERE bl.library_id = :library_id
    ");
    $stmt_books->bindValue(':library_id', $library_id, SQLITE3_INTEGER);
    $books_result = $stmt_books->execute();

    $books = [];
    while ($row = $books_result->fetchArray(SQLITE3_ASSOC)) {
        $books[] = $row;
    }

    // Step 3: Build response
    $response = [
        "library" => $library,
        "books" => $books
    ];

    echo json_encode($response);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(["error" => "Could not retrieve library: " . $e->getMessage()]);
}
?>

