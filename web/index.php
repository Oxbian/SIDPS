<?php

ini_set('display_errors', 'on');
error_reporting(E_ALL);

spl_autoload_register(function ($class) {
  include 'class/' . $class . '.class.php';
});

$db = new Database(); 

?>
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">
  <title>IDPS visualization</title>
  <link rel="icon" type="image/x-icon" href="assets/favicon.ico"><!-- Core theme CSS (includes Bootstrap)-->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
  <link href="/css/styles.css" rel="stylesheet">
</head>

<body id="page-top">
  <!-- Navigation-->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" id="mainNav">
    <div class="container px-4"><a class="navbar-brand" href="#page-top">Alerts</a><button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button>
      <div class="collapse navbar-collapse" id="navbarResponsive">
        <ul class="navbar-nav ms-auto">
          <!-- TODO changer ? -->
          <!-- <li class="nav-item"><a class="nav-link" href="/">Accueil</a></li>
          <li class="nav-item"><a class="nav-link" href="#echouage">Liste des échouages</a></li>
          <li class="nav-item"><a class="nav-link" href="add.php">Enregistrer un echouage</a></li>
          <li class="nav-item"><a class="nav-link" href="stats.php">statistiques</a></li> -->
        </ul>
      </div>
    </div>
  </nav><!-- Header-->
  <header class="bg-primary bg-gradient text-white">
    <div class="container px-4 text-center">
      <h1 class="fw-bolder">Alertes systemes</h1>
      <p class="lead">meilleur outil de surveillance du monde</p>
      <a class="btn btn-lg btn-light" href="#alertes">Alertes</a>
    </div>
  </header>

  <section class="bg-light" id="alertes">
    <div class="container px-4">
      <div class="row gx-4 justify-content-center">
        <div class="col-lg-8">
          <h2>Liste des échouages</h2>
          <p class="lead">veuillez selectionner les filtres de recherche ou parcourez la liste ci-dessous</p>

          <form class="row g-3" method="POST">

            <div class="col-auto">
              <select class="form-select" aria-label="Choisir une date" name="date">
                <option selected value="">Année</option>
                <?php for ($i = 1990; $i < 2020; $i++) : ?>
                  <option value="<?php echo $i; ?>"><?php echo $i; ?></option>
                <?php endfor; ?>
              </select>
            </div>

            <div class="col-auto">
              <select class="form-select" aria-label="Chosisir une gravité" name="gravité">
                <option selected value="">Gravité</option>
                <?php
                $especesByType = $db->getAlertsByGravite();
                foreach ($especesByType as $espece) : ?>
                  <option value="<?php echo $espece->Getespece(); ?>"><?php echo $espece->Getespece(); ?></option>
                <?php endforeach; ?>
              </select>
            </div>

            <!-- <div class="col-auto">
              <select class="form-select" aria-label="Chosisir une zone" name="zone">
                <option selected value="">Zone</option>

                <?php
                // $zonesEchouage = $db->getZonesEchouage();
                // foreach ($zonesEchouage as $zone) : ?>
                  <option value="<?php //echo $zone->Getzone(); ?>"><?php// echo $zone->Getzone(); ?></option>
                <?php //endforeach; ?>
              </select>
            </div> -->

            <div class="col-auto ms-auto me-0">
              <button type="submit" class="btn btn-primary mb-3">Filtrer</button>
            </div>
          </form>

          <table class="table table-striped">
            <thead class="bg-primary text-white">
              <tr>
                <th scope="col" class="id">N°</th>
                <th scope="col" class="Date">Date</th>
                <th scope="col" class="label">Espece</th>
                <th scope="col" class="label">Zone</th>
                <th scope="col" class="label">Nombre</th>
                <th scope="col" class="label"></th>
                <th scope="col" class="label"></th>
              </tr>
            </thead>
            <tbody style="border: 1px solid black;">

              <?php
              $echouages = $db->getAlerts($_POST, 20);
              foreach ($echouages as $echouage) : ?>
                <tr style="border: 1px solid black;">
                  <td class="id"><?php echo $echouage->Getid(); ?></td>
                  <td class="id"><?php echo $echouage->Getdate(); ?></td>
                  <td class="label"><a href="info-echouage.php/?id=<?php echo $echouage->Getid(); ?>"><?php echo $echouage->Getespece(); ?></a></td>
                  <td class="label"><?php echo $echouage->Getzone(); ?></td>
                  <td class="label"><?php echo $echouage->Getnombre(); ?></td>
                  <td class="label"><a href="delete.php/?id=<?php echo $echouage->Getid(); ?>">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                      <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                      <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                    </svg></a>
                  </td>
                  <td class="label"><a href="edit.php/?id=<?php echo $echouage->Getid(); ?>">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
                      <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>
                    </svg></a>
                  </td>
                </tr>
              <?php endforeach; ?>

            </tbody>
          </table>
          <nav aria-label="Page navigation">
            <ul class="pagination">
              
              <?php
              $nb_echouage = $db->getnbAlerts();
              $nb_page = ceil($nb_echouage / 20);
              if (isset($_GET["page"])) {
                $page = intval($_GET['page']);
              } else {
                $page = 1;
              }
              echo "<li class='page-item col-auto'><a class='page-link' href=index.php?page=1'>premiere page</a></li>";

              if ($page > 1) {
                echo "<li class='page-item col-auto'><a class='page-link' href=index.php?page=" . strval($page - 1) . "'>" . strval($page - 1) . "</a></li>";
              }

              echo "<li class='page-item col-auto'><a class='page-link' style=href=index.php?page=" . $page . "'>" . $page . "</a></li>";

              if (($page) < $nb_page) {
                echo "<li class='page-item col-auto'><a class='page-link' href=index.php?page=" . strval($page + 1) . "'>" . strval($page + 1) . "</a></li>";
              }

              echo "<li class='page-item col-auto'><a class='page-link' href=index.php?page=" . strval($nb_page) . "'>derniere page</a></li>";
              ?>

            </ul>


          </nav>

              


        </div>
      </div>
    </div>
  </section><!-- Contact section-->




  <footer class="py-5 bg-dark">
    <div class="container px-4">
      <p class="m-0 text-center text-white">Copyright &copy; CIR2 2023/<a class ="text-white" href="https://www.observatoire-pelagis.cnrs.fr/">Pelagis</a></p>
    </div>
  </footer><!-- Bootstrap core JS-->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script><!-- Core theme JS-->
  <!-- <script src="js/scripts.js"></script> -->
</body>

</html>