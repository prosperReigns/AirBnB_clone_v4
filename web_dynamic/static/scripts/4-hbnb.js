$(document).ready(function() {
  // Initialize an empty array to store selected amenity IDs
  var selectedAmenities = [];

  // Listen for changes on all checkbox tags with the class 'amenity-checkbox'
  $('.amenity-checkbox').change(function() {
    var amenityId = $(this).val(); // Get the Amenity ID from the checkbox value

    if ($(this).is(':checked')) {
      // Checkbox is checked, add the Amenity ID to the array (if not already present)
      if (!selectedAmenities.includes(amenityId)) {
        selectedAmenities.push(amenityId);
      }
    } else {
      // Checkbox is unchecked, remove the Amenity ID from the array
      var index = selectedAmenities.indexOf(amenityId);
      if (index > -1) {
        selectedAmenities.splice(index, 1);
      }
    }
  });

  // Function to send the POST request with selected amenities
  function searchPlaces() {
    $.ajax({
      url: 'http://0.0.0.0:5001/api/v1/places_search/',
      method: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ amenities: selectedAmenities }),
      success: function(data) {
        if (data.status === 'OK') {
          // Clear existing places before rendering new results
          $('#section.places').empty();

          // Loop through and display places as in 3-hbnb.js (modify selectors if needed)
          data.results.forEach(function(place) {
            var article = $('<article>');
            article.addClass('media');
            article.append($('<div class="media-left">').html('<img class="media-object" src="' + place.images.replace(/\[|\]/g, '') + '" alt="' + place.name + '">'));
            article.append($('<div class="media-body">').html('<h2>' + place.name + '</h2>'));
            var description = place.description.replace(/Owner.*\n/g, '');
            article.append($('<p>' + description + '</p>'));
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
  }

  // Attach click event listener to the button
  $('#search_button').click(function() {
    searchPlaces();
  });
});
