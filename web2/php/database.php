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
    try
    {
      $db = new PDO('mysql:host='.DB_SERVER.';dbname='.DB_NAME.';charset=utf8',
        DB_USER, DB_PASSWORD);
      $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION); 
    }
    catch (PDOException $exception)
    {
      error_log('Connection error: '.$exception->getMessage());
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
    try
    {
      $request = 'SELECT * FROM alertes';
        $params = [];


        // Si $filtres est non nul et non vide, appliquez les conditions
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
    }
    catch (PDOException $exception)
    {
      error_log('Request error: '.$exception->getMessage());
      return false;
    }
    return $result;
  }

    //----------------------------------------------------------------------------
  //--- dbRequestDevices --------------------------------------------------------
  //----------------------------------------------------------------------------
  // Function to get all alertes 
  // \param db The connected database.
  // \return The list of alertes.
  function dbRequestDevices($db)
  {
    try
    {
      $request = 'SELECT device_product FROM alertes GROUP BY device_product;';
      $statement = $db->prepare($request);
      $statement->execute();
      $result = $statement->fetchAll(PDO::FETCH_ASSOC);
    }

    catch (PDOException $exception)
    {
      error_log('Request error: '.$exception->getMessage());
      return false;
    }
    return $result;
  }


  //----------------------------------------------------------------------------
  //--- dbAddCTweet ------------------------------------------------------------
  //----------------------------------------------------------------------------
  // Add a tweet.
  // \param db The connected database.
  // \param login The login of the user.
  // \param text The tweet to add.
  // \return True on success, false otherwise.
  function dbAddTweet($db, $login, $text)
  {
    try
    {
      $request = 'INSERT INTO tweets(login, text) VALUES(:login, :text)';
      $statement = $db->prepare($request);
      $statement->bindParam(':login', $login, PDO::PARAM_STR, 20);
      $statement->bindParam(':text', $text, PDO::PARAM_STR, 80);
      $statement->execute();
    }
    catch (PDOException $exception)
    {
      error_log('Request error: '.$exception->getMessage());
      return false;
    }
    return true;
  }
  
  //----------------------------------------------------------------------------
  //--- dbModifyTweet ----------------------------------------------------------
  //----------------------------------------------------------------------------
  // Function to modify a tweet.
  // \param db The connected database.
  // \param id The id of the tweet to update.
  // \param login The login of the user.
  // \param text The new tweet.
  // \return True on success, false otherwise.
  function dbModifyTweet($db, $id, $login, $text)
  {
    try
    {
      $request = 'UPDATE tweets SET text=:text WHERE id=:id AND login=:login ';
      $statement = $db->prepare($request);
      $statement->bindParam(':id', $id, PDO::PARAM_INT);
      $statement->bindParam(':login', $login, PDO::PARAM_STR, 20);
      $statement->bindParam(':text', $text, PDO::PARAM_STR, 80);
      $statement->execute();
    }
    catch (PDOException $exception)
    {
      error_log('Request error: '.$exception->getMessage());
      return false;
    }
    return true;
  }

  //----------------------------------------------------------------------------
  //--- dbDeleteTweet ----------------------------------------------------------
  //----------------------------------------------------------------------------
  // Delete a tweet.
  // \param db The connected database.
  // \param id The id of the tweet.
  // \param login The login of the user.
  // \return True on success, false otherwise.
  function dbDeleteTweet($db, $id, $login)
  {
    try
    {
      $request = 'DELETE FROM tweets WHERE id=:id AND login=:login';
      $statement = $db->prepare($request);
      $statement->bindParam(':id', $id, PDO::PARAM_INT);
      $statement->bindParam(':login', $login, PDO::PARAM_STR, 20);
      $statement->execute();
    }
    catch (PDOException $exception)
    {
      error_log('Request error: '.$exception->getMessage());
      return false;
    }
    return true;
  }
?>
