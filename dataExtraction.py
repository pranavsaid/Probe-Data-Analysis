from math import sin, cos, atan2, sqrt, degrees, radians, pi, asin
from geopy.distance import great_circle as distance
from geopy.point import Point


import csv


class ProbePoint(object):
  def __init__(self, sampleID, dateTime, sourceCode, latitude, longitude, elevation, speed, heading):
    self.sampleID = sampleID
    self.dateTime = dateTime
    self.sourceCode = sourceCode
    self.latitude = latitude
    self.longitude = longitude
    self.elevation = elevation
    self.speed = speed
    self.heading = heading

  def __str__(self):
    return str(self.sampleID) + ',' + str(self.dateTime) + ',' + str(self.sourceCode) + ',' \
           + str(self.latitude) + ',' + str(self.longitude) + ',' + str(self.elevation) + ',' \
           + str(self.speed) + ',' + str(self.heading)


class LinkData(object):
  def __init__(self, file_name):
    self.file = file_name
    self.links = {}

  def extractLinks(self):
    with open(self.file, 'r') as lk:
      datareader = csv.reader(lk)
      for row in datareader:
        linkPVID = int(row[0])
        refNodeID = int(row[1])
        nrefNodeID = int(row[2])
        length = float(row[3])
        directionOfTravel = row[5]
        shapeInfo = row[14]
        slopeInfo = row[16]
        self.links[linkPVID] = Link(linkPVID, refNodeID, nrefNodeID, length, directionOfTravel, shapeInfo, slopeInfo)
        # print str(self.links[linkPVID])
    return self.links


class Link(object):
  def __init__(self, linkPVID, refNodeID, nrefNodeID, length, directionOfTravel, shapeInfo, slopeInfo):
    self.linkPVID = linkPVID
    self.refNodeID = refNodeID
    self.nrefNodeID = nrefNodeID
    self.length = length
    self.directionOfTravel = directionOfTravel
    self.shapeInfo = shapeInfo
    self.slopeInfo = slopeInfo
    self.geo = []
    self.slope = []
    self._extract_shape_info()
    self._extract_slope_info()
    self.link = ''

  def get_nrefNodeID(self):
  	return self.nrefNodeID

  def get_refNodeID(self):
  	return self.refNodeID

  def _extract_shape_info(self):
    for dat in self.shapeInfo.split('|'):
      info = [0,0]
      info[0], info[1], elevation = dat.split('/')
      self.geo.append(info)
    self.reflat = float(self.geo[0][0])
    self.reflong = float(self.geo[0][1])
    l = len(self.geo)
    self.nreflat = float(self.geo[l-1][0])
    self.nreflong = float(self.geo[l-1][1])

  def _extract_slope_info(self):
    if not self.slopeInfo :
      self.slopeInfo = None
      return
    for dat in self.slopeInfo.split('|') :
      info = [0,0]
      info[0], info[1] = dat.split('/')
      self.slope.append(info)

  def __str__(self) :
    return 'PVID ' + str(self.linkPVID) + ' Ref ID :'+ str(self.refNodeID) + ' lat :' + str(self.reflat) + ' long :' + str(self.reflong) \
         + ' NRef ID :'+ str(self.nrefNodeID) + ' lat :' + str(self.nreflat) + ' long :' + str(self.nreflong)

  def distFromMidPoint(self, probepoint,lattitude1,longitude1,lattitude2,longitude2):
    p = Point(probepoint.latitude,probepoint.longitude)
    a_lat, a_lon = radians(lattitude1), radians(longitude1)
    b_lat, b_lon = radians(lattitude2), radians(longitude2)
    delta_lon = b_lon - a_lon
    B_x = cos(b_lat) * cos(delta_lon)
    B_y = cos(b_lat) * sin(delta_lon)
    mid_lat = atan2( sin(a_lat) + sin(b_lat),sqrt(((cos(a_lat) + B_x)**2 + B_y**2)) )
    mid_lon = a_lon + atan2(B_y, cos(a_lat) + B_x)
    mid_lon = (mid_lon + 3*pi) % (2*pi) - pi
    midpoint = Point(latitude=degrees(mid_lat), longitude=degrees(mid_lon))
    return distance(midpoint, p).km * 1000


