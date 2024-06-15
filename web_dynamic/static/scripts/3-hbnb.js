$(document).ready(function() {
  // Fetch available places
  $.ajax({
    url: 'http://0.0.0.0:5001/api/v1/places_search/',
    method: 'POST',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify({}), // Empty dictionary in the body
    success: function(data) {
      if (data.status === 'OK') {
        // Loop through each place in the response data
        data.results.forEach(function(place) {
          // Create an article element for each place
          var article = $('<article>');

          // Add class and basic information (assuming structure from your endpoint)
          article.addClass('media');
          article.append($('<div class="media-left">').html('<img class="media-object" src="' + place.images.replace(/\[|\]/g, '') + '" alt="' + place.name + '">'));
          article.append($('<div class="media-body">').html('<h2>' + place.name + '</h2>'));

          // Remove the Owner tag from the description (assuming 'description' field)
          var description = place.description.replace(/Owner.*\n/g, '');
          article.append($('<p>' + description + '</p>'));

          // Append the article to the places section
          $('#section.places').append(article);
        });
      } else {
        console.error('Error fetching places:', data.error);
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.error('Error fetching places:', textStatus, errorThrown);
    }
  });
});
