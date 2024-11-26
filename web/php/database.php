<?php
require_once('constants.php');
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

//----------------------------------------------------------------------------
//--- dbConnect --------------------------------------------------------------
//----------------------------------------------------------------------------
// Create the connection to the database.
// \return False on error and the database otherwise.
function dbConnect()
{
  try {
    $db = new PDO(
      'mysql:host=' . DB_SERVER . ';dbname=' . DB_NAME . ';charset=utf8',
      DB_USER,
      DB_PASSWORD
    );
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  } catch (PDOException $exception) {
    error_log('Connection error: ' . $exception->getMessage());
    return false;
  }
  return $db;
}

//----------------------------------------------------------------------------
//--- dbRequestAlertes --------------------------------------------------------
//----------------------------------------------------------------------------
// Function to get all alertes 
// \param db The connected database.
// \return The list of alertes.
function dbRequestAlerts($db, $filtres = null, $orderby, $order)
{
  try {
    $request = 'SELECT * FROM alertes';
    $params = [];

    if (isset($filtres)) {
      $conditions = [];
      foreach ($filtres as $colonne => $valeur) {
        $conditions[] = "$colonne = :$colonne";
        $params[":$colonne"] = $valeur;
      }
      $request .= ' WHERE ' . implode(' AND ', $conditions);
    }

    $request .= " ORDER BY $orderby $order";

    $statement = $db->prepare($request);
    $statement->execute($params);
    $result = $statement->fetchAll(PDO::FETCH_ASSOC);
  } catch (PDOException $exception) {
    error_log('Request error: ' . $exception->getMessage());
    return false;
  }
  return $result;
}

//----------------------------------------------------------------------------
//--- dbRequestDevices --------------------------------------------------------
//----------------------------------------------------------------------------
// Function to get all Devices 
// \param db The connected database.
// \return The list of Devices.
function dbRequestDevices($db)
{
  try {
    $request = 'SELECT device_product FROM alertes GROUP BY device_product;';
    $statement = $db->prepare($request);
    $statement->execute();
    $result = $statement->fetchAll(PDO::FETCH_ASSOC);
  } catch (PDOException $exception) {
    error_log('Request error: ' . $exception->getMessage());
    return false;
  }
  return $result;
}
