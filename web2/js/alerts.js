'use strict';

// initialisation 
ajaxRequest('GET', 'php/request.php/alertes/', displayAlerts);
ajaxRequest('GET', 'php/request.php/devices/', fillSelectDevice);
fillSelectRisque();


// filtrage
$('#filter-button').click(() => {
  const params = []; // Initialise le tableau des paramètres
  const device = $('#device-select').val();
  const alertlvl = $('#risque-select').val();
  console.log("device =" + device);
  console.log("alertlvl =" + alertlvl);
  
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

$('#tweets').on('click', '.mod', () => {
  ajaxRequest('PUT', 'php/request.php/tweets/' +
    $(event.target).closest('.mod').attr('value'), () => {
    ajaxRequest('GET', 'php/request.php/tweets/', displayTweets);
  }, 'login=' + login + '&text=' + prompt('Nouveau tweet :'));
}
);
$('#tweets').on('click', '.del', () => {
  console.log('delete');
  ajaxRequest('DELETE', 'php/request.php/tweets/' +
    $(event.target).closest('.del').attr('value') + '?login=' + login, () => {
    ajaxRequest('GET', 'php/request.php/tweets/', displayTweets);
  }
  );
}
);

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