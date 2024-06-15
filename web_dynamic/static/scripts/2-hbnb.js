$(document).ready(function() {
  // Fetch the API status
  $.ajax({
    url: 'http://0.0.0.0:5001/api/v1/status/',
    dataType: 'json',
    success: function(data) {
      if (data.status === 'OK') {
        $('#api_status').addClass('available');
      } else {
        $('#api_status').removeClass('available');
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.error('Error fetching API status:', textStatus, errorThrown);
    }
  });
});
