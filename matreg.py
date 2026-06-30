import numpy as np

def matreg(Tj,Yj,epoch=0,periods=None):
    #   Regression function using variable matrix methods. 
    #   [YF,YR,Xb,HTH,HTHinv] = MATREG(T,Y,epoch,periods) takes the 
    #   regression of a dataset Y that is tested for dependence on variable T.
    #
    #   epoch is the amount of time by which the time series is to be shifted.
    #   Epoch must be included even if it is zero.
    #
    #   Use an array for periods [m1,...mn] when nper > 1
    #   Periods aren't required and defaults are zero.
    #   If m1 = 1, then a period of one year will be assumed.
    #
    #   Terms are, in order linear slope and y-intercept followed by 
    #   alternating cosine and sine terms to create the matrix H.
    #
    #   Calculations are done using matrix methods as follows:    
    #        HTH = H'*H;
    #        HTy = H'*Y;
    #        HTHinv = inv(HTH);
    #        X = HTHinv*HTy;
    #
    #   The fit is calculated as follows: 
    #        fit = X(1) + X(2)*(T-epoch) + X(3)*cos(2*pi*(T-epoch)) + 
    #        X(4)*sin(2*pi*(T-epoch)) + ... alternating cosines and sines
    #
    #   YF,YR,X,YF,& HTHinv are returned so that other quantities may be found.
    
    if periods is None:
        periods = []

    # make vertical arrays
    Tj = np.asarray(Tj).reshape(-1)
    Yj = np.asarray(Yj).reshape(-1)
    
    # number of periods
    nper = len(periods)
    if nper > 0:
        freqp = 2 * np.pi / np.array(periods)
    else:
        freqp = np.array([])
    # number of parameters to use for sinusoids
    nparam = 2 + 2 * nper

    # if the data is bad
    bad = np.isnan(Yj) | np.isnan(Tj)
    Tj = Tj[~bad]
    Yj = Yj[~bad]

    # the H matrix for the computations
    H = np.ones((len(Yj), nparam))

    H[:,1] = Tj

    # populate the sinusoidal terms
    if nper > 0:
        H[:,2:nparam:2] = np.cos(freqp*Tj[:,None])
        H[:,3:nparam:2] = np.sin(freqp*Tj[:,None])

    # perform the computations to find X
    HTH = H.T @ H
    HTy = H.T @ Yj
    HTHinv = np.linalg.inv(HTH)
    Xb = HTHinv @ HTy
    Xb = Xb.T

    # find the best fit equation
    # include sinusoidal terms if necessary
    if nper > 0:
        Xcos = Xb[2:nparam:2] * np.cos(freqp * Tj[:, None])
        Xsin = Xb[3:nparam:2] * np.sin(freqp * Tj[:, None])
        YF = Xb[0] + Xb[1] * Tj + np.sum(Xcos, axis=1) + np.sum(Xsin, axis=1)
    else:
        YF = Xb[0] + Xb[1] * Tj

    # transpose the array to horizontal again (just my preference)
    Xb = Xb.T

    # compute the residual
    YR = Yj - YF

    return YF, YR, Xb, HTH, HTHinv
