# Written by Logan Amos\
import math

class ProjectileMotion():
    def __init__(self):
        self.theta = 0 # in degrees, will convert to radians
        self.vi    = 0 # initial velocity
        self.vix   = self.vi * math.cos(self.theta) # initial x velocity
        self.viy   = self.vi * math.sin(self.theta) # initial y velocity
        self.dx    = 0 # x distance travelled
        self.dy    = 0 # y distance travelled
        self.ay    = 0 # acceleration in the y direction
        self.t     = 0 # duration of flight

    def rangeCalc(self, vi, theta, initial_height=None):
        if initial_height == None and theta <= 90:
            try:
                #       (vi)^2(sin2theta)
                # dx =  -------------------
                #               ay

                a = math.pow(vi, 2)
                b = math.sin(2*theta)
                c = self.ay
                self.dx = (a*b)/c
                return self.dx
            except ZeroDivisionError:
                print("Did you define y-acceleration?")
        
    def parabolicPositionCalc(self, vi, ay, height=None,time=None):
        if height == None:
            # Use 4th kinematic equation
            dx = (vi*time + 0.5*ay(*math.pow(time,2)))
            return dx
        if time == None:
            # Use quadratic equation
            a = -4.6 # acceleration due to gravity * 0.5
            b = self.vi
            b = self.viy
            c = height
            time = (-b+math.sqrt(math.pow(b,2)-(4*a*c)))/2*a
            return time
            
def deaccelerate(velocity, rate):
    if velocity != 0:
        velocity -= rate
    return velocity

def accelerate(velocity, rate, ceiling=None):
    if ceiling == None:
        velocity += rate
        return velocity
    if ceiling != 0:
        velocity += rate
        return velocity
            

if __name__ == "__main__":
    p = ProjectileMotion()
    p.theta = 50
    p.vi = 0
    p.ay = -9.8
    dx = p.rangeCalc(p.vi,p.theta)
    #print(dx)
    t = p.parabolicPositionCalc(p.vi,p.ay, height=12)
    print(-t)

