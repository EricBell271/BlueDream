# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 19:59:31 2018

@author: Eric Bell
"""
import numpy as np
import pandas as pd
def gentrends(x, window=1/3.0, charts=True):
    """
    Returns a Pandas dataframe with support and resistance lines.

    :param x: One-dimensional data set
    :param window: How long the trendlines should be. If window < 1, then it
                   will be taken as a percentage of the size of the data
    :param charts: Boolean value saying whether to print chart to screen
    """

    import numpy as np
    import pandas as pd

#    x = np.array(x)

    if window < 1:
        window = int(window * len(x))

    max1 = np.where(x == max(x))[0][0]  # find the index of the abs max
    min1 = np.where(x == min(x))[0][0]  # find the index of the abs min

    # First the max
    if max1 + window > len(x):
        max2 = max(x[0:(max1 - window)])
    else:
        max2 = max(x[(max1 + window):])

    # Now the min
    if min1 - window < 0:
        min2 = min(x[(min1 + window):])
    else:
        min2 = min(x[0:(min1 - window)])

    # Now find the indices of the secondary extrema
    max2 = np.where(x == max2)[0][0]  # find the index of the 2nd max
    min2 = np.where(x == min2)[0][0]  # find the index of the 2nd min

    # Create & extend the lines
    maxslope = (x[max1] - x[max2]) / (max1 - max2)  # slope between max points
    minslope = (x[min1] - x[min2]) / (min1 - min2)  # slope between min points
    a_max = x[max1] - (maxslope * max1)  # y-intercept for max trendline
    a_min = x[min1] - (minslope * min1)  # y-intercept for min trendline
    b_max = x[max1] + (maxslope * (len(x) - max1))  # extend to last data pt
    b_min = x[min1] + (minslope * (len(x) - min1))  # extend to last data point
    maxline = np.linspace(a_max, b_max, len(x))  # Y values between max's
    minline = np.linspace(a_min, b_min, len(x))  # Y values between min's

    # OUTPUT
    trends = np.transpose(np.array((x, maxline, minline)))
    trends = pd.DataFrame(trends, index=np.arange(0, len(x)),
                          columns=['Data', 'Max Line', 'Min Line'])

    if charts is True:
        from matplotlib.pyplot import plot, grid, show
        plot(trends)
        grid()
        show()

    return trends, maxslope, minslope

def segtrends(x, segments=2, charts=True):
    """
    Turn minitrends to iterative process more easily adaptable to
    implementation in simple trading systems; allows backtesting functionality.

    :param x: One-dimensional data set
    :param window: How long the trendlines should be. If window < 1, then it
                   will be taken as a percentage of the size of the data
    :param charts: Boolean value saying whether to print chart to screen
    """

    import numpy as np
    y = np.array(x)

    # Implement trendlines
    segments = int(segments)
    maxima = np.ones(segments)
    minima = np.ones(segments)
    segsize = int(len(y)/segments)
    for i in range(1, segments+1):
        ind2 = i*segsize
        ind1 = ind2 - segsize
        maxima[i-1] = max(y[ind1:ind2])
        minima[i-1] = min(y[ind1:ind2])

    # Find the indexes of these maxima in the data
    x_maxima = np.ones(segments)
    x_minima = np.ones(segments)
    for i in range(0, segments):
        x_maxima[i] = np.where(y == maxima[i])[0][0]
        x_minima[i] = np.where(y == minima[i])[0][0]

    if charts:
        import matplotlib.pyplot as plt
        plt.plot(y)
        plt.grid(True)

    for i in range(0, segments-1):
        maxslope = (maxima[i+1] - maxima[i]) / (x_maxima[i+1] - x_maxima[i])
        a_max = maxima[i] - (maxslope * x_maxima[i])
        b_max = maxima[i] + (maxslope * (len(y) - x_maxima[i]))
        maxline = np.linspace(a_max, b_max, len(y))

        minslope = (minima[i+1] - minima[i]) / (x_minima[i+1] - x_minima[i])
        a_min = minima[i] - (minslope * x_minima[i])
        b_min = minima[i] + (minslope * (len(y) - x_minima[i]))
        minline = np.linspace(a_min, b_min, len(y))

        if charts:
            plt.plot(maxline, 'g')
            plt.plot(minline, 'r')

    if charts:
        plt.show()

    # OUTPUT
    return x_maxima, maxima, x_minima, minima

def minitrends(x, window=20, charts=True):
    """
    Turn minitrends to iterative process more easily adaptable to
    implementation in simple trading systems; allows backtesting functionality.

    :param x: One-dimensional data set
    :param window: How long the trendlines should be. If window < 1, then it
                   will be taken as a percentage of the size of the data
    :param charts: Boolean value saying whether to print chart to screen
    """

    import numpy as np

    y = np.array(x)
    if window < 1:  # if window is given as fraction of data length
        window = float(window)
        window = int(window * len(y))
    x = np.arange(0, len(y))
    dy = y[window:] - y[:-window]
    crit = dy[:-1] * dy[1:] < 0

    # Find whether max's or min's
    maxi = (y[x[crit]] - y[x[crit] + window] > 0) & \
           (y[x[crit]] - y[x[crit] - window] > 0) * 1
    mini = (y[x[crit]] - y[x[crit] + window] < 0) & \
           (y[x[crit]] - y[x[crit] - window] < 0) * 1
    maxi = maxi.astype(float)
    mini = mini.astype(float)
    maxi[maxi == 0] = np.nan
    mini[mini == 0] = np.nan
    xmax = x[crit] * maxi
    xmax = xmax[~np.isnan(xmax)]
    xmax = xmax.astype(int)
    xmin = x[crit] * mini
    xmin = xmin[~np.isnan(xmin)]
    xmin = xmin.astype(int)

    # See if better max or min in region
    yMax = np.array([])
    xMax = np.array([])
    for i in xmax:
        indx = np.where(xmax == i)[0][0] + 1
        try:
            Y = y[i:xmax[indx]]
            yMax = np.append(yMax, Y.max())
            xMax = np.append(xMax, np.where(y == yMax[-1])[0][0])
        except:
            pass
    yMin = np.array([])
    xMin = np.array([])
    for i in xmin:
        indx = np.where(xmin == i)[0][0] + 1
        try:
            Y = y[i:xmin[indx]]
            yMin = np.append(yMin, Y.min())
            xMin = np.append(xMin, np.where(y == yMin[-1])[0][0])
        except:
            pass
    if y[-1] > yMax[-1]:
        yMax = np.append(yMax, y[-1])
        xMax = np.append(xMax, x[-1])
    if y[0] not in yMax:
        yMax = np.insert(yMax, 0, y[0])
        xMax = np.insert(xMax, 0, x[0])
    if y[-1] < yMin[-1]:
        yMin = np.append(yMin, y[-1])
        xMin = np.append(xMin, x[-1])
    if y[0] not in yMin:
        yMin = np.insert(yMin, 0, y[0])
        xMin = np.insert(xMin, 0, x[0])

    # Plot results if desired
    if charts is True:
        from matplotlib.pyplot import plot, show, grid
        plot(x, y)
        plot(xMax, yMax, '-o')
        plot(xMin, yMin, '-o')
        grid(True)
        show()
    # Return arrays of critical points
    return xMax, yMax, xMin, yMin

def iterlines(x, window=30, charts=True):
    """
    Turn minitrends to iterative process more easily adaptable to
    implementation in simple trading systems; allows backtesting functionality.

    :param x: One-dimensional data set
    :param window: How long the trendlines should be. If window < 1, then it
                   will be taken as a percentage of the size of the data
    :param charts: Boolean value saying whether to print chart to screen
    """

    

    x = np.array(x)
    n = len(x)
    if window < 1:
        window = int(window * n)
    sigs = np.zeros(n, dtype=float)

    i = window
    while i != n:
        if x[i] > max(x[i-window:i]): sigs[i] = 1
        elif x[i] < min(x[i-window:i]): sigs[i] = -1
        i += 1

    xmin = np.where(sigs == -1.0)[0]
    xmax = np.where(sigs == 1.0)[0]
    ymin = x[xmin]
    ymax = x[xmax]
    if charts is True:
        from matplotlib.pyplot import plot, grid, show
        plot(x)
        plot(xmin, ymin, 'ro')
        plot(xmax, ymax, 'go')
        grid(True)
        show()

    return sigs


def supres(ltp, n):
    """
    This function takes a numpy array of last traded price
    and returns a list of support and resistance levels 
    respectively. n is the number of entries to be scanned.
    """
    from scipy.signal import savgol_filter as smooth

    # converting n to a nearest even number
    if n % 2 != 0:
        n += 1
    
    n_ltp = ltp.shape[0]

    # smoothening the curve
    ltp_s = smooth(ltp, (n + 1), 3)

    # taking a simple derivative
    ltp_d = np.zeros(n_ltp)
    ltp_d[1:] = np.subtract(ltp_s[1:], ltp_s[:-1])

    resistance = []
    support = []


    for i in range(n_ltp - n):
        arr_sl = ltp_d[i:(i + n)]
        divided = int(n/2)
        first = arr_sl[:(divided)]  # first half
        last = arr_sl[(divided):]  # second half

        r_1 = np.sum(first > 0)
        r_2 = np.sum(last < 0)

        s_1 = np.sum(first < 0)
        s_2 = np.sum(last > 0)

        # local maxima detection
        if (r_1 == (divided)) and (r_2 == (divided)):
            resistance.append(ltp[i + ((divided) - 1)])

        # local minima detection
        if (s_1 == (divided)) and (s_2 == (divided)):
            support.append(ltp[i + ((divided) - 1)])
    return support, resistance