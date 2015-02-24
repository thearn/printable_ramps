import numpy as np

def fit_multiple(Ys, A, B, offset=True):
    """
    Scale multiple curves together to fit between points A and B.
    
    All fitted functions are then shifted, if necessary, so all points are 
    positive. This ensures that a printable set of ramps will always be returned,
    while still representing the A --> B problem accurately. 
    """
    Y, dips = [], []
    for y in Ys:
        y_new, dip = rescale(y, A, B)
        Y.append(y_new)
        dips.append(dip)

    if offset:
        for y in Y:
            y += -min(dips) + 0.01
    return Y


def rescale(y, A, B):
    """
    Scale a single function to fit between points A and B
    """

    dy = B[1] - A[1]
    dx = B[0] - A[0]

    y = (y - y[-1])# / (y[0] - y[1])
    y = y / (y[0] - y[-1]) * -dy + min([B[1], A[1]])

    dip = min(y)
    if dip >= 0:
        dip = 0.0

    return y, dip

if __name__ == "__main__":
    import pylab
    A = [0, 50.0]
    B = [150., 1.0]

    x = np.linspace(0,150,150)
    y1 = (x - 95.)**2 - 3


    y2 = 0.5*x + 3*np.sin(0.1*x + 4*np.pi/2)


    ys = fit_multiple([y1, y2], A, B)

    for y in ys:
        print y
        pylab.plot(y)
    pylab.show()