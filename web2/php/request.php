<?php

    require_once('database.php');

    // Database connexion.
    $db = dbConnect();
    if (!$db)
    {
        header ('HTTP/1.1 503 Service Unavailable');
        exit;
    }

    // Check the request.
    $requestMethod = $_SERVER['REQUEST_METHOD'];
    $request = $_SERVER['PATH_INFO'];
    $request = explode('/', $request);

    if ($request[1] != 'alertes')
    {
        header('HTTP/1.1 400 Bad Request');
        exit;
    }

    if ($requestMethod == 'GET')
    {
        $data = dbRequestAlerts($db);
    }
  
    if ($requestMethod == 'PUT')
    {
        parse_str(file_get_contents('php://input'), $_PUT);
        if($id !=''&&isset($_PUT['login'])&&isset($_PUT['text']))
            $data = dbModifyTweet($db, $id, $_PUT['login'], strip_tags($_PUT['text']));
    }

    // Send data to the client.
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-control: no-store, no-cache, must-revalidate');
    header('Pragma: no-cache');
    if($requestMethod == 'POST')
        header('HTTP/1.1 201 Created');
    else
        header('HTTP/1.1 200 OK');
    echo json_encode($data);
    exit;
?>
