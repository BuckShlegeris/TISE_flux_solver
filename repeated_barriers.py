from fluxSolver import transmissionAmount, graph



def makeBarriers(width,height,spacing,number):
    outlist = []
    x = 0

    for a in range(number):
        outlist.append((x,height))
        x += width
        outlist.append((x,0))
        x += spacing

    return outlist

graph(makeBarriers(1,1,0.03,40))

