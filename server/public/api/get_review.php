<?php
require_once('config.php');

// Show PHP errors during development
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Set headers
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

// Decode the JSON input
$data = json_decode(file_get_contents("php://input"), true);

// Validate input
if (!isset($data['book_id'])) {
    http_response_code(400);
    echo json_encode(["error" => "Missing required field: book_id"]);
    exit();
}

$book_id = $data['book_id'];

try {
    // Fetch all reviews for the given book_id
    $stmt = $db->prepare("
        SELECT review.review_id, review.rating, review.content, review.book_id, review.reviewer_id,
               person.uname AS reviewer_name
        FROM review
        LEFT JOIN person ON review.reviewer_id = person.user_id
        WHERE review.book_id = :book_id
        ORDER BY review.review_id DESC
    ");
    $stmt->bindValue(':book_id', $book_id, SQLITE3_INTEGER);

    $result = $stmt->execute();
    $reviews = [];

    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $reviews[] = $row;
    }

    echo json_encode(["book_id" => $book_id, "reviews" => $reviews]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(["error" => "Could not retrieve reviews: " . $e->getMessage()]);
}
?>

