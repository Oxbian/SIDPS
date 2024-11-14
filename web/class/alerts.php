<?php

class Alerts
{
    //attributs  TDO change names
    private $id;
    private $date;
    public $espece;
    public $zone;
    private $nombre;

    //methodes TODO : changes names
    public function Getid()
    {
        return $this->id;
    }
    public function Getdate()
    {
        return $this->date;
    }
    public function Getespece()
    {
        return $this->espece;
    }
    public function Getzone()
    {
        return $this->zone;
    }
    public function Getnombre()
    {
        return $this->nombre;
    }

    public function Setid($id)
    {
        $this->id = $id;
    }
    public function Setdate($date)
    {
        $this->date = $date;
    }
    public function Setespece($espece)
    {
        $this->espece = $espece;
    }
    public function Setzone($zone)
    {
        $this->zone = $zone;
    }
    public function Setnombre($nombre)
    {
        $this->nombre = $nombre;
    }

    // function __construct($id, $date, $espece, $zone, $nombre)
    // {
    //     $this->$id = $id;
    //     $this->$date = $date;
    //     $this->$espece = $espece;
    //     $this->$zone = $zone;
    //     $this->$nombre = $nombre;
    // }
}
