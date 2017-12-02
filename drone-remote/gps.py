from geopy.distance import great_circle

class GPS():
    
    def __init__(self, lat, lng, distance):
        self.lat = lat
        self.lng = lng
        self.cautionDistance = distance
    
    def setCautionDistance(self, distance):
        self.cautionDistance = distance
    
    def updateLocation(self, lat, lng):
        this.lat = lat
        this.lng = lng
    
    def myLocation(self):
        return this.lat, this.lng
    
    def distance(self, lat, lng):
        return great_circle(this.myLocation, (lat, lng)).metres
    
    def alert(self, lat, lng):
        distance = self.distance(lat, lng)
        
        if distance <= self.cautionDistance:
            return True
        
        return False
        
    