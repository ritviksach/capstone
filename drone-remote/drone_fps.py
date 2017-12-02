import datetime

class FPS():
    def __init__(self, logQ = None):
        self.prev = datetime.datetime.now()
        self.FPS = 10.0
        self.q = None
        if logQ:
            self.q = logQ
            
    def update(self):
        now = datetime.datetime.now()
        newFPS = 1.0 / (now - self.prev).total_seconds()
        self.prev = now
        self.FPS = self.FPS * 0.9 + newFPS * 0.1
        if self.q:
            try:
                self.q.put((self,prev, self.FPS), False)
            except Queue.Full:
                pass
            
    def reset(self):
        self.prev = datetime.datetime.now()
        
        if self.q:
            try:
                tstamp.y = self.q.get(False)
            except Queue.Empty:
                pass
            
            time.sleep(0.001)
            
    def log(self, label=""):
        print "%s %6.3f FPS" % (label, self.FPS)
        sys.stdout.flush()

    def get(self):
        return self.FPS