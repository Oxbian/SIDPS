<?php

class Database
{
    private $db_name;
    private $db_user;
    private $db_pass;
    private $db_host;
    private $pdo;

    public function __construct($db_name = "sidps", $db_user = 'sidps', $db_pass = 'sidps', $db_host = 'localhost')
    {
        $this->db_name = $db_name;
        $this->db_user = $db_user;
        $this->db_pass = $db_pass;
        $this->db_host = $db_host;
    }

    private function getPDO()
    {
        if ($this->pdo === null) {
            $pdo = new PDO('mysql:dbname=' . $this->db_name . ';host=localhost;charset=UTF8', $this->db_user, $this->db_pass);
            $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $this->pdo = $pdo;
        }
        return $this->pdo;
    }

    public function query($stmt, $class_name)
    {
        $req = $this->getPDO()->query($stmt);
        return $req->fetchAll(PDO::FETCH_CLASS, $class_name);
    }


    // TOCHANGE  
    public function getnbAlerts()
    {
        $sql = 'SELECT COUNT(*) AS nb_alerts FROM alertes';

        $sth = $this->getPDO()->prepare($sql);
        $sth->execute();
        $result = $sth->fetch();

        $nbAlerts = (int) $result['nb_alerts'];
        return $nbAlerts;
    }

    // TODO
    public function getAlerts($filters = null, $limit = 10)
    {
        $whereArgs = [];

        if (isset($_GET["page"])) {
            $page = intval($_GET['page']);
        } else {
            $page = 1;
        }

        $decalage = ($page - 1) * $limit;

        $sql = 'SELECT *
        FROM alertes ';

        if ($filters != null) {
            foreach ($filters as $key => $value) {
                if ($value != '') $whereArgs[] = $key . ' = :' . $key;
            }
        }
        if (!empty($whereArgs)) $sql .= 'WHERE ' . implode(' AND ', $whereArgs);

        $sql .= ' LIMIT :limit OFFSET :offset';
        $sth = $this->getPDO()->prepare($sql);

        // TODO : edit filters
        if ($filters != null) {
            if ($filters['event_gravite'] != '') $sth->bindParam('event_gravite', $filters['event_gravite']);
            if ($filters['device_product'] != '') $sth->bindParam('device_product', $filters['device_product']);
            // if ($filters['zone'] != '') $sth->bindParam('zone', $filters['zone']);
        }
        $sth->bindParam(':limit', $limit, PDO::PARAM_INT);
        $sth->bindParam(':offset', $decalage, PDO::PARAM_INT);
        $sth->execute();

        return $sth->fetchAll(PDO::FETCH_CLASS, 'Alerts');
    }

    public function getAlertUnique($filters = null)
    {
        $whereArgs = [];
        $sql = 'SELECT *
        FROM alertes ';

        if ($filters != null) {
            foreach ($filters as $key => $value) {
                if ($value != '') $whereArgs[] = $key . ' = :' . $key;
            }
        }
        if (!empty($whereArgs)) $sql .= 'WHERE ' . implode(' AND ', $whereArgs);

        $sth = $this->getPDO()->prepare($sql);

        if ($filters != null) {
            if ($filters['id'] != '') $sth->bindParam('id', $filters['id']);
        }
        $sth->execute();

        return $sth->fetchAll(PDO::FETCH_CLASS, 'Alerts');
    }

    public function getDevices()
    {
        $sql = 'SELECT device_product
        FROM alertes
        GROUP BY device_product';

        $sth = $this->getPDO()->prepare($sql, [PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY]);
        $sth->execute();
        return $sth->fetchAll(PDO::FETCH_CLASS, 'Alerts');
    }

    
    public function getnbbygravite($filters = null)
    {
        $i=0;
        $tmp=0;
        $maxrg=0;
        $whereArgs = [];
        if ($filters != null) {
            foreach ($filters as $key) {
                $whereArgs[] = $key;
            }
            $sql = 'SELECT gravite, COUNT(*) as nbbygravite FROM alertes where date>='. implode(' AND ', $whereArgs).' GROUP BY gravite';
        }else {
            $sql = 'SELECT gravite, COUNT(*) as nbbygravite FROM alertes GROUP BY gravite';

        }
        

        $sth = $this->getPDO()->prepare($sql);
        $sth->execute();
        $result = $sth->fetchAll(PDO::FETCH_CLASS, 'Alerts');
        while($i<38)
        {
            if((int)($result[$i]->nbbyespece)>$tmp)
            {
                $tmp=(int)($result[$i]->nbbyespece);
                $maxrg=$i;
            }
            $i++;
        }        
        return $result[$maxrg]->espece;
    }

    // TODO : remplacer par ce qui est demandé
    // public function getnbbyzone($filters = null)
    // {
    //     $i=0;
    //     $tmp=0;
    //     $maxrg=0;
    //     $whereArgs = [];
    //     if ($filters != null) {
    //         foreach ($filters as $key) {
    //             $whereArgs[] = $key;
    //         }
    //         $sql = 'SELECT zone, COUNT(*) as nbbyzone FROM echouage where date>='. implode(' AND ', $whereArgs).' GROUP BY zone';
    //     }else {
    //         $sql = 'SELECT espece, COUNT(*) as nbbyespece FROM echouage GROUP BY espece';
    //     }

        

    //     $sth = $this->getPDO()->prepare($sql);
    //     $sth->execute();
    //     $result = $sth->fetchAll(PDO::FETCH_CLASS, 'Echouage');
    //     while($i<2)
    //     {
    //         if((int)($result[$i]->nbbyzone)>$tmp)
    //         {
    //             $tmp=(int)($result[$i]->nbbyzone);
    //             $maxrg=$i;
    //         }
    //         $i++;
    //     }        
    //     return $result[$maxrg]->zone;
    // }

    // public function getZonesEchouage()
    // {
    //     $sql = 'SELECT zone
    //     FROM echouage
    //     GROUP BY zone';

    //     $sth = $this->getPDO()->prepare($sql, [PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY]);
    //     $sth->execute();
    //     return $sth->fetchAll(PDO::FETCH_CLASS, 'Echouage');
    // }


    public function editEchouage($id, $newCet)
    {
        $sql = "UPDATE echouage 
        SET date=".$newCet['date'].", espece='".$newCet['espece']."', zone='".$newCet['zone']."', nombre=".$newCet['nb']
        ." WHERE id=".$id;

        $sth = $this->getPDO()->prepare($sql);
        $sth->execute();
    }

    // TODO : ajouter commentaires
    // public function addComm($newCet)
    // {
    //     $sql = "INSERT INTO echouage (date, espece, zone, nombre)
    //     VALUES (".$newCet['date'].", '".$newCet['espece']."', '".$newCet['zone']."', ".$newCet['nb'].")";

    //     $sth = $this->getPDO()->prepare($sql);
    //     $sth->execute();
    // }

    public function deleteAlerts($id)
    {
        // $sql = "DELETE from echouage WHERE id=".$id;
        // $sth = $this->getPDO()->prepare($sql);
        // $sth->execute();
    }
}
