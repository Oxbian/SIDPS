<?php

class Alerts
{
    // Attributs privés
    private $id;
    private $cef_version;
    private $date_alerte;
    private $event_gravite;
    private $device_product;
    private $device_vendor;
    private $device_version;
    private $alerte_name;
    private $destinationAddress;
    private $sourceAddress;
    private $destinationPort;
    private $sourcePort;
    private $protocol;
    private $applicationProtocol;
    private $reason;
    private $action;
    private $commentaire;

    // Getter et Setter pour id
    public function getId()
    {
        return $this->id;
    }

    public function setId($id)
    {
        $this->id = $id;
    }

    // Getter et Setter pour cef_version
    public function getCefVersion()
    {
        return $this->cef_version;
    }

    public function setCefVersion($cef_version)
    {
        $this->cef_version = $cef_version;
    }

    // Getter et Setter pour date_alerte
    public function getDateAlerte()
    {
        return $this->date_alerte;
    }

    public function setDateAlerte($date_alerte)
    {
        $this->date_alerte = $date_alerte;
    }

    // Getter et Setter pour event_gravite
    public function getEventGravite()
    {
        return $this->event_gravite;
    }

    public function setEventGravite($event_gravite)
    {
        $this->event_gravite = $event_gravite;
    }

    // Getter et Setter pour device_product
    public function getDeviceProduct()
    {
        return $this->device_product;
    }

    public function setDeviceProduct($device_product)
    {
        $this->device_product = $device_product;
    }

    // Getter et Setter pour device_vendor
    public function getDeviceVendor()
    {
        return $this->device_vendor;
    }

    public function setDeviceVendor($device_vendor)
    {
        $this->device_vendor = $device_vendor;
    }

    // Getter et Setter pour device_version
    public function getDeviceVersion()
    {
        return $this->device_version;
    }

    public function setDeviceVersion($device_version)
    {
        $this->device_version = $device_version;
    }

    // Getter et Setter pour alerte_name
    public function getAlerteName()
    {
        return $this->alerte_name;
    }

    public function setAlerteName($alerte_name)
    {
        $this->alerte_name = $alerte_name;
    }

    // Getter et Setter pour destinationAddress
    public function getDestinationAddress()
    {
        return $this->destinationAddress;
    }

    public function setDestinationAddress($destinationAddress)
    {
        $this->destinationAddress = $destinationAddress;
    }

    // Getter et Setter pour sourceAddress
    public function getSourceAddress()
    {
        return $this->sourceAddress;
    }

    public function setSourceAddress($sourceAddress)
    {
        $this->sourceAddress = $sourceAddress;
    }

    // Getter et Setter pour destinationPort
    public function getDestinationPort()
    {
        return $this->destinationPort;
    }

    public function setDestinationPort($destinationPort)
    {
        $this->destinationPort = $destinationPort;
    }

    // Getter et Setter pour sourcePort
    public function getSourcePort()
    {
        return $this->sourcePort;
    }

    public function setSourcePort($sourcePort)
    {
        $this->sourcePort = $sourcePort;
    }

    // Getter et Setter pour protocol
    public function getProtocol()
    {
        return $this->protocol;
    }

    public function setProtocol($protocol)
    {
        $this->protocol = $protocol;
    }

    // Getter et Setter pour applicationProtocol
    public function getApplicationProtocol()
    {
        return $this->applicationProtocol;
    }

    public function setApplicationProtocol($applicationProtocol)
    {
        $this->applicationProtocol = $applicationProtocol;
    }

    // Getter et Setter pour reason
    public function getReason()
    {
        return $this->reason;
    }

    public function setReason($reason)
    {
        $this->reason = $reason;
    }

    // Getter et Setter pour action
    public function getAction()
    {
        return $this->action;
    }

    public function setAction($action)
    {
        $this->action = $action;
    }

    // Getter et Setter pour commentaire
    public function getCommentaire()
    {
        return $this->commentaire;
    }

    public function setCommentaire($commentaire)
    {
        $this->commentaire = $commentaire;
    }
}

?>
