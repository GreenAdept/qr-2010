
"""
    Google Maps API interface.

    Generates necessary Javascript code
    for showing the google map &
    interacting with it.

    Based on Pymaps 0.9
    Copyright (C) 2007  Ashley Camba <stuff4ash@gmail.com> http://xthought.org
"""

# Google API key
_api_key = "ABQIAAAAQQRAsOk3uqvy3Hwwo4CclBTrVPfEE8Ms0qPwyRfPn-DOTlpaLBTvTHRCdf2V6KbzW7PZFYLT8wFD0A"

class Map:
    def __init__(self, id='gmap', points=[], point_order=[]):
        """ points should be an array of tuples of the form
            (<id>, <lat>, <lon>, <html>). If <html> is blank/not given,
            then the DOM node with id="<map_id>_point_<point_id>" is bound
            to the point's infowindow (and if there is no DOM node with
            this id, then the infowindow is just not shown).
            
            point_order is a list of point ID's, whose order determines
            the order that the points are connected to one another.
            If point_order is empty, then the points are not connected to
            one another.
        """
        self.id = id
        self.center = (0,0)
        self.zoom = 1
        self.points = points
        self.point_order = point_order
    
    def to_js(self):
        
        js = """
        \n<script src=\"http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s\" type="text/javascript"></script>
        <script type="text/javascript">
        //<![CDATA[
        function load_gmap() {
            if (GBrowserIsCompatible()) {
                
                function Point(id, lat, long, html, icon) {
                    this.gpoint = new GMarker(new GLatLng(lat, long),
                                              { "icon" : icon,
                                                "draggable" : true }
                                             );
                    this.html = html;
                    this.id = id;
                }
                
                
                function Map(id,points,lat,long,zoom,point_order) {
                    this.id = id;
                    this.points = points;
                    this.point_order = point_order;
                    this.gmap = new GMap2(document.getElementById(this.id));
                    this.gmap.setCenter(new GLatLng(lat, long), zoom);
                    this.markerlist = markerlist;
                    this.addmarker = addmarker;
                    this.array2points = array2points;
                    this.getPoints = getPoints;
                    this.updateLines = updateLines;
                    
                    if (this.point_order.length > 0) {
                        this.gpolyline = new GPolyline();
                        this.gmap.addOverlay(this.gpolyline);
                    }
                    
                    function markerlist(array) {
                        for (var i in array) {
                            this.addmarker(array[i]);
                        }
                    }
                    
                    function array2points(map_points) {
                        for (var i in map_points) {
                            points[i] = new Point(map_points[i][0],
                                                  map_points[i][1],
                                                  map_points[i][2],
                                                  map_points[i][3],
                                                  map_points[i][4]
                                                  );
                        }
                        return points;
                    }
                    
                    function points_dict(points) {
                        var dict = {};
                        for (var i in points) {
                            var id = points[i].id;
                            dict[id] = points[i];
                        }
                        return dict;
                    }
                    
                    function addmarker(point) {
                        if (point.html) {
                            GEvent.addListener(point.gpoint, "click", function() {
                                // 'this' is the GMarker object
                                this.openInfoWindowHtml(point.html);
                            });
                        } else {
                            point.gpoint.bindInfoWindow(
                                document.getElementById(
                                    "gmap_point_" + point.id));
                        }
                        GEvent.addListener(point.gpoint, "dragstart", function(){
                            // 'this' is the GMarker object
                            this.closeInfoWindow();
                        });
                        if (this.point_order.length > 0) {
                            GEvent.bind(point.gpoint, "dragend", this, this.updateLines);
                        }
                        this.gmap.addOverlay(point.gpoint);
                    }
                    
                    function getPoints() {
                        var point_data = [];
                        for (var i in this.points) {
                            var point = this.points[i];
                            point_data.push({ "id": point.id,
                                              "lat": point.gpoint.getLatLng().lat(),
                                              "lon": point.gpoint.getLatLng().lng() });
                        }
                        
                        return point_data;
                    }
                    
                    function updateLines() {
                        if (this.point_order.length > 0) {
                            for (var i in this.point_order) {
                                var point_id = this.point_order[i];
                                var point = this.points_by_id[point_id];
                                
                                this.gpolyline.deleteVertex(i);
                                this.gpolyline.insertVertex(i, point.gpoint.getLatLng());
                            }
                        }
                    }
                    
                    this.points = array2points(this.points);
                    this.points_by_id = points_dict(this.points);
                    this.markerlist(this.points);
                    this.updateLines();
                }
                
                %s
            }
        }
        
        //]]>
        </script>
        """ % (_api_key, self._mapjs())
        return js
    
    def _mapjs(self):
        js = "%s_points = %s;\n" % (self.id, self.points)
        js += "%s_order = %s;\n" % (self.id, self.point_order)
        
        js = js.replace("(", "[")
        js = js.replace(")", "]")
        js = js.replace("u'", "'")
        js = js.replace("''","")    #python forces you to enter something in a list, so we remove it here
##        js = js.replace("'icon'", "icon")
        # for icon  in self.icons:
            # js = js.replace("'"+icon.id+"'",icon.id)
        js +=   """             %s = new Map('%s',%s_points,%s,%s,%s,%s_order);
        """ % (self.id,self.id,self.id,self.center[0],self.center[1],self.zoom,self.id)
        js += """ %s.gmap.addControl(new GSmallMapControl());\n""" % self.id
        return js
    
    # def _iconjs(self,icon):
    #     js = """ 
    #             var %s = new GIcon(); 
    #             %s.image = "%s";
    #             %s.shadow = "%s";
    #             %s.iconSize = new GSize(%s, %s);
    #             %s.shadowSize = new GSize(%s, %s);
    #             %s.iconAnchor = new GPoint(%s, %s);
    #             %s.infoWindowAnchor = new GPoint(%s, %s);
    #     """ % (icon.id, icon.id, icon.image, icon.id, icon.shadow, icon.id, icon.iconSize[0],icon.iconSize[1],icon.id, icon.shadowSize[0], icon.shadowSize[1], icon.id, icon.iconAnchor[0],icon.iconAnchor[1], icon.id, icon.infoWindowAnchor[0], icon.infoWindowAnchor[1])
    #     return js
     
    # def _buildicons(self):
    #     js = ""
    #     if (len(self.icons) > 0):
    #         for i in self.icons:
    #            js = js + self._iconjs(i)    
    #     return js
    

    
