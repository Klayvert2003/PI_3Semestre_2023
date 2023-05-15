function initMap() {
    var lat = document.querySelector('#lat').textContent;
    var lon = document.querySelector('#lon').textContent;
    var map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: parseFloat(lat), lng: parseFloat(lon)},
      zoom: 16,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      disableDefaultUI: true,
      zoomControl: true,
      gestureHandling: 'cooperative',
      styles: [
        {
          "featureType": "poi",
          "stylers": [
            { "visibility": "on" }
          ]
        }
      ]
    });
    var marker = new google.maps.Marker({
      position: {lat: parseFloat(lat), lng: parseFloat(lon)},
      map: map,
      title: 'Minha localização'
    });
  }