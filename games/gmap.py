
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
    def __init__(self, id='gmap', points=[]):
        """ points should be an array of tuples of the form
            (<id>, <lat>, <lon>, <html>)
        """
        self.id = id
        self.center = (0,0)
        self.zoom = 1
        self.points = points
    
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
                
                
                function Map(id,points,lat,long,zoom) {
                    this.id = id;
                    this.points = points;
                    this.gmap = new GMap2(document.getElementById(this.id));
                    this.gmap.setCenter(new GLatLng(lat, long), zoom);
                    this.markerlist = markerlist;
                    this.addmarker = addmarker;
                    this.array2points = array2points;
                    this.getPoints = getPoints;
                    
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
                    
                    function addmarker(point) {
                        if (point.html) {
                            GEvent.addListener(point.gpoint, "click", function() { // change click to mouseover or other mouse action
                                point.gpoint.openInfoWindowHtml(point.html);
                            });
                        }
                        GEvent.addListener(point.gpoint, "dragstart", function(){
                            // when event gets called, "this" will be the GMap2 object
                            this.closeInfoWindow();
                        });
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
                    
                    this.points = array2points(this.points);
                    this.markerlist(this.points);
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
        
        js = js.replace("(", "[")
        js = js.replace(")", "]")
        js = js.replace("u'", "'")
        js = js.replace("''","")    #python forces you to enter something in a list, so we remove it here
##        js = js.replace("'icon'", "icon")
        # for icon  in self.icons:
            # js = js.replace("'"+icon.id+"'",icon.id)
        js +=   """             %s = new Map('%s',%s_points,%s,%s,%s);
        """ % (self.id,self.id,self.id,self.center[0],self.center[1],self.zoom)
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
    

    
