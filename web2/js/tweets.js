'use strict';

let login = 'cir2';
let currentTitle = 'Liste des tweets';

ajaxRequest('GET', 'php/request.php/tweets/', displayTweets);

$('#all-button').click(() =>
  {
    currentTitle = 'Liste des tweets';
    ajaxRequest('GET', 'php/request.php/tweets/', displayTweets);
  }
);

$('#my-button').click(() =>
  {
    currentTitle = 'Liste de mes tweets';
    ajaxRequest('GET', 'php/request.php/tweets/?login=' + login, displayTweets);
  }
);

$('#tweet-add').submit((event) =>
  {
    event.preventDefault();
    ajaxRequest('POST', 'php/request.php/tweets/', () =>
      {
        ajaxRequest('GET', 'php/request.php/tweets/', displayTweets);
      }, 'login=' + login + '&text=' + $('#tweet').val());
    $('#tweet').val('');
  }
);

$('#tweets').on('click', '.mod', () =>
  {
    ajaxRequest('PUT', 'php/request.php/tweets/' +
      $(event.target).closest('.mod').attr('value'), () =>
        {
          ajaxRequest('GET', 'php/request.php/tweets/', displayTweets);
        }, 'login=' + login + '&text=' + prompt('Nouveau tweet :'));
  }
);
$('#tweets').on('click', '.del', () =>
  {
    console.log('delete');
    ajaxRequest('DELETE', 'php/request.php/tweets/' +
      $(event.target).closest('.del').attr('value') +'?login=' + login, () =>
        {
          ajaxRequest('GET', 'php/request.php/tweets/', displayTweets);
        }
      );
  }
);

//------------------------------------------------------------------------------
//--- displayTweets ------------------------------------------------------------
//------------------------------------------------------------------------------
// Display tweets.
// \param tweets The tweets data received via the Ajax request.
function displayTweets(tweets)
{
  // Fill tweets.
  $('#tweets').html('<h3>' + currentTitle + '</h3>');
  for (let tweet of tweets)
    $('#tweets').append('<div class="card"><div class="card-body">' +
      tweet.login + ' : ' + tweet.text +
      '<div class="btn-group float-right" role="group">' +
      '<button type="button" class="btn btn-light float-right mod"' +
      ' value="' + tweet.id + '"><i class="fa fa-edit"></i></button>' +
      '<button type="button" class="btn btn-light float-right del"' +
      ' value="' + tweet.id + '"><i class="fa fa-trash"></i></button>' +
      '<div></div></div>');
}
