<?php
require_once('database.php');
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);


// Database connexion.
$db = dbConnect();
if (!$db) {
    header('HTTP/1.1 503 Service Unavailable');
    exit;
}

// Check the request.
$requestMethod = $_SERVER['REQUEST_METHOD'];
$request = $_SERVER['PATH_INFO'];
$request = explode('/', $request);


if ($request[1] == 'alertes') {
    if ($requestMethod == 'GET') {

        $filtresArray = [];
        if(isset($_GET['device_product']))
            $filtresArray['device_product'] = $_GET['device_product'];
        if(isset($_GET['agent_severity']))
            $filtresArray['agent_severity'] = $_GET['agent_severity'];
        error_log('filtres array : ' . json_encode($filtresArray));

        if (!empty($filtresArray)) {
            $data = dbRequestAlerts($db, $filtresArray);
        } else {
            $data = dbRequestAlerts($db, null);
        }
    }

    if ($requestMethod == 'PUT') {
        parse_str(file_get_contents('php://input'), $_PUT);
        if ($id != '' && isset($_PUT['login']) && isset($_PUT['text']))
            $data = dbModifyTweet($db, $id, $_PUT['login'], strip_tags($_PUT['text']));
    }
}

if ($request[1] == 'devices') {
    $data = dbRequestDevices($db);
}

// Send data to the client.
header('Content-Type: application/json; charset=utf-8');
header('Cache-control: no-store, no-cache, must-revalidate');
header('Pragma: no-cache');
if ($requestMethod == 'POST')
    header('HTTP/1.1 201 Created');
else
    header('HTTP/1.1 200 OK');
echo json_encode($data);
exit;
