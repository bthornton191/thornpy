"""Signal processing module
"""
from scipy.signal import butter, filtfilt, find_peaks
from scipy.signal.windows import hann, hamming, blackman, boxcar
import matplotlib.pyplot as plt
from matplotlib import cm  
import numpy as np

def low_pass(sig, time, freq_cutoff, N=5):
    """Applies a Nth order butterworth lowpass filter.
    
    Parameters
    ----------
    sig : list
        Signal to be filtered
    time : list
        Time signal in seconds associated with `sig`
    freq_cutoff : int
        Cutoff frequency in Hz to use when filtering
    N : int
        Order of butterworth filter (default is 5)
    
    Returns
    -------
    list
        Filtered signal
    list
        Time signal associated with filtered signal

    """
    freq_samp = 1/(time[1]-time[0])
    omega = freq_cutoff/freq_samp*2
    b_coef, a_coef = butter(N, omega)
    return list(filtfilt(b_coef, a_coef, sig)), time
        
def step_function(index, start, init_val, end, final_val):
    """Approximates the Heaviside step function with a cubic polynomial.
    
    Example
    -------
    >>> x = [2, 3, 3.5, 4, 5]
    >>> start = 3
    >>> init_val = 0
    >>> end = 3
    >>> final_val = 1
    >>> step_function(x, start, init_val, end, final_val)
    [0.0, 0.0, 0.5, 1.0, 1.0]
    
    Parameters
    ----------
    index : list
        Independent variable
    start : float
        Value of independent variable at which the STEP function begins
    init_val : float
        Initial value of the step
    end : float
        Value of independent variable at which the STEP function ends
    final_val : float
        Final value of the step
    
    Returns
    -------
    list
        Resulting step function

    """
    height = final_val - init_val
    step =  [init_val for ind in index if ind <= start]    
    step += [init_val + height*((ind-start)/(end-start))**2 * (3-2*((ind-start)/(end-start))) for ind in index if start < ind < end]
    step += [final_val for ind in index if ind >= end]
    return step

def fft_watefall(time, sig, percent_overlap=50, n_fft=1024, title=None, t_min=None, t_max=None, input_sig=None, input_conversion_factor=60/360, input_unit='RPM', response_unit=None, response_conversion_factor=1, psd=False, z_scale='linear', order_lines=None, f_range=None, clean_sig=None, return_order_cuts=None):
    """Genenerates a waterfall plot from data in an Adams result or request file.
    
    Parameters
    ----------
    time : list
        Time signal in seconds
    sig : list
        Signal
    comp : str
        Name of the result component in the Adams dataset
    percent_overlap : int, optional
        Percent overlap for the FFT waterfall, by default 50
    n_fft : int, optional
        Number of points used in each FFT, by default 1024
    window : str, optional
        Type of window used for each FFT, by default 'hanning'
    t_min : float, optional
        Start time if cropping data, by default None
    t_max : float, optional
        End time if cropping data, by default None
    input_sig : list, optional
        Time signal of input shaft speed, by default None
    input_time : list, optional
        Input shaft speed, by default None
    input_conversion_factor : float, optional
        Conversion factor applied to input signal, by default 60/360 (deg/s to RPM)
    response_unit : str, optional
        Text to display on the response signal y axis, by default None
    input_unit : str, optional
        Text to display on the input signal y axis, by default None
    conversion_factor : float, optional
        Conversion factor applied to response signal, by default 1
    psd : bool, optional
        If True FFT will output in PSD. If False FFT will output Magnitude , by default False
    z_scale : str, optional
        The scaling of the values in the spec. 'linear' is no scaling. 'dB' returns the values in dB scale. `psd` is True, this is dB power (10 * log10). Otherwise this is dB amplitude (20 * log10). by default 'linear'
    orders : list, optional
        Adds order fans to the waterfall plots at each order in the list.  Only used if `input_comp` is given.
    f_range : list, optional
        [mininum frequency, maximum frequency].  Only affects plot limits
    clean_sig : float, optional
        If given, removes data points that exceed `clean_sig` multiplied by the standard deviation of the signal.
    title : str, optional
        Plot title, by default None.
    
    Returns
    -------
    Figure
        Waterfall plot

    """    
    if clean_sig is not None:
        sig, i_removed = _clean_sig(sig, clean_sig)

    # Convert to other unis (for converting to Gs)
    if response_conversion_factor is not None:
        sig = [v*response_conversion_factor for v in sig]
    
    check_num_points(len(time), n_fft)

    t_s = (time[-1] - time[0])/(len(time) - 1)
    f_s = 1/t_s
    
    _fig, (ax1, ax2) = plt.subplots(nrows=2)
    ax1.plot(time, sig)
    # plt.grid()

    # Pxx, freqs, bins, im = ax2.specgram(sig, NFFT=n_fft, Fs=f_s, noverlap=percent_overlap/100*n_fft, window=get_window(window))
    Pxx, freqs, bins, im = ax2.specgram(sig, NFFT=n_fft, Fs=f_s, noverlap=percent_overlap/100*n_fft, detrend='mean', mode='magnitude' if psd is False else 'psd', scale=z_scale, cmap='nipy_spectral')
    # The `specgram` method returns 4 objects. They are:
    # - Pxx: the periodogram
    # - freqs: the frequency vector
    # - bins: the centers of the time bins
    # - im: the matplotlib.image.AxesImage instance representing the data in the plot
    _fig.clear()
    plt.close()    
    del _fig

    # Convert to dB
    if z_scale.lower() == 'db':
        Pxx = np.log10(Pxx) * (20 if psd is False else 10)

    # ----------------
    # Signal
    # ----------------
    x_wtrfl, y_wtrfl = np.meshgrid(bins+time[0], freqs)
    fig, axes = plt.subplots(nrows=2 if input_sig is None else 3)
    axes[0].plot(time, sig)
    
    if clean_sig is not None:
        axes[0].plot([time[i] for i in i_removed], [sig[i] for i in i_removed], '.', markersize=3)

    axes[0].set_xlim(time[0], time[-1])
    if response_unit is None:
        axes[0].set_ylabel(response_unit)
    else:
        axes[0].set_ylabel(response_unit)
    axes[0].grid()        

    if title is not None:
        axes[0].set_title(title)    

    if input_sig is None:
        # ----------------
        # 3D FFT
        # ----------------        
        wtrfl_surf = axes[1].contourf(x_wtrfl, y_wtrfl, Pxx, 250, cmap=cm.get_cmap('nipy_spectral'), extend='min')
        axes[1].set_xlim(time[0], time[-1])
        axes[1].set_xlabel('Time (s)')
        axes[1].set_ylabel('Frequency (Hz)')
        axes[1].set_grid(True)
        # wtrfl_fig.colorbar(wtrfl_surf)

    else:        
        # ----------------
        # Order Chart
        # ----------------
        if len(input_sig) != len(time):
            raise ValueError('Input signal must be the same lenght as the response signel.')

        input_sig_rpm = [abs(v*input_conversion_factor) for v in input_sig]
        input_bins = [abs(input_sig_rpm[np.argmax(time>=t_bn+time[0])]) for t_bn in bins]
        x_order, y_order = np.meshgrid(input_bins, freqs)
        
        # Plot Input Signal
        axes[1].plot(time, input_sig_rpm)
        axes[1].set_xlim(time[0], time[-1])
        axes[1].set_xlabel('Time (s)')
        axes[1].set_ylabel(input_unit)
        axes[1].set_title('Input Speed')
        axes[1].grid(True)

        # Plot Order Waterfall
        if f_range is not None:
            i_min = np.argmax(freqs>=f_range[0])
            i_max = np.argmax(freqs>=f_range[1])
        else:
            i_min = len(freqs)
            i_max = len(freqs)

        wtrfl_surf = axes[2].contourf(x_order[i_min:i_max], y_order[i_min:i_max], Pxx[i_min:i_max], 250, cmap=cm.get_cmap('nipy_spectral', 100), extend='min')
        axes[2].set_xlabel(input_unit)
        axes[2].set_ylabel('Frequency (Hz)')

        # Add order lines
        if order_lines is not None:
            _add_order_lines(axes[2], order_lines, input_unit)
    
        if psd is True:
            y_label = f'{response_unit}^2/Hz' if z_scale.lower()!='db' else 'dB'            
        elif response_unit is not None:
            y_label = response_unit if z_scale.lower()!='db' else 'dB'

        # Add colorbar
        cbar = fig.colorbar(wtrfl_surf)
        cbar.set_label(y_label)

        # Generate Order Cut Plots
        if return_order_cuts is not None:
            order_cuts = _order_cut_plot(input_bins, freqs, Pxx, return_order_cuts, y_label=y_label)
        
    fig.set_size_inches(10,10)
    fig.tight_layout()

    print(f'dt: {n_fft*t_s}')

    if input_sig is None:
        return (fig, time, sig)
    elif return_order_cuts is None:
        return (fig, time, sig, input_sig_rpm)
    else:
        return (fig, time, sig, input_sig_rpm, order_cuts)

def check_num_points(num, n_fft):    
    if num < n_fft:
        for pow_2 in [2**e for e in range(100)][::-1]:
            if num >= pow_2:
                suggested_n = pow_2
                raise ValueError(f'n_fft ({n_fft}) must be less than the number of points in the signal ({num}). Try {suggested_n}.')        
        
        raise ValueError(f'n_fft ({n_fft}) must be less than the number of points in the signal ({num}).')

def get_window(window):
    if window == 'hanning':
        win = hann
    elif window == 'hamming':
        win = hamming
    elif window == 'blackman':
        win = blackman
    elif window in ['rectangular', 'boxcar', None]:
        win = boxcar
    else:
        raise ValueError(f'{window} not recognized as a window!')    
    return win

def _add_order_lines(ax, orders, input_unit):
    """Adds order fan lines to ax at each order in `orders`.
    
    Parameters
    ----------
    ax : axes
        An axes object with a order waterfall countour plot
    orders : list
        List of orders to put lines at.
    input_to_hz : float, optional
        Value to scale the x value by to convert to hz, by default 1/60 (rpm to hz)

    """
    input_to_hz = _get_conversion_to_hz(input_unit)
    ax.autoscale(False)

    for order in orders:        
        x_coords = [0, ax.get_xlim()[-1]]
        y_coords = [0, x_coords[-1]*input_to_hz*order]

        if y_coords[-1] > ax.get_ylim()[-1]:
            y_coords[-1] = ax.get_ylim()[-1]
            x_coords[-1] = y_coords[-1]/input_to_hz/order

        # Add line
        ax.plot(x_coords, y_coords, color='white', linestyle='-', linewidth=2, alpha=.75)

        # Add annotation
        box_props = dict(boxstyle='round', pad=.3, fc='white', ec='black')
        ax.annotate(f'{order:.1f}', (x_coords[-1], y_coords[-1]), bbox=box_props)

def _get_conversion_to_hz(input_unit):
    """Given a unit returns the factor to convert to Hz.
    
    Parameters
    ----------
    input_unit : str
        Unit to be converted to Hz.  Must be 'rpm', 'hz', 'deg/s', 'degs/s', 'deg/sec', or 'degs/sec'.
    
    Returns
    -------
    float
        conversion factor

    """
    # Get conversion factor
    if input_unit.lower() == 'rpm':
        input_to_hz = 1/60
    elif input_unit.lower() == 'hz':
        input_to_hz = 1
    elif input_unit.lower().startswith('deg') and (input_unit.lower().endswith('/s') or input_unit.lower().endswith('/sec')):
        input_to_hz = 1/360

    return input_to_hz

def _clean_sig(sig, n_sigma):
    sig = np.array(sig)
    i_pks, _ = find_peaks(np.abs(sig), threshold=np.std(sig)*n_sigma)

    for i_pk in i_pks:
        sig[i_pk] = np.mean([sig[i_pk-1], sig[i_pk+1]])

    return list(sig), list(i_pks)

def _order_cut_plot(input_sig, freqs, Pxx, orders, input_to_hz=1/60, input_unit='rpm', y_label=None):
    """Returns a figure with suplots of order cuts.
    
    Parameters
    ----------
    input_sig : list
        Input speed signal corresponding to `Pxx` bins
    freqs : list
        Frequencies crresponding to `Pxx` bins
    Pxx : 2-D array
        Spectrum
    orders : list
        Orders to plot
    input_to_hz : float, optional
        Conversion from input units to Hz, by default 1/60 (rpm to hz)
    input_unit : str, optional
        Input signal units, by default 'rpm'
    y_label : str, optional
        Y axis lable for plots, by default None
    
    Returns
    -------
    figure
        figure with suplots of order cuts

    """
    fig, axes = plt.subplots(nrows=len(orders))
    for ax, order in zip(axes, orders):
        freqs_to_plot = [in_sig*input_to_hz*order for in_sig in input_sig]
        i_freqs = [_find_nearest(freqs, f) for f in freqs_to_plot]
        
        amp = [Pxx[i][j] for i,j in zip(i_freqs,range(len(input_sig)))]
        
        ax.plot(input_sig, amp)
        ax.set_xlabel(input_unit)

        if y_label is not None:
            ax.set_ylabel(y_label)

        ax.set_title(f'Order {order}')
        ax.grid()

    fig.set_size_inches(10,10/3*len(orders))
    fig.tight_layout()

    return fig

def _find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx



