## differentEnergyFlux.py

# Buck Shlegeris, May 2013
# Thanks to Stephen Watson, Daniel Filan, and Prithvi Reddy for their assistance
# with the theoretical underpinnings of this module.

from cmath import sqrt, exp
from numpy import mat
from numpy.linalg import lstsq
import numpy as np
import pylab

###################
#  The API is as follows.

#  It is assumed that the mass of the particle and hbar are 1.

#  Potential functions are written as a list of (x,y) pairs, specifying where
#  the potential should change, and what it should change to. For example, a
#  rectangular potential barrier which starts at x=0, has potential of 1, and a
#  width of 1 would be written as [(0,1),(1,0)].

#####
# solve(potential_function,energy)
# This takes a potential function and solves for a particle flux of 1 coming in
# from the right.

# The solution is written as a list of complex values representing the coefficient
# of every part of the wavefuntion, with the part of the wave going left and the
# part of the wave going right written seperately in that order.


#####
# graph(potential_function, energy, name=None)
# This solves the potential function and then graphs it. If you specify name,
# it then saves the graph to an accordingly named file.

# The red line is potential, the dark blue and green lines are the real and 
# imaginary sections of the wavefunction respectively, and the teal line is the
# probability density.

#####
# transmissionAmount(potential_function, energy)
# This solves the potential function, then tells you what proportion of the wave
# propogates through to the other side. (It's just returning the second last 
# number in the solution list.)

def exampleRun():
    potentialBarrier = [(0,2),(1,0)]
    
    print transmissionAmount(potentialBarrier,1)
    
    print solve(potentialBarrier,1)
    
    graph(potentialBarrier,1)


##################################################################
## Beware, extremely ugly implementation below!

def momentum(pot,energy):
    return 1j*sqrt(2*(pot-energy))

def valOfWave(p, x, k1, k2): # p stands for momentum
    return k1*exp(1j*p*x) + k2*exp(-1j*p*x)

def makeEquations(pot,energy):

    numVars = len(pot)*2+2
  
    outmatrix = []
    outvals = []
  
    outmatrix.append([1.]+[0.]*(numVars-1))
    outvals.append([1.])
  
    outmatrix.append([0.]*(numVars-1)+[1])   
    outvals.append([0.])
  
    prevPot = 0
  
    listPosition = 0
  
    for (pos,thisPot) in pot:
        prevMomentum = momentum(prevPot,energy)
        thisMomentum = momentum(thisPot,energy)
           
        # Psi(x) = k1 exp(ipx) + k2 exp(-ipx)
        a = exp(1j*pos*prevMomentum)
        b = exp(1j*-pos*prevMomentum)
        c = exp(1j*pos*thisMomentum)
        d = exp(1j*-pos*thisMomentum)
      
        newrow = [0.]*listPosition*2 + [a,b,-c,-d] + [0.]*(numVars - listPosition*2 - 4)
       
        outmatrix.append(newrow)
        outvals.append([0])

        # Same thing, but with spatial derivatives
 
        a = prevMomentum*exp(1j*pos*prevMomentum)
        b = -prevMomentum*exp(1j*-pos*prevMomentum)
        c = thisMomentum*exp(1j*pos*thisMomentum)
        d = -thisMomentum*exp(1j*-pos*thisMomentum)
      
        newrow = [0.]*listPosition*2 + [a,b,-c,-d] + [0.]*(numVars - listPosition*2 - 4)
 
        outmatrix.append(newrow)      
        outvals.append([0.])
      
        listPosition += 1
        prevPot = thisPot
      
    return mat(outmatrix), mat(outvals)
 
def solve(pot,energy):
    a,b = makeEquations(pot,energy)
    return lstsq(a,b)[0]
    
def graph(potential,energy,name=None):
    graphSolution(potential,energy,solve(potential,energy),name)

def graphSolution(pot,energy,solution,name):
    pot = map(lambda (x,y): (float(x),float(y)), pot)

    def findValue(x):
        n, m = findPosAndVal(x,pot)
        return valOfWave(momentum(m,energy),x,solution[n*2],solution[n*2+1])

    def findPosAndVal(x,inlist):
        if x < inlist[0][0]:
            return (0,0.0)
        
        else:
            a = 0
            try:
                while inlist[a][0] < x:
                    a+=1
                return (a, float(inlist[a-1][1]))
            except Exception:
                return (a, float(inlist[a-1][1]))

    real = np.vectorize(lambda y: findValue(y).real)
    imag = np.vectorize(lambda y: findValue(y).imag)
    mag = np.vectorize(lambda y: abs(findValue(y)))
    potFunc = np.vectorize(lambda y: findPosAndVal(y,pot)[1])
        
    t = np.arange(-6.0, 10.0+0.01, 0.01)

    s = real(t)
    s2 = imag(t)
    s3 = potFunc(t)
    s4 = mag(t)
    
    pylab.plot(t, s,label="Real value")
    pylab.plot(t, s2, label = "Imaginary value")
    pylab.plot(t, s3, label = "Potential")
    pylab.plot(t, s4, label="Magnitude")

    pylab.xlabel('Position')
    
    pylab.legend()
    
    pylab.title('Quantum flux solver. T=%f'%abs(solution.item(len(pot)*2)))
    pylab.grid(True)
    if name:
        pylab.savefig(name)

    pylab.show()


def transmissionAmount(potential,energy):
    a = solve(potential,energy)
    return abs(a.item(len(potential)*2))**2


if __name__ == "__main__":
    exampleRun()
