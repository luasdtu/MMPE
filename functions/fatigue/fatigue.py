'''
Created on 04/03/2013

@author: mmpe
'''



from cython_compile.cython_compile import cython_import
import numpy as np


def rfc_hist(sig_rf, nrbins=46):
    """
    Histogram of rainflow counted cycles
    ====================================

    hist, bin_edges, bin_avg = rfc_hist(sig, nrbins=46)

    Divide the rainflow counted cycles of a signal into equally spaced bins.

    Created on Wed Feb 16 16:53:18 2011
    @author: David Verelst
    Modified 10.10.2011 by Mads M Pedersen to elimintate __copy__ and __eq__

    Parameters
    ----------
    sig_rf : array-like
        As outputted by rfc_astm or rainflow

    nrbins : int, optional
        Divide the rainflow counted amplitudes in a number of equally spaced
        bins.

    Output
    ------
    hist : array-like
        Counted rainflow cycles per bin, has nrbins elements

    bin_edges : array-like
        Edges of the bins, has nrbins+1 elements.

    bin_avg : array-like
        Average rainflow cycle amplitude per bin, has nrbins elements.
    """

    rf_half = sig_rf

    # the Matlab approach is to divide into 46 bins
    bin_edges = np.linspace(0, 1, num=nrbins + 1) * rf_half.max()
    hist = np.histogram(rf_half, bins=bin_edges)[0]
    # calculate the average per bin
    hist_sum = np.histogram(rf_half, weights=rf_half, bins=bin_edges)[0]
    # replace zeros with one, to avoid 0/0
    hist_ = hist.copy()
    hist_[(hist == 0).nonzero()] = 1.0
    # since the sum is also 0, the avg remains zero for those whos hist is zero
    bin_avg = hist_sum / hist_

    return hist, bin_edges, bin_avg


def check_signal(signal):
    # check input data validity
    if not type(signal).__name__ == 'ndarray':
        raise TypeError('signal must be ndarray, not: ' + type(signal).__name__)

    elif len(signal.shape) not in (1, 2):
        raise TypeError('signal must be 1D or 2D, not: ' + str(len(signal.shape)))

    if len(signal.shape) == 2:
        if signal.shape[1] > 1:
            raise TypeError('signal must have one column only, not: ' + str(signal.shape[1]))


def rainflow_windap(signal, levels=255., thresshold=(255. / 50)):
    """
    Windap equivalent rainflow counting
    ===================================

    Calculate the amplitude and mean values of cycles in signal

    This algorithms used by this routine is implemented directly as described in
    "Recommended Practices for Wind Turbine Testing - 3. Fatigue Loads", 2. edition 1990, Appendix A

    Parameters
    ----------
    Signal : array-like
        The raw signal

    levels : int, optional
        The signal is discretize into this number of levels.
        255 is equivalent to the implementation in Windap

    thresshold : int, optional
        Cycles smaller than this thresshold are ignored
        255/50 is equivalent to the implementation in Windap

    Output
    ------
    ampl : array-like
        amplitudes of the cycles

    mean : array-like
        Mean values of the cycles


    Example
    -------
    signal = np.array([-2.0, 0.0, 1.0, 0.0, -3.0, 0.0, 5.0, 0.0, -1.0, 0.0, 3.0, 0.0, -4.0, 0.0, 4.0, 0.0, -2.0])
    ampl, mean = rainflow_windap(signal)
    """
    check_signal(signal)
    #type <double> is required by <find_extreme> and <rainflow>
    signal = signal.astype(np.double)

    offset = np.min(signal)
    signal -= offset
    if np.max(signal) > 0:
        gain = float(np.max(signal)) / levels
        signal = signal / gain
        signal = np.round(signal).astype(np.int)

        #Import peak_throug(find extremes) and pair_range(rainflowcount).
        #If possible the module is compiled using cython otherwise the python implementation is used

        cython_import('functions.fatigue.peak_trough')
        from functions.fatigue.peak_trough import peak_trough


        #Convert to list of local minima/maxima where difference > thresshold
        sig_ext = peak_trough(signal, thresshold)

        cython_import("functions.fatigue.pair_range")
        from functions.fatigue.pair_range import pair_range_amplitude_mean
        #rainflow count
        ampl_mean = pair_range_amplitude_mean(sig_ext)

        #This is not smart but corresponds to the implementation in Windap
        ampl_mean = np.array(ampl_mean)

        #sig_rfc = sig_rfc[np.where(sig_rfc>=thresshold)[0]]
        ampl_mean = np.round(ampl_mean / thresshold) * gain * thresshold
        ampl_mean[:, 1] += offset
        return ampl_mean.T



def rainflow_astm(signal):
    """
    Matlab equivalent rainflow counting
    ===================================

    Calculate the amplitude and mean values of cycles in signal

    This implemementation is based on the c-implementation by Adam Nieslony found at
    the MATLAB Central File Exchange http://www.mathworks.com/matlabcentral/fileexchange/3026

    Parameters
    ----------
    Signal : array-like
        The raw signal

    Output
    ------
    ampl : array-like
        amplitudes of the cycles

    mean : array-like
        Mean values of the cycles


    Example
    -------
    signal = np.array([-2.0, 0.0, 1.0, 0.0, -3.0, 0.0, 5.0, 0.0, -1.0, 0.0, 3.0, 0.0, -4.0, 0.0, 4.0, 0.0, -2.0])
    ampl, mean = rainflow_windap(signal)
    """
    check_signal(signal)

    # type <double> is reuqired by <find_extreme> and <rainflow>
    signal = signal.astype(np.double)

    # Import find extremes and rainflow.
    # If possible the module is compiled using cython otherwise the python implementation is used
    cython_import('functions.fatigue.rainflowcount_astm')
    from rainflowcount_astm import find_extremes, rainflow_astm

    # Remove points which is not local minimum/maximum
    sig_ext = find_extremes(signal)

    # rainflow count
    ampl_mean = np.array(rainflow_astm(sig_ext))

    return np.array(ampl_mean).T


def eq_load(signal, no_bins=46, m=[3, 4, 6, 8, 10, 12], neq=1, rainflow_func=rainflow_windap):
    """
    Equivalent load calculation
    ===========================

    Calculate the equivalent loads for a list of Wohler exponent

    Parameters
    ----------
    Signal : array-like
        The raw signal

    no_bins : int, optional
        Number of bins in rainflow count histogram

    m : array-like, optional
        Wohler exponent (default is [3, 4, 6, 8, 10, 12])

    neq : int, optional
        The equivalent number of load cycles (default is 1, but normally the time duration in seconds is used)

    rainflow_func : {rainflow_windap, rainflow_astm}, optional
        The rainflow counting function to use (default is rainflow_windap)

    Output
    ------
    eq_loads : array-like
        list of equivalent loads for the corresponding Wohler exponents


    Example
    -------
    signal = np.array([-2.0, 0.0, 1.0, 0.0, -3.0, 0.0, 5.0, 0.0, -1.0, 0.0, 3.0, 0.0, -4.0, 0.0, 4.0, 0.0, -2.0])
    eq_loads = eq_load(signal, no_bins=50, neq=17, rainflow_func=rainflow_windap)
    """
    ampl, _ = rainflow_func(signal)
    if ampl is None:
        return []
    hist_data, x, bin_avg = rfc_hist(ampl, no_bins)

    m = np.atleast_1d(m)

    eq = []
    for i in range(len(m)):
        eq.append(np.power(np.sum(0.5 * hist_data * np.power(bin_avg, m[i])) / neq, 1. / m[i]))
    return eq

def cycle_matrix(signal, ampl_bins=10, mean_bins=10, rainflow_func=rainflow_windap):
    """
    Markow load cycle matrix
    =============================

    Calculate the Markow load cycle matrix

    Parameters
    ----------
    Signal : array-like
        The raw signal

    ampl_bins : int, optional
        Number of amplitude value bins (default is 10)

    mean_bins : int, optional
        Number of mean value bins (default is 10)

    rainflow_func : {rainflow_windap, rainflow_astm}, optional
        The rainflow counting function to use (default is rainflow_windap)

    Output
    ------
    H : ndarray, shape(ampl_bins, mean_bins)
        A bi-dimensional histogram of load cycles. Amplitudes are histogrammed along the first dimension and mean values are histogrammed along the second dimension.

    ampl_edges : ndarray, shape(ampl_bins,)
        The amplitude bin edges

    mean_edges : ndarray, shape(mean_bins,)
        The mean bin edges

    Example
    -------
    signal = np.array([-2.0, 0.0, 1.0, 0.0, -3.0, 0.0, 5.0, 0.0, -1.0, 0.0, 3.0, 0.0, -4.0, 0.0, 4.0, 0.0, -2.0])
    H, ampl_edges, mean_edges= cycle_matrix(signal)
    """
    ampl, mean = np.array(rainflow_func(signal))
    return np.histogram2d(ampl, mean, [ampl_bins, mean_bins])



if __name__ == "__main__":
    import os
    os.chdir("../../")  # When compile is needed current working directory must be parent of functions.fatigue
    signal = np.array([-2.0, 0.0, 1.0, 0.0, -3.0, 0.0, 5.0, 0.0, -1.0, 0.0, 3.0, 0.0, -4.0, 0.0, 4.0, 0.0, -2.0])
    print eq_load(signal, no_bins=50, neq=17, rainflow_func=rainflow_windap)
    print eq_load(signal, no_bins=50, neq=17, rainflow_func=rainflow_astm)
    print cycle_matrix(signal, 4, 4, rainflow_func=rainflow_windap)
    print cycle_matrix(signal, 4, 4, rainflow_func=rainflow_astm)
