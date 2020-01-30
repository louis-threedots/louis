class Cell:
    


    def __init__(self):
        self.state = [0,0,0,0,0,0]
    

    def set_state(self, state):
        self.state = state
        #TODO: Physically set pin state passed as binary array to the function.

    
    def clear(self):
        self.state = [0,0,0,0,0,0]
