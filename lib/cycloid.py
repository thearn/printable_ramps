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


def total_time(x,y):
    """
    Estimated time of decent
    """
    g=9.8
    ya = y[0]
    dy = np.gradient(y, np.gradient(x, edge_order=2), edge_order=2)
    f = np.sqrt((dy[1:]**2 + 1)/np.abs(ya - y[1:]))
    return np.trapz(f)/np.sqrt(2*g)/10.


def get_times(x, y):
    T = []
    for i in xrange(2, len(x)+1):
        T.append(total_time(x[:i], y[:i]))
    return T

def objective(Y):
    global X
    y2 = np.array([50] + list(Y) + [8.0])
    return total_time(X,y2)

if __name__ == "__main__":
    from fit import fit_multiple
    from scipy.optimize import fmin
    import pylab

    # start and end points
    A = [0, 50.0]
    B = [110, 8.0]

    # fit a cycloid
    X, y0 = cycloid(A,B, n=B[0])
    y = fmin(objective, y0[1:-1])
    print objective(y)

    pylab.plot(X,y0)
    pylab.plot(X[1:-1],y)

    pylab.show()

