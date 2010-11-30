"""
    Some utility functions for the Games app.
"""

def csv_to_list(csv):
    """ Return a list of integer values from a CSV string """
    return map(int, filter(lambda x: len(x) > 0, csv.split(',')))

def locations_to_points(locations):
    """ Convert a list of Locations into a list of 'points',
        where each point is a tuple containing (id, lat, lon).
    """
    
    points = []
    for loc in locations:
        # temp: fill in the text for the location.
        # this is technically a View thing, but the google maps
        # infowindow binding isnt working properly yet,
        # so I have this here for the demo
        text = 'ID: %d<br />Clue: %s' % (loc.id, loc.clue)
        points.append((str(loc.id),
                       str(loc.latitude),
                       str(loc.longitude), text))
    return points
