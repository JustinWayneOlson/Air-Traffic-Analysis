$(document).ready(function() {
    $('#grid-size').slider({
        formatter: function(value) {
            return 'Current value: ' + value;
        }
    });

    $('#altitude').slider({
        formatter: function(value) {
            return 'Current value: ' + value;
        }
    });

    $.ajax({
        type: "GET",
        url: "/dropdown-fill/Dest",
        success: function(data) {
            $('#Dest').select2({
                data: data['response'],
                placeholder: "Select an option"
            });
        },
        error: function(error) {
            console.log(error);
        }
    });

    $.ajax({
        type: "GET",
        url: "/computed-routes",
        success: function(data) {
            var menu_data = $.map(data['response'], function(value, index) {
                return value['jobName'];
            });
            console.log(menu_data);
            $('#routes').select2({
                data: menu_data,
                placeholder: "Select an already computed route."
            });
        },
        error: function(error) {
            console.log(error);
        }
    });



    $.ajax({
        type: "GET",
        url: "/dropdown-fill/Origin",
        success: function(data) {
            $('#Origin').select2({
                data: data['response'],
                placeholder: "Select an option"
            });
        },
        error: function(error) {
            console.log(error);
        }
    });


    $('#options').select2({
        data: ["Suggested routes based on filter options", "Routes selected for computation"],
        dropdownAutoWidth: true
    });


    $("#compute").on('click', function() {
        if($('#json-input').val()) {
            var post_object = JSON.parse($('#json-input').val().replace(/\'/g, '"'));
        } else {
            var post_object = {
                'jobName': $('#compute-name').val(),
                'Origin': $('#Origin').val(),
                'Dest': $('#Dest').val(),
                'gridResPlanar': $('#grid-size').val(),
                'gridResVert': $('#altitude').val(),
                'heuristic': $('#heuristic').val()
            };
        }
        $.ajax({
            url: "/routing-compute",
            type: "POST",
            data: JSON.stringify(post_object),
            success: function(new_data) {
                $.ajax({
                    type: "GET",
                    url: "/computed-routes",
                    success: function(data) {
                        var menu_data = $.map(data['response'], function(value, index) {
                            return value['jobName'];
                        });
                        menu_data.push(new_data['response'])
                        console.log(menu_data);
                        $('#routes').select2({
                            data: menu_data,
                            placeholder: "Select an already computed route."
                        }).trigger('change');
                    },
                    error: function(error) {
                        console.log(error);
                    }
                   });
               },
               error: function(error) {
                   console.log(error);
               }
           });
    });

    $("#plot").on('click', function() {
            $.ajax({
                    url: "/display-route/" + $('#routes').val(),
                    type: "GET",
                    success: function(response_data) {
                       //var data = JSON.parse('{"nodes":[{"Color":"white","lat":36.080056,"Name":"LAS","long":-115.15225},{"TotalDelay":186,"Name":"MCI","TotalFlights":3,"Color":"yellow","TotalDelayedFlights":2,"NASDelay":186,"SecurityDelayTot":0,"CarrierDelayTot":0,"long":-94.71390500000001,"WeatherDelayTot":0,"WeatherDelay":0,"SecurityDelay":0,"NASDelayTot":2,"lat":39.297606,"LateAircraftDelayTot":0,"LateAircraftDelay":0,"CarrierDelay":0},{"TotalDelay":267,"Name":"SAN","TotalFlights":2,"Color":"red","TotalDelayedFlights":1,"NASDelay":267,"SecurityDelayTot":0,"CarrierDelayTot":0,"long":-117.18966699999999,"WeatherDelayTot":0,"WeatherDelay":0,"SecurityDelay":0,"NASDelayTot":1,"lat":32.733556,"LateAircraftDelayTot":0,"LateAircraftDelay":0,"CarrierDelay":0},{"TotalDelay":76,"Name":"MSY","TotalFlights":2,"Color":"green","TotalDelayedFlights":1,"NASDelay":76,"SecurityDelayTot":0,"CarrierDelayTot":0,"long":-90.258028,"WeatherDelayTot":0,"WeatherDelay":0,"SecurityDelay":0,"NASDelayTot":1,"lat":29.993389,"LateAircraftDelayTot":0,"LateAircraftDelay":0,"CarrierDelay":0},{"TotalDelay":70,"Name":"PHL","TotalFlights":2,"Color":"green","TotalDelayedFlights":1,"NASDelay":70,"SecurityDelayTot":0,"CarrierDelayTot":0,"long":-75.241139,"WeatherDelayTot":0,"WeatherDelay":0,"SecurityDelay":0,"NASDelayTot":1,"lat":39.871944,"LateAircraftDelayTot":0,"LateAircraftDelay":0,"CarrierDelay":0},{"TotalDelay":23,"Name":"DFW","TotalFlights":2,"Color":"green","TotalDelayedFlights":1,"NASDelay":23,"SecurityDelayTot":0,"CarrierDelayTot":0,"long":-97.037997,"WeatherDelayTot":0,"WeatherDelay":0,"SecurityDelay":0,"NASDelayTot":1,"lat":32.896828,"LateAircraftDelayTot":0,"LateAircraftDelay":0,"CarrierDelay":0},{"TotalDelay":179,"Name":"BOS","TotalFlights":2,"Color":"red","TotalDelayedFlights":1,"NASDelay":179,"SecurityDelayTot":0,"CarrierDelayTot":0,"long":-71.00518100000001,"WeatherDelayTot":0,"WeatherDelay":0,"SecurityDelay":0,"NASDelayTot":1,"lat":42.364346999999995,"LateAircraftDelayTot":0,"LateAircraftDelay":0,"CarrierDelay":0},{"TotalDelay":24,"Name":"OAK","TotalFlights":2,"Color":"green","TotalDelayedFlights":1,"NASDelay":24,"SecurityDelayTot":0,"CarrierDelayTot":0,"long":-122.220722,"WeatherDelayTot":0,"WeatherDelay":0,"SecurityDelay":0,"NASDelayTot":1,"lat":37.721278000000005,"LateAircraftDelayTot":0,"LateAircraftDelay":0,"CarrierDelay":0},{"TotalDelay":762,"Name":"MSP","TotalFlights":10,"Color":"red","TotalDelayedFlights":9,"NASDelay":762,"SecurityDelayTot":0,"CarrierDelayTot":0,"long":-93.221767,"WeatherDelayTot":0,"WeatherDelay":0,"SecurityDelay":0,"NASDelayTot":9,"lat":44.881956,"LateAircraftDelayTot":0,"LateAircraftDelay":0,"CarrierDelay":0},{"TotalDelay":29,"Name":"LAX","TotalFlights":2,"Color":"green","TotalDelayedFlights":1,"NASDelay":29,"SecurityDelayTot":0,"CarrierDelayTot":0,"long":-118.408075,"WeatherDelayTot":0,"WeatherDelay":0,"SecurityDelay":0,"NASDelayTot":1,"lat":33.942536,"LateAircraftDelayTot":0,"LateAircraftDelay":0,"CarrierDelay":0},{"TotalDelay":340,"Name":"FLL","TotalFlights":7,"Color":"green","TotalDelayedFlights":6,"NASDelay":150,"SecurityDelayTot":0,"CarrierDelayTot":3,"long":-80.15275,"WeatherDelayTot":0,"WeatherDelay":0,"SecurityDelay":0,"NASDelayTot":6,"lat":26.072582999999998,"LateAircraftDelayTot":1,"LateAircraftDelay":108,"CarrierDelay":82},{"TotalDelay":1360,"Name":"SEA","TotalFlights":18,"Color":"red","TotalDelayedFlights":17,"NASDelay":825,"SecurityDelayTot":1,"CarrierDelayTot":6,"long":-122.309306,"WeatherDelayTot":1,"WeatherDelay":0,"SecurityDelay":0,"NASDelayTot":13,"lat":47.449,"LateAircraftDelayTot":2,"LateAircraftDelay":211,"CarrierDelay":324},{"TotalDelay":0,"Name":"BWI","TotalFlights":1,"Color":"green","TotalDelayedFlights":0,"NASDelay":0,"SecurityDelayTot":0,"CarrierDelayTot":0,"long":-76.66833299999999,"WeatherDelayTot":0,"WeatherDelay":0,"SecurityDelay":0,"NASDelayTot":0,"lat":39.175360999999995,"LateAircraftDelayTot":0,"LateAircraftDelay":0,"CarrierDelay":0},{"TotalDelay":119,"Name":"ORD","TotalFlights":2,"Color":"yellow","TotalDelayedFlights":1,"NASDelay":119,"SecurityDelayTot":0,"CarrierDelayTot":0,"long":-87.904842,"WeatherDelayTot":0,"WeatherDelay":0,"SecurityDelay":0,"NASDelayTot":1,"lat":41.978603,"LateAircraftDelayTot":0,"LateAircraftDelay":0,"CarrierDelay":0},{"TotalDelay":213,"Name":"DTW","TotalFlights":4,"Color":"yellow","TotalDelayedFlights":3,"NASDelay":213,"SecurityDelayTot":0,"CarrierDelayTot":0,"long":-83.353389,"WeatherDelayTot":0,"WeatherDelay":0,"SecurityDelay":0,"NASDelayTot":3,"lat":42.212444,"LateAircraftDelayTot":0,"LateAircraftDelay":0,"CarrierDelay":0},{"TotalDelay":147,"Name":"ATL","TotalFlights":6,"Color":"green","TotalDelayedFlights":5,"NASDelay":66,"SecurityDelayTot":0,"CarrierDelayTot":1,"long":-84.428067,"WeatherDelayTot":0,"WeatherDelay":0,"SecurityDelay":0,"NASDelayTot":4,"lat":33.636719,"LateAircraftDelayTot":1,"LateAircraftDelay":75,"CarrierDelay":6},{"TotalDelay":744,"Name":"IAH","TotalFlights":5,"Color":"red","TotalDelayedFlights":4,"NASDelay":662,"SecurityDelayTot":1,"CarrierDelayTot":1,"long":-95.341442,"WeatherDelayTot":1,"WeatherDelay":0,"SecurityDelay":0,"NASDelayTot":4,"lat":29.984433000000003,"LateAircraftDelayTot":1,"LateAircraftDelay":0,"CarrierDelay":82}],"links":[{"source":0,"target":13},{"source":0,"target":4},{"source":0,"target":2},{"source":0,"target":16},{"source":0,"target":5},{"source":0,"target":14},{"source":0,"target":15},{"source":0,"target":12},{"source":0,"target":9},{"source":0,"target":7},{"source":0,"target":11},{"source":0,"target":8},{"source":0,"target":10},{"source":0,"target":3},{"source":0,"target":1},{"source":0,"target":6}]}');
                       var data = JSON.parse(response_data['response']['routeLines']);
                       console.log(data);


                        var map = new google.maps.Map(d3.select("#map").node(), {
                            zoom: 4,
                            center: new google.maps.LatLng(52, -133),
                            mapTypeId: google.maps.MapTypeId.TERRAIN,
                            styles: [{
                                    "elementType": "geometry",
                                    "stylers": [{
                                        "color": "#212121"
                                    }]
                                },
                                {
                                    "elementType": "labels.icon",
                                    "stylers": [{
                                        "visibility": "off"
                                    }]
                                },
                                {
                                    "elementType": "labels.text.fill",
                                    "stylers": [{
                                        "color": "#757575"
                                    }]
                                },
                                {
                                    "elementType": "labels.text.stroke",
                                    "stylers": [{
                                        "color": "#212121"
                                    }]
                                },
                                {
                                    "featureType": "administrative",
                                    "elementType": "geometry",
                                    "stylers": [{
                                            "color": "#757575"
                                        },
                                        {
                                            "visibility": "off"
                                        }
                                    ]
                                },
                                {
                                    "featureType": "administrative.country",
                                    "elementType": "labels.text.fill",
                                    "stylers": [{
                                        "color": "#9e9e9e"
                                    }]
                                },
                                {
                                    "featureType": "administrative.land_parcel",
                                    "stylers": [{
                                        "visibility": "off"
                                    }]
                                },
                                {
                                    "featureType": "administrative.locality",
                                    "elementType": "labels.text.fill",
                                    "stylers": [{
                                        "color": "#bdbdbd"
                                    }]
                                },
                                {
                                    "featureType": "administrative.neighborhood",
                                    "stylers": [{
                                        "visibility": "off"
                                    }]
                                },
                                {
                                    "featureType": "poi",
                                    "stylers": [{
                                        "visibility": "off"
                                    }]
                                },
                                {
                                    "featureType": "poi",
                                    "elementType": "labels.text",
                                    "stylers": [{
                                        "visibility": "off"
                                    }]
                                },
                                {
                                    "featureType": "poi",
                                    "elementType": "labels.text.fill",
                                    "stylers": [{
                                        "color": "#757575"
                                    }]
                                },
                                {
                                    "featureType": "poi.park",
                                    "elementType": "geometry",
                                    "stylers": [{
                                        "color": "#181818"
                                    }]
                                },
                                {
                                    "featureType": "poi.park",
                                    "elementType": "labels.text.fill",
                                    "stylers": [{
                                        "color": "#616161"
                                    }]
                                },
                                {
                                    "featureType": "poi.park",
                                    "elementType": "labels.text.stroke",
                                    "stylers": [{
                                        "color": "#1b1b1b"
                                    }]
                                },
                                {
                                    "featureType": "road",
                                    "stylers": [{
                                        "visibility": "off"
                                    }]
                                },
                                {
                                    "featureType": "road",
                                    "elementType": "geometry.fill",
                                    "stylers": [{
                                        "color": "#2c2c2c"
                                    }]
                                },
                                {
                                    "featureType": "road",
                                    "elementType": "labels",
                                    "stylers": [{
                                        "visibility": "off"
                                    }]
                                },
                                {
                                    "featureType": "road",
                                    "elementType": "labels.icon",
                                    "stylers": [{
                                        "visibility": "off"
                                    }]
                                },
                                {
                                    "featureType": "road",
                                    "elementType": "labels.text.fill",
                                    "stylers": [{
                                        "color": "#8a8a8a"
                                    }]
                                },
                                {
                                    "featureType": "road.arterial",
                                    "elementType": "geometry",
                                    "stylers": [{
                                        "color": "#373737"
                                    }]
                                },
                                {
                                    "featureType": "road.highway",
                                    "elementType": "geometry",
                                    "stylers": [{
                                        "color": "#3c3c3c"
                                    }]
                                },
                                {
                                    "featureType": "road.highway.controlled_access",
                                    "elementType": "geometry",
                                    "stylers": [{
                                        "color": "#4e4e4e"
                                    }]
                                },
                                {
                                    "featureType": "road.local",
                                    "elementType": "labels.text.fill",
                                    "stylers": [{
                                        "color": "#616161"
                                    }]
                                },
                                {
                                    "featureType": "transit",
                                    "stylers": [{
                                        "visibility": "off"
                                    }]
                                },
                                {
                                    "featureType": "transit",
                                    "elementType": "labels.text.fill",
                                    "stylers": [{
                                        "color": "#757575"
                                    }]
                                },
                                {
                                    "featureType": "water",
                                    "elementType": "geometry",
                                    "stylers": [{
                                        "color": "#000000"
                                    }]
                                },
                                {
                                    "featureType": "water",
                                    "elementType": "labels.text",
                                    "stylers": [{
                                        "visibility": "off"
                                    }]
                                },
                                {
                                    "featureType": "water",
                                    "elementType": "labels.text.fill",
                                    "stylers": [{
                                        "color": "#3d3d3d"
                                    }]
                                }
                            ]
                        });

                        var overlay = new google.maps.OverlayView();

                        overlay.onAdd = function() {
                            var layer = d3.select(this.getPanes().overlayLayer).append("div")
                                .attr("class", "stations");

                            overlay.draw = function() {

                                layer.select('svg').remove();

                                var projection = this.getProjection(),
                                    padding = 10;

                                var svg = layer.append("svg")
                                    .attr('width', 1200)
                                    .attr('height', 600);
                                console.log(data);

                                var node = svg.selectAll(".stations")
                                    .data(data.nodes)
                                    .enter().append("g")
                                    .each(transform)
                                    .attr("class", "node");

                                var link = svg.selectAll(".link")
                                    .data(data.links)
                                    .enter().append("path")
                                    .attr("class", "path")
                                    .each(drawlink);

                                node.append("circle")
                                    .attr("r", 4.5)
                                    .style("fill", "white");

                                node.append("text")
                                    .attr("x", 7)
                                    .attr("y", 0)
                                    .attr("dy", ".31em")
                                    .text(function(d) {
                                        return d.name;
                                    });

                                //Convert GPS coordinates to corresponding div pixels
                                function latLongToPos(d) {
                                    var p = new google.maps.LatLng(d.lat, d.long);
                                    p = projection.fromLatLngToDivPixel(p);
                                    p.x = p.x - padding;
                                    p.y = p.y - padding;
                                    return p;
                                }

                                //Comput GPS midpoint between source and destination airport
                                function latLongToMidpoint(source, dest) {
                                    //half_lat adjusted North by 3 degrees to adjust for curved paths
                                    half_lat = (dest.lat + source.lat) / 2 + 3;
                                    half_lon = (dest.long + source.long) / 2;
                                    var p = new google.maps.LatLng(half_lat, half_lon);
                                    p = projection.fromLatLngToDivPixel(p);
                                    p.x = p.x - padding;
                                    p.y = p.y - padding;
                                    return p;
                                }

                                function transform(d) {
                                    var p = latLongToPos(d);
                                    return d3.select(this)
                                        .attr("transform", "translate(" + p.x + "," + p.y + ")");
                                }

                                //Driver function to draw links between set of 3 points
                                function drawlink(d) {
                                    var p1 = latLongToPos(data.nodes[d.source]);
                                    var p2 = latLongToMidpoint(data.nodes[d.source], data.nodes[d.target]);
                                    var p3 = latLongToPos(data.nodes[d.target]);
                                    var lineData = [{
                                            "x": p1.x,
                                            "y": p1.y
                                        },
                                        {
                                            "x": p2.x,
                                            "y": p2.y
                                        },
                                        {
                                            "x": p3.x,
                                            "y": p3.y
                                        }
                                    ];
                                    var lineFunction = d3.svg.line()
                                        .x(function(d) {
                                            return d.x;
                                        })
                                        .y(function(d) {
                                            return d.y;
                                        })
                                        .interpolate("basis");

                                    d3.select(this)
                                        .attr("d", lineFunction(lineData))
                                        .style('fill', 'none')
                                        .style('stroke', 'yellow');
                                }
                            };

                        };
                        console.log('hello');
                        overlay.setMap(map);
                },
                error: function(error) {
                    console.log(error);
                }
            });
    });

$("#delete").on('click', function() {
    $.ajax({
        url: "/delete-route/" + $('#routes').val(),
        type: "GET",
        success: function(data) {
            console.log(data);
        },
        error: function(error) {
            console.log(error);
        }
    });
});

});
