from rpy2 import robjects
import numpy as np
import shapely.geometry as sg

def rStrauss(beta, gamma, R, area):
    """
    Generate a random pattern of points, a simulated realisation of the Strauss process, using a perfect simulation algorithm.

    :param beta: intensity
    :param gamma: contorls the 'strength' of interaction between points, if gamma = 1 the model reduces to a Poisson process. If gamma = 0, the model is a hard core process. For values 0<gamma<1, the process exhibits inhibition between points
    :param R: pairwise distance
    :param area: sampling region
    :return: a two dimensional array, each element is a (x,y) coordinate
    """

    minx, miny, maxx, maxy = area.bounds
    # call R
    r = robjects.r
    r.library("spatstat")
    a = r.owin(r.c(minx,maxx),r.c(miny,maxy))
    b = r.rStrauss(beta,gamma,R,W = a)
    #b = r.rStrauss(2,0.2,0.7,W = a)
    #print(b.rx2('x'))
    x = b.rx2('x')
    y = b.rx2('y')

    return np.array([[x[i],y[i]] for i in range(len(x))])


if __name__ == "__main__":
    area = sg.Polygon([(0, 0), (0, 2), (2, 2), (2, 0)])
    print(rStrauss(2,0.2,0.7,area))