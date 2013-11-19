var map, team_one_points, team_two_points, team_one_map, team_two_map;
var team_one_points = []
var team_two_points = [];

var team_one_gradient = [
    'rgba(0, 255, 255, 0)',
    'rgba(0, 255, 255, 1)',
    'rgba(0, 191, 255, 1)',
    'rgba(0, 127, 255, 1)',
    'rgba(0, 63, 255, 1)',
    'rgba(0, 0, 255, 1)',
    'rgba(0, 0, 223, 1)',
    'rgba(0, 0, 191, 1)',
    'rgba(0, 0, 159, 1)',
    'rgba(0, 0, 127, 1)',
    'rgba(63, 0, 91, 1)',
    'rgba(127, 0, 63, 1)',
    'rgba(191, 0, 31, 1)',
    'rgba(255, 0, 0, 1)'
  ]

function initialize() {
    var mapOptions = {
        zoom: 4,
        center: new google.maps.LatLng(39.8282, -98.5795),
        mapTypeId: google.maps.MapTypeId.MAP
    };

    map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);

    json = $('#point_data').html() 
    var obj = jQuery.parseJSON( json );
    
    for (var i=0; i<obj.team_one_coordinates.length; i++){
         team_one_points.push(new google.maps.LatLng(obj.team_one_coordinates[i][0], obj.team_one_coordinates[i][1]));
    };
    for (var i=0; i<obj.team_two_coordinates.length; i++){
         team_two_points.push(new google.maps.LatLng(obj.team_two_coordinates[i][0], obj.team_two_coordinates[i][1]));
    };


    var one_points = new google.maps.MVCArray(team_one_points);
    team_one_map = new google.maps.visualization.HeatmapLayer({
        data: one_points,
        radius: 20,
        gradient: null
    });
    team_one_map.setMap(map);


    var two_points = new google.maps.MVCArray(team_two_points);
    teamp_two_map = new google.maps.visualization.HeatmapLayer({
        data: two_points,
        radius: 15,
        gradient: team_one_gradient
    });
    teamp_two_map.setMap(map);
}

google.maps.event.addDomListener(window, 'load', initialize);

{% autoescape true %}
$('document').write({{ popped }})
{% endautoescape %}