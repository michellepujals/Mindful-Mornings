/* Divide whole thing into a component, then subdivide into 3 components for 
the 3 colunms, then keep subdividing until down to the smallest components 
(ie a task is a component and can be reused) */

//Code for map//

function initMap() {
    let directionsService = new google.maps.DirectionsService;
    let directionsDisplay = new google.maps.DirectionsRenderer;
    let myHome = new google.maps.LatLng(37.783581,-122.203272);
    let bootcamp = new google.maps.LatLng(37.803135, -122.266952)
     let mapOptions =  {
        zoom: 10, 
        center: myHome
    }
    let map = new google.maps.Map(document.getElementById('map'), mapOptions);
    directionsDisplay.setMap(map);
    directionsDisplay.setPanel(document.getElementById('directionsPanel'));
    let marker = new google.maps.Marker({position: myHome, map: map});
    calculateAndDisplayRoute(directionsService, directionsDisplay);
    document.getElementById('mode').addEventListener('change', function() {
        calculateAndDisplayRoute(directionsService, directionsDisplay);
    });
}


function calculateAndDisplayRoute(directionsService, directionsDisplay) {
    let selectedMode = document.getElementById('mode').value;
    let myHome = new google.maps.LatLng(37.783581,-122.203272);
    let bootcamp = new google.maps.LatLng(37.803135, -122.266952)
    //let start = document.getElementById('start').value;
    //let end = document.getElementById('end').value;
    let request = {
        origin:myHome,
        destination:bootcamp,
        travelMode: google.maps.TravelMode[selectedMode]
    };
    directionsService.route(request, function(response, status) {
          if (status == 'OK') {
            directionsDisplay.setDirections(response);
          } else {
            window.alert('Directions request failed due to ' + status);
          }
    });
}
