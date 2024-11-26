'use strict';

// initialisation 
let previousAlerts = [];
let sortOrder = {};
ajaxRequest('GET', 'php/request.php/alertes/', CheckNewAlerts);

// ajaxRequest('GET', 'php/request.php/alertes/', displayAlerts);
setInterval(() => {
  ajaxRequest('GET', 'php/request.php/alertes/', CheckNewAlerts);
  // Effectuer une requête AJAX pour récupérer les nouvelles alertes
}, 10000);
ajaxRequest('GET', 'php/request.php/devices/', fillSelectDevice);
fillSelectRisque();

// filtrage
$('#filter-button').click(() => {
  const params = []; // Initialise le tableau des paramètres
  const device = $('#device-select').val();
  const alertlvl = $('#risque-select').val();
  
  // Ajouter les paramètres uniquement s'ils sont définis
  if (device) params.push(`device_product=${encodeURIComponent(device)}`);
  if (alertlvl) params.push(`agent_severity=${encodeURIComponent(alertlvl)}`);
  
  // Construire l'URL avec les paramètres
  let url;
  if (params.length) {
    url = `php/request.php/alertes/?${params.join('&')}`;
    console.log(url);
  } else {
    url = 'php/request.php/alertes/';
    console.log(url);
  }
  
  // Effectuer la requête AJAX
  ajaxRequest('GET', url, displayAlerts); 
}
);


// $('#tweets').on('click', '.del', () => {
//   console.log('delete');
//   ajaxRequest('DELETE', 'php/request.php/tweets/' +
//     $(event.target).closest('.del').attr('value') + '?login=' + login, () => {
//     ajaxRequest('GET', 'php/request.php/tweets/', displayTweets);
//   }
//   );
// }
// );

//------------------------------------------------------------------------------
//--- displayAlerts ------------------------------------------------------------
//------------------------------------------------------------------------------
// Display alerts.
// \param alerts The alerts data received via the Ajax request.
function displayAlerts(alerts) {
  // Clear the table.
  $('#tab-alert').empty();
  // Fill alerts.
  console.log(alerts);
  for (let alert of alerts)
    $('#tab-alert').append(
      $('<tr>').append(
        $('<td>').text(alert['id']),
        $('<td>').text(alert['date_alerte']),
        $('<td>').text(alert['name']),
        $('<td>').text(alert['device_product']),
        $('<td>').text(alert['src']+":"+alert['spt']),
        $('<td>').text(alert['dst']+":"+alert['dpt']),
        $('<td>').text(alert['agent_severity']),
        $('<td>').text(alert['reason'])
      )
    );
}

function fillSelectDevice(devices) {
  for (let device of devices)
    $('#device-select').append($('<option>').text(device['device_product']).val(device['device_product']));
}

function fillSelectRisque() {
  for (let i = 1; i <= 10; i++)
    $('#risque-select').append($('<option>').text(i).val(i));
}

function CheckNewAlerts(newAlerts) {
  // Comparer les nouvelles alertes avec les anciennes
  if (JSON.stringify(previousAlerts) !== JSON.stringify(newAlerts)) {
      // Si les alertes ont changé, mettre à jour l'interface
      displayAlerts(newAlerts);
      
      // Mettre à jour les alertes précédentes
      previousAlerts = newAlerts;
  }
}

// Fonction pour trier les alertes
function sortTable(columnName) {
  const currentOrder = sortOrder[columnName] || 'asc';
  const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
  sortOrder[columnName] = newOrder;

  // Construire les paramètres de la requête pour l'orderby
  const params = [];
  params.push(`orderby=${columnName}`);
  params.push(`order=${newOrder}`);

  const url = `php/request.php/alertes/?${params.join('&')}`;

  // Effectuer la requête AJAX pour récupérer les alertes triées
  ajaxRequest('GET', url, displayAlerts);
}

// Ajouter des gestionnaires d'événements de clic sur les en-têtes de colonnes
$('th').click(function() {
  let columnName = $(this).text().trim().toLowerCase().replace(/ /g, '_'); // Convertir le texte de l'en-tête en nom de colonne
  console.log(columnName);
  switch (columnName) {
    case 'n°':
      columnName = 'id';
      break;
    case 'date':
      columnName = 'date_alerte';
      break;
    case 'nom_alerte':
      columnName = 'name';
      break;
    case 'appareil_de_détection':
      columnName = 'device_product';
      break;
    case 'adresse_source':
      columnName = 'src';
      break;
    case 'adresse_destination':
      columnName = 'dst';
      break;
    case 'niveau_d\'alerte':
      columnName = 'agent_severity';
      break;
    case 'raison':
      columnName = 'reason';
      break;
  }
  sortTable(columnName);
});