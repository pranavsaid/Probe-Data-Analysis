from math import sin, cos, atan2, sqrt, degrees, radians, pi, atan, asin
from dataExtraction import ProbePoint
from dataExtraction import LinkData
import csv

class MapMatch(object):

  def main(self):
    mapstruct = LinkData('Partition6467LinkData.csv')
    self.links = mapstruct.extractLinks()
    self.probefile = 'Partition6467ProbePoints.csv'
    self.csvop = ''
    self.prpoints = []
    self.mainMAtchingCode()

  def mainMAtchingCode(self):
    f = open('output.csv', 'w')
    with open(self.probefile, 'r') as probe:
      datareader = csv.reader(probe)
      i = 0
      for row in datareader:
        ppoint = ProbePoint(int(row[0]),str(row[1]),int(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]))
        if i == 0 :
          self.prpoints.append(ppoint)
          i = i + 1
        elif self.prpoints[i-1].sampleID == ppoint.sampleID :
          self.prpoints.append(ppoint)
          i = i + 1
        else :
          self.prpoints = []
          self.prpoints.append(ppoint)
          i = 1
        link = self.getNearestLink(ppoint)
        linkPVID = link.linkPVID
        distFromLink = link.distFromMidPoint(ppoint,link.reflat,link.reflong,link.nreflat,link.nreflong)
        distFromRef = self.haversine(ppoint,link.reflat,link.reflong)
        slope = self.slope(link,ppoint)
        direction = link.directionOfTravel
        stri = ',' + str(linkPVID) + ','+ str(direction) + ','+str(distFromRef) + ','+str(distFromLink)
        print str(ppoint) + stri + '\n'
        f.write(str(ppoint) + stri + '\n')
    f.close()


  def getNearestLink(self,ppoint):
    nearestlink = self.links.keys()[0]
    minimun_distance = self.links[nearestlink].distFromMidPoint(ppoint,self.links[nearestlink].reflat,self.links[nearestlink].reflong,self.links[nearestlink].nreflat,self.links[nearestlink].nreflong)
    for link in self.links :
      distFromMidPoint = self.links[link].distFromMidPoint(ppoint,self.links[link].reflat,self.links[link].reflong,self.links[link].nreflat,self.links[link].nreflong)
      if distFromMidPoint < minimun_distance :
        nearestlink = link
        minimun_distance = distFromMidPoint
    return self.links[nearestlink]

  def slope(self,link,ppoint) :
    if len(self.prpoints) == 1 :
      return 'Not enough point available to print slope'
    i = len(self.prpoints) - 2
    elevation = ppoint.elevation - self.prpoints[i].elevation
    distance = self.haversine(ppoint,self.prpoints[i].latitude,self.prpoints[i].longitude)
    sl = elevation/distance
    if sl > 1 or sl < -1 :
      return 'distance bet probe points too small : ' + str(distance) + 'm'
    prslope = degrees(asin(elevation/distance))
    if link.slopeInfo is None :
      return ' Proble slope : '+str(prslope)+' Link slope : Not available '
    mmlink = 0
    mindist = link.distFromMidPoint(ppoint,link.geo[0][0],link.geo[0][1],link.geo[1][0],link.geo[1][1])
    for i in range(1,len(link.slope)):
      sldistance = link.distFromMidPoint(ppoint,link.geo[i-1][0],link.geo[i-1][1],link.geo[i][0],link.geo[i][1])
      if sldistance < mindist :
        mmlink = i
        mindist = sldistance
    error = float(link.slope[mmlink][1]) - prslope
    return ' Probe slope : '+str(prslope)+' Link slope : '+str(link.slope[mmlink][1])+\
    ' error : '+ str(abs(error))


  def haversine(self,probepoint1,probepoint2_latitude,probepoint2_longitude):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lat1 = probepoint1.latitude
    lon1 = probepoint1.longitude
    lat2 = probepoint2_latitude
    lon2 = probepoint2_longitude
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371*1000 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

if __name__ == '__main__':
  MapMatch().main()