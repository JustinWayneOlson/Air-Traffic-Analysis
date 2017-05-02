$(document).ready(function() {
    $('#legend').hide();
    $('#tabs').tabs();
    $('#Origin').prop("disabled", true);
    $('#Dest').prop("disabled", true);
    $('#Carrier').prop("disabled", true);


    //Time picker for start date formatted m/d/y
    $('#date_start').datetimepicker({
        timepicker: false,
        format: 'm/d/Y'
    });

    //Time picker for end date formatted m/d/y
    $('#date_end').datetimepicker({
        timepicker: false,
        format: 'm/d/Y'
    });
    $('#info-table').DataTable();

    //Ajax call to populate dropdown menu for Source airports(s)
    $.ajax({
        type: "GET",
        url: "/dropdown-fill/Origin",
        success: function(data) {
            console.log('done');
            $('#Origin').prop('disabled', false);
            $('#Origin').select2({
                data: data['response'],
                placeholder: "Select an option"
            });
        },
        error: function(error) {
            console.log(error);
        }
    });

    //Ajax call to populate dropdown menu for Destination airport(s)
    $.ajax({
        type: "GET",
        url: "/dropdown-fill/Dest",
        success: function(data) {
            $('#Dest').prop('disabled', false);
            $('#Dest').select2({
                data: data['response'],
                placeholder: "Select an option"
            });
        },
        error: function(error) {
            console.log(error);
        }
    });

    //Ajax call to populate dropdown menu for different Carriers
    $.ajax({
        type: "GET",
        url: "/dropdown-fill/Carrier",
        success: function(data) {
            $('#Carrier').prop('disabled', false);
            $('#Carrier').select2({
                data: data['response'],
                placeholder: "Select an option"
            });
        },
        error: function(error) {
            console.log(error);
        }
    });
});

//Ran if the "Plot Airports" button is pushed
$("#plot-airports").click(function(event) {
    var tab_num = $('#tab-tabs').children().length;
    var tab_id = "tab-" + parseInt(tab_num + 1);
    $('#tab-tabs').append('<li><a href="#' + tab_id + '">Query #' + tab_num + '</a></li>');
    $('#tabs').append('<div id="' + tab_id + '"></div>');
    $('#' + tab_id).append('<div class="row"><div class="col-xs-6 map-container"><div class="map" id="map-' + tab_num + '"></div></div><div class="col-xs-6 table-container"><table id="table-' + tab_num + '" class="display"></table></div></div>');
    $('#' + tab_id).append('<div class="row"><div class="col-xs-4 line-plot-container"><div id="ct-chart-line-' + tab_num + '" class="ct-chart"></div></div><div class="col-xs-4 pie-plot-container"><div id="ct-chart-pie-' + tab_num + '" class="ct-chart"></div></div><div class="col-xs-4 bar-plot-container"><div id="ct-chart-bar-' + tab_num + '" class="ct-chart"></div></div></div>');
    $('#tabs').tabs("refresh");

      var observe_element = document.getElementById(tab_id);
      var observer = new MutationObserver(function(mutations){
           mutations.forEach(function(mutation){
           $('.ct-chart').each(function(i, e) {
               e.__chartist__.update();
           });
           $('.map').each(function(i, e) {
               google.maps.event.trigger(map, 'resize');
           });
         });
      });
      console.log(observer);

         observer.observe(observe_element, {
            attributes: true
         });


    //Instantiating map visualization (night mode)
    var map = new google.maps.Map(d3.select("#map-" + tab_num).node(), {
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

    //Loading icon while Google map is loading
    $('#map- ' + tab_num).append('<img id="loading" src="/img/loading.gif"></img>');

    //Instantiate 'data' dictionary to store user input
    var data = {}
    $('#selections-container').find('input').each(function(index, value) {
        //For the non-checkbox options...
        if ($(value).val() && $(value).attr('type') != 'checkbox') {
            //Add multiple values for a single input into the dictionary
            if ($(value).attr('multiple') == 'multiple') {
                data[$(value).attr('id')] = $(value).val().split(',');
            }

            //Otherwise, add the single value into the dictionary
            else {
                data[$(value).attr('id')] = $(value).val();
            }
        }

        //For the checkbox options...
        else if ($(value).attr('type') == 'checkbox') {
            //Add whether or not the 'Verbose Output' or 'Toggle Plaths' options are checked
            //True if checked, False if unchecked
            data['verbose_toggle'] = $('#verbose-toggle').prop('checked');
            data['path_toggle'] = $('#path-toggle').prop('checked');
        }
    });

    //Stringify the data dictionary
    var form_query = JSON.stringify(data);

    //Ajax call to run once the 'Display Airports' button is pushed
    $.ajax({
        url: "/display-airports",
        type: "POST",
        data: form_query,

        success: function(data) {
            console.log(data);
            var line_chart_data = {
                labels: data['plot_data']['line']['labels'],
                series: [
                  data['plot_data']['line']['series']
                ]
            };

            var bar_chart_data = {
                labels: data['plot_data']['bar']['labels'],
                series: [
                  data['plot_data']['bar']['series']
                ]
            };

            new Chartist.Line('#ct-chart-line-' + tab_num, chart_data);
            new Chartist.Bar('#ct-chart-bar-' + tab_num, chart_data);
            var chart_data = {
                series: [20, 15, 40]
            };

            var options = {
                labelInterpolationFnc: function(value) {
                    return value[0]
                }
            };

            new Chartist.Pie('#ct-chart-pie-' + tab_num, chart_data, options);

            $('#table-' + tab_num).DataTable({
                data: data['table_data']['table_data'],
                columns: data['table_data']['headers']
            });

            //If the user requests verbose output, append output to verbose-contained in html
            if (data['verbose']) {
                $('#verbose-container').append('<p>' + data['verbose'] + '</p>')
            }

            if (!(data['links'])) {
                $('#loading').remove();
                var geoJSON;
                var request;
                var gettingData = false;
                var openWeatherMapKey = "b6c5711b8dcd855fced4510aa21dbecc";

                function initialize(map) {
                    google.maps.event.addListener(map, 'idle', checkIfDataRequested);

                    map.data.addListener('click', function(event) {
                        infowindow.setContent(
                            "<img src=" + event.feature.getProperty("icon") + ">" +
                            "<br /><strong>" + event.feature.getProperty("city") + "</strong>" +
                            "<br />" + event.feature.getProperty("temperature") + "&deg;C" +
                            "<br />" + event.feature.getProperty("weather"));

                        infowindow.setOptions({
                            position: {
                                lat: event.latLng.lat(),
                                lng: event.latLng.lng()
                            },
                            pixelOffset: {
                                width: 0,
                                height: -15
                            }
                        });
                        infowindow.open(map);
                    });
                }

                var checkIfDataRequested = function() {
                    while (gettingData === true) {
                        request.abort();
                        gettingData = false;
                    }
                    getCoords();
                };

                var getCoords = function() {
                    var bounds = map.getBounds();
                    var NE = bounds.getNorthEast();
                    var SW = bounds.getSouthWest();
                    getWeather(NE.lat(), NE.lng(), SW.lat(), SW.lng());
                };

                var getWeather = function(northLat, eastLng, southLat, westLng) {
                    gettingData = true;
                    console.log("Getting weather...");
                    var requestString = "http://api.openweathermap.org/data/2.5/box/city?bbox=" +
                        westLng + "," + northLat + "," +
                        eastLng + "," + southLat + "," +
                        map.getZoom() +
                        "&cluster=yes&format=json" +
                        "&APPID=" + openWeatherMapKey;
                    request = new XMLHttpRequest();
                    request.onload = processResults;
                    request.open("get", requestString, true);
                    request.send();
                };

                var processResults = function() {
                    var results = JSON.parse(this.responseText);
                    if (results.list.length > 0) {
                        resetData();
                        for (var i = 0; i < results.list.length; i++) {
                            geoJSON.features.push(jsonToGeoJson(results.list[i]));
                        }
                        drawIcons(geoJSON);
                    }
                };

                var infowindow = new google.maps.InfoWindow();

                var jsonToGeoJson = function(weatherItem) {
                    var feature = {
                        type: "Feature",
                        properties: {
                            city: weatherItem.name,
                            weather: weatherItem.weather[0].main,
                            temperature: weatherItem.main.temp,
                            icon: "http://openweathermap.org/img/w/" +
                                weatherItem.weather[0].icon + ".png",
                            coordinates: [weatherItem.coord.Lon, weatherItem.coord.Lat]
                        },

                        geometry: {
                            type: "Point",
                            coordinates: [weatherItem.coord.Lon, weatherItem.coord.Lat]
                        }
                    };

                    map.data.setStyle(function(feature) {
                        return {
                            icon: {
                                url: feature.getProperty('icon'),
                                anchor: new google.maps.Point(25, 25)
                            }
                        };
                    });
                    return feature;

                    function latLongToPos(d) {
                        var p = new google.maps.LatLng(d.lat, d.long);
                        p = projection.fromLatLngToDivPixel(p);
                        p.x = p.x - padding;
                        p.y = p.y - padding;
                        return p;
                    }

                    function mouseoutofinfo() {
                        d3.select(this).transition()
                            .duration(100)
                            .attr("r", 4.5);
                    }

                    function someinfo() {
                        d3.select(this).transition()
                            .duration(1000)
                            .attr("r", 75);
                    }
                    var table_data = []

                    function moreinfo() {
                        $('.odd').remove();
                        var delay_data = $(this)[0].__data__;
                    }

                    function transform(d) {
                        var p = latLongToPos(d);
                        return d3.select(this)
                            .attr("transform", "translate(" + p.x + "," + p.y + ")");
                    }

                    function setColor(d) {
                        return d3.select(this)
                            .style('fill', d.Color)
                    }
                };

                var resetData = function() {
                    geoJSON = {
                        type: "FeatureCollection",
                        features: []
                    };
                    map.data.forEach(function(feature) {
                        map.data.remove(feature);
                    });
                };

                var drawIcons = function(weather) {
                    map.data.addGeoJson(geoJSON);
                    gettingData = false;
                };

                google.maps.event.addDomListener(window, 'load', initialize(map));

                var overlay = new google.maps.OverlayView();
                overlay.onAdd = function() {
                    var layer = d3.select(this.getPanes().overlayMouseTarget).append("div")
                        .attr("class", "stations");
                    overlay.draw = function() {
                        layer.select('svg').remove();
                        var projection = this.getProjection(),
                            padding = 10;

                        var svg = layer.append("svg")
                            .attr('width', 1200)
                            .attr('height', 600);

                        var node = svg.selectAll(".stations")
                            .data(data.nodes)
                            .enter().append("g")
                            .each(transform)
                            .attr("class", "node")
                            .on('click', moreinfo);

                        node.append("circle")
                            .attr("r", 4.5)
                            .each(setColor)
                            .on('mouseover', someinfo)
                            .on('mouseout', mouseoutofinfo);

                        function latLongToPos(d) {
                            var p = new google.maps.LatLng(d.lat, d.long);
                            p = projection.fromLatLngToDivPixel(p);
                            p.x = p.x - padding;
                            p.y = p.y - padding;
                            return p;
                        }

                        function mouseoutofinfo() {
                            d3.select(this).transition()
                                .duration(100)
                                .attr("r", 4.5);
                        }

                        function someinfo() {
                            d3.select(this).transition()
                                .duration(1000)
                                .attr("r", 10);
                        }


                        function moreinfo() {
                            $('.odd').remove();
                            var delay_data = $(this)[0].__data__;
                            console.log(tab_id);
                            if($('#' + tab_id).find($('#my-modal')))
                            {
                              $('#' + tab_id).find($('#my-modal')).remove();
                            }
                            $('#' +tab_id).append('<div id="my-modal" class="bs-example-modal-sm fade modal"role=dialog aria-labelledby=mySmallModalLabel tabindex=-1><div class="modal-dialog modal-sm"role=document><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Close">&times;</span></button><h4 class="modal-tittle">Additional Data</h4><span aria-hidden="true"></div><div class="modal-body"> <pre>' +  JSON.stringify($(this)[0].__data__, undefined, 2) + '</pre></div></div></div></div>');
                            $('#my-modal').modal();
                        }

                        function transform(d) {
                            var p = latLongToPos(d);
                            return d3.select(this)
                                .attr("transform", "translate(" + p.x + "," + p.y + ")");
                        }

                        function setColor(d) {
                            return d3.select(this)
                                .style('fill', d.Color)
                        }
                    };
                };
                overlay.setMap(map);

            } else {
                $('#loading').remove();
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

                        var node = svg.selectAll(".stations")
                            .data(data.nodes)
                            .enter().append("g")
                            .each(transform)
                            .attr("class", "node")
                            .on('click', moreinfo);

                        var link = svg.selectAll(".link")
                            .data(data.links)
                            .enter().append("path")
                            .attr("class", "path")
                            .each(drawlink);

                        node.append("circle")
                            .attr("r", 4.5)
                            .style("fill", "white")
                            .on('mouseover', someinfo)
                            .on('mouseout', mouseoutofinfo);

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

                        function mouseoutofinfo() {
                            d3.select(this).transition()
                                .duration(100)
                                .attr("r", 4.5);
                        }

                        function someinfo() {
                            d3.select(this).transition()
                                .duration(1000)
                                .attr("r", 10);
                        }


                        function moreinfo() {
                            $('.odd').remove();
                            var delay_data = $(this)[0].__data__;
                            console.log(tab_id);
                            if($('#' + tab_id).find($('#my-modal')))
                            {
                              $('#' + tab_id).find($('#my-modal')).remove();
                            }
                            $('#' +tab_id).append('<div id="my-modal" class="bs-example-modal-sm fade modal"role=dialog aria-labelledby=mySmallModalLabel tabindex=-1><div class="modal-dialog modal-sm"role=document><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Close">&times;</span></button><h4 class="modal-tittle">Additional Data</h4><span aria-hidden="true"></div><div class="modal-body"> <pre>' +  JSON.stringify($(this)[0].__data__, undefined, 2) + '</pre></div></div></div></div>');
                            $('#my-modal').modal();
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

                overlay.setMap(map);
            }
        },
        error: function(error) {
            $('#loading').remove()
            console.log(error);
        }
    });
})
