<?php
require_once('config.php');

// Enable foreign key constraints (if needed later)
$db->exec("PRAGMA foreign_keys = ON");

// Get raw POST data and decode JSON
$data = json_decode(file_get_contents("php://input"), true);

// Check required fields
if (!isset($data['uname'], $data['fname'], $data['lname'], $data['hash'])) {
    http_response_code(400);
    echo json_encode(["error" => "Missing required fields."]);
    exit();
}

// Prepare statement to insert user
$stmt = $db->prepare('INSERT INTO person (uname, fname, lname, hash) VALUES (:uname, :fname, :lname, :hash)');
$stmt->bindValue(':uname', $data['uname'], SQLITE3_TEXT);
$stmt->bindValue(':fname', $data['fname'], SQLITE3_TEXT);
$stmt->bindValue(':lname', $data['lname'], SQLITE3_TEXT);
$stmt->bindValue(':hash', $data['hash'], SQLITE3_TEXT);

try {
    $result = $stmt->execute();
    if ($result) {
        echo json_encode(["success" => true, "user_id" => $db->lastInsertRowID()]);
    } else {
        throw new Exception($db->lastErrorMsg());  // << more detailed error
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(["error" => "Could not add user: " . $e->getMessage()]);
}

?>
