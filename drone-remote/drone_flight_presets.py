
class FlightModePresets():
    def __init__(self):
        self.cycleTime = 0
        self.cycleType = "odd"
        self.evadingObject = False
        
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
        self.evadingObject = False
        
    def getEvasiveValues(self, state, cb):
        throttle, rotation, elev, aile = state["r_thumb_y"], state["r_thumb_x"], state["l_thumb_y"], state["l_thumb_x"]
        '''
            Implementation is to go left for a while and
            come back onto the original path once collision 
            is not detected anymore
            
            One possible solution is to get a start/stop state
            
            Start, if cb is None:
                keep giving values that make drone go left (aile +)
                count the number of cycles that this value has been sent
                
            Stop, if a callback function is given:
                Get the number of cycles drone got GO-LEFT command
                send GO-RIGHT command that many times
        '''
        if cb is None:
            self.cycleTime += 1
            aile = 1150
        else:
            print "*** Went left for %d cycles ***" % self.cycleTime
            self.cycleTime -= 1
            if self.cycleTime == 0:
                cb()
            aile = 1100
                
        return throttle, rotation, elev, aile
        
    
    def getHoverModeValues(self):
        self.cycleTime += 1
        if self.cycleTime < 100:
            return self.liftOffValues()
        
        if self.cycleTime == 100:
            print "Lift off done, stablising now!"
        
        return self.getStableModeValues()
    
    def getStableModeValues(self):
        throttle, rotation, elev, aile = self.liftOffValues()
        
        self.cycleTime += 1
        if self.cycleType == "even":
            elev = 1100 + (self.cycleTime * 2)
            
            # Switch cycles after sending 5 values of same type
            if self.cycleTime % 5 == 0:
                self.cycleType = "odd"
                self.cycleTime = 0
        else:
            elev = 1100 - (self.cycleTime * 2)
            if self.cycleTime % 5 == 0:
                self.cycleTime = 0
                self.cycleType = "even"
        
        return throttle, rotation, elev, aile
    
    
    def liftOffValues(self):
        throttle = 1100
        rotation = None
        elev = 1050
        aile = 1100
        
        return throttle, rotation, elev, aile
        