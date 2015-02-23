import numpy as np
from scipy.optimize import broyden1

def cycloid(A, B, n = 100):
    """
    Generates n uniformly spaced sample points of an 
    inverted cycloid between points A and B.
    """

    x0, y0 = A 
    x1, y1 = B
    m = (y0 - y1) / (x1 - x0)

    def f(t):
        """
        Objective function for Broyden solver
        """
        return np.abs((1- np.cos(t)) / (t - np.sin(t)) - m)

    # find theta at B using a Broyden solver
    t = broyden1(f, [3.])[0]

    # now compute a
    a = (y1 - y0) / (1- np.cos(t))

    X,Y =[],[]
    # get sample points by varying theta
    for i in np.linspace(0, t, n):
        x = x0 - a*(i - np.sin(i))
        y = y0 + a*(1- np.cos(i))
        X.append(x)
        Y.append(y)
    x,y = np.array(X),np.array(Y)

    # now resample the points uniformly in x
    X = np.linspace(x.min(), x.max(), x.size)
    Y = np.interp(X, x, y)

    return X, Y

if __name__ == "__main__":
    from fit import fit_multiple
    import pylab

    # start and end points
    A = [0, 50.0]
    B = [150, 1.0]

    # fit a cycloid
    X, y0 = cycloid(A,B, n=B[0])

    # wavey curve
    y2 = 0.5*X + 3*np.sin(0.1*X + 4*np.pi/2) - 0.001*(X - 10.)**2

    # parabola
    y3 = (X - 95.)**2 - 3

    # fit them all to start at A and end at B
    y0, y1, y2, y3 = fit_multiple([y0, X, y2, y3], A, B)

    pylab.plot(X,y0)
    pylab.plot(X,y1)
    pylab.plot(X,y2)
    pylab.plot(X,y3)
    pylab.show()

