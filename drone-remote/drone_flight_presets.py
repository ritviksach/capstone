
class FlightModePresets():
    def __init__(self):
        self.cycleTime = 0
        self.cycleType = "odd"
        
    def getValues(self, flightMode):
        if flightMode == "evasiveManeuver":
            return self.getEvasiveValues()
            
        elif flightMode == "hover":
            return self.getHoverModeValues()
        
        elif flightMode == "stable":
            return self.getStableModeValues()
        
    def reset(self):
        self.cycleTime   = 0
        self.cycleType   = "odd"
        
    def getEvasiveValues(self, state):
        '''
            Implementation is to go left for a while and
            come back onto the original path once collision 
            is not detected anymore
            
            One possible solution is to get a start/stop state
            
            Start:
                keep giving values that make drone go left (aile +)
                count the number of cycles that this value has been sent
                
            Stop:
                Get the number of cycles drone got GO-LEFT command
                send GO-RIGHT command that many times
        '''
        
        return self.StableModeValues()
    
    def getHoverModeValues(self):
        #self.cycleNumber += 1
        #if self.cycleNumber < 100:
        return self.liftOffValues()
        
        #print "Lift off done, stablising now!"
        
        #return self.getStableModeValues()
    
    def getStableModeValues(self):
        throttle, rotation, elev, aile = self.liftOffValues()
        
        self.cycleTime += 1
        if self.cycleType == "even":
            throttle = 1060
            aile = 1025
            # Switch cycles after sending 5 values of same type
            if self.cycleTime % 5 == 0:
                self.cycleType = "odd"
                self.cycleTime = 0
        else:
            throttle = 1070
            aile = 1100
            if self.cycleTime % 5 == 0:
                self.cycleTime = 0
                self.cycleType = "even"
        
        return throttle, rotation, elev, aile
    
    
    def liftOffValues(self):
        throttle = 1100
        rotation = None
        elev = 1050
        aile = 1175
        
        return throttle, rotation, elev, aile
        