'use strict';

// initialisation 
let previousAlerts = [];
let sortOrder = {};

ajaxRequest('GET', 'php/request.php/alertes/', CheckNewAlerts);
ajaxRequest('GET', 'php/request.php/devices/', fillSelectDevice);
fillSelectRisque();

setInterval(() => {
  ajaxRequest('GET', 'php/request.php/alertes/', CheckNewAlerts);
}, 10000);

// initialisation of the filters
$('#filter-button').click(() => {
  const params = []; 
  const device = $('#device-select').val();
  const alertlvl = $('#risque-select').val();

  // enable parameters only if they are not empty
  if (device) params.push(`device_product=${encodeURIComponent(device)}`);
  if (alertlvl) params.push(`agent_severity=${encodeURIComponent(alertlvl)}`);

  // build the url
  let url;
  if (params.length) {
    url = `php/request.php/alertes/?${params.join('&')}`;
    console.log(url);
  } else {
    url = 'php/request.php/alertes/';
    console.log(url);
  }

  ajaxRequest('GET', url, displayAlerts);
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
        $('<td>').text(alert['src'] + ":" + alert['spt']),
        $('<td>').text(alert['dst'] + ":" + alert['dpt']),
        $('<td>').text(alert['agent_severity']),
        $('<td>').text(alert['reason'])
      )
    );
}

//------------------------------------------------------------------------------
//--- fillSelectDevice ------------------------------------------------------------
//------------------------------------------------------------------------------
// fill select with devices.
// \param devices The devices data received via the Ajax request.
function fillSelectDevice(devices) {
  for (let device of devices)
    $('#device-select').append($('<option>').text(device['device_product']).val(device['device_product']));
}

//------------------------------------------------------------------------------
//--- fillSelectRisque ------------------------------------------------------------
//------------------------------------------------------------------------------
// fill select with alertslvl.
function fillSelectRisque() {
  for (let i = 1; i <= 10; i++)
    $('#risque-select').append($('<option>').text(i).val(i));
}

//------------------------------------------------------------------------------
//--- CheckNewAlerts ------------------------------------------------------------
//------------------------------------------------------------------------------
// checks if there is new alerts in the database and display if so.
// \param newAlerts The alerts data received via the Ajax request.
// \previousAlerts The old alerts data received via the Ajax request and stored.
function CheckNewAlerts(newAlerts) {
  if (JSON.stringify(previousAlerts) !== JSON.stringify(newAlerts)) {
    displayAlerts(newAlerts);
    previousAlerts = newAlerts;
  }
}

//------------------------------------------------------------------------------
//--- sortTable ------------------------------------------------------------
//------------------------------------------------------------------------------
// sort the table.
// \param columnName The name of the column to sort.
function sortTable(columnName) {
  const currentOrder = sortOrder[columnName] || 'asc';
  const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
  sortOrder[columnName] = newOrder;

  const params = [];
  params.push(`orderby=${columnName}`);
  params.push(`order=${newOrder}`);

  const url = `php/request.php/alertes/?${params.join('&')}`;

  ajaxRequest('GET', url, displayAlerts);
}

// sort the table when clicking on the column name
$('th').click(function () {
  let columnName = $(this).text().trim().toLowerCase().replace(/ /g, '_'); 
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