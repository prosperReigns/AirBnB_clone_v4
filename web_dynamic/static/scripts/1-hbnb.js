$(document).ready(function() {
  // Initialize an empty array to store amenity IDs
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

    // Update the h4 tag content inside the div with the Amenities list
    var amenityListString = selectedAmenities.join(', ');
    $('#amenities h4').text('Amenities: ' + amenityListString);
  });
});
