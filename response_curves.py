import matplotlib.pyplot as pyplot
import pylab
from fluxsolver import transmissionAmount, graph

def graphResponse(devices, e1, e2, eStep, title=""):
    
    for (device,label) in devices:
        x = []
        y = []

        energy = e1


        while energy < e2:
            x.append(energy)
            y.append(transmissionAmount(device,energy))
            
            energy += eStep

        if not label:
            label = str(device)
        pyplot.plot(x,y,label=label)
    pylab.xlabel('Energy of wave')
    pylab.ylabel('Transmssion probability')
    pylab.legend()
    pylab.title(title)
    pylab.grid(True)
    pyplot.show()

def makeBarriers(width,height,spacing,number):
    outlist = []
    x = 0

    for a in range(number):
        outlist.append((x,height))
        x += width
        outlist.append((x,0))
        x += spacing



    return (outlist,str((width,height,spacing,number)))

if False:
    barrierlist = []
    x = 0

    for a in range(number):
        outlist.append((x,1))
        x += 1
        outlist.append((x,0))
        x += 1

    for a in range(number):
        outlist.append((x,1))
        x += 1
        outlist.append((x,0))
        x += 1

barriers = [makeBarriers(1,1,1,10),
            makeBarriers(1.2,1.2,1.2,10)]

#graph(makeBarriers(0.2,1,1,10),1.2)
graphResponse(barriers,0,4,0.01,'Transmission probabilities from consecutive square wells')
