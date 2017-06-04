"""Main surrogates estimation methods.

This file include the following methods :
- No surrogates
- Swap phase/amplitude through trials
- Swap amplitude
- Shuffle phase time-series
- Shuffle amplitude time-series
- Time lag
- Circular shifting
"""

import numpy as np
from joblib import Parallel, delayed
from .methods import ComputePac

__all__ = ['ComputeSurogates']


def ComputeSurogates(pha, amp, surargs, pacargs, nperm, njobs):
    """Compute surrogates using tensors and parallel computing.

    Args:
        pha: np.ndarray
            Array of phases of shapes (npha, ...)

        amp: np.ndarra
            Array of amplitudes of shapes (namp, ...)

        suragrs: tuple
            Tuple containing the arguments to pass to the suroSwitch function.

        pacargs: tuple
            Tuple containing the arguments to pass to the ComputePac function.

        nperm: int
            Number of permutations.

        njobs: int
            Number of jos for the parallel computing.

    Returns:
        suro: np.ndarray
            Array of pac surrogates of shape (nperm, npha, namp, ...)
    """
    s = Parallel(n_jobs=njobs)(delayed(_computeSur)(
                            pha, amp, surargs, pacargs) for k in range(nperm))
    return np.array(s)


def _computeSur(pha, amp, surargs, pacargs):
    """Compute surrogates.

    This is clearly not the optimal implementation. Indeed, for each loop the
    suroSwicth and ComputePac have a several "if" that slow down the execution,
    at least a little bit. And, it's not esthetic but joblib doesn't accept
    to pickle functions.

    Args:
        pha: np.ndarray
            Array of phases of shapes (npha, ...)

        amp: np.ndarra
            Array of amplitudes of shapes (namp, ...)

        suragrs: tuple
            Tuple containing the arguments to pass to the suroSwitch function.

        pacargs: tuple
            Tuple containing the arguments to pass to the ComputePac function.
    """
    # Get the surrogates :
    pha, amp = suroSwitch(pha, amp, *surargs)
    # Compute PAC on surrogates :
    return ComputePac(pha, amp, *pacargs)


def suroSwitch(pha, amp, idn, axis, traxis):
    """List of methods to compute surrogates.

    The surrogates are used to normalized the cfc value. It help to determine
    if the cfc is reliable or not. Usually, the surrogates used the same cfc
    method on surrogates data.
    Here's the list of methods to compute surrogates:
    - No surrogates
    - Swap phase/amplitude across trials
    - Swap amplitude across trials
    - Shuffle phase time-series
    - Shuffle amplitude time-series
    - Time lag
    - circular shifting

    Each method should return the surrogates, the mean of the surrogates and
    the deviation of the surrogates.
    """
    # No surrogates
    if idn == 0:
        return None

    # Swap phase/amplitude across trials :
    elif idn == 1:
        return SwapPhaAmp(pha, amp, traxis)

    # Swap phase :
    elif idn == 2:
        return SwapPha(pha, amp, traxis)

    # Swap amplitude :
    elif idn == 3:
        return SwapAmp(pha, amp, traxis)

    # Shuffle phase/amplitude time-series :
    elif idn == 4:
        return ShufflePhaAmp(pha, amp, axis)

    # Shuffle phase values
    elif idn == 5:
        return ShufflePha(pha, amp, axis)

    # Shuffle amplitude values
    elif idn == 6:
        return ShuffleAmp(pha, amp, axis)

    # Introduce a time lag
    elif idn == 7:
        raise(NotImplementedError)

    # Circular shifting
    elif idn == 8:
        raise(NotImplementedError)

    else:
        raise ValueError(str(idn) + " is not recognized as a valid surrogates"
                         " evaluation method.")


###############################################################################
###############################################################################
#                            SWAPING
###############################################################################
###############################################################################


def SwapPhaAmp(pha, amp, axis):
    """Swap phase/amplitude trials (Tort, 2010).

    Args:
        pha: np.ndarray
            Array of phases of shapes (npha, ...)

        amp: np.ndarra
            Array of amplitudes of shapes (namp, ...)

        axis: int
            Location of the trial axis.

    Return:
        pha: np.ndarray
            Swapped version of phases of shapes (npha, ...)

        amp: np.ndarra
            Swapped version of amplitudes of shapes (namp, ...)
    """
    npha = pha.shape[0]
    pa = _dimswap(np.concatenate((pha, amp)), axis=axis)

    return _dimswap(pa[0:npha, ...], axis), _dimswap(pa[npha::, ...], axis)


def SwapAmp(pha, amp, axis):
    """Swap amplitude across trials, (Bahramisharif, 2013).

    Args:
        pha: np.ndarray
            Array of phases of shapes (npha, ...)

        amp: np.ndarra
            Array of amplitudes of shapes (namp, ...)

        axis: int
            Location of the trial axis.

    Return:
        pha: np.ndarray
            Original version of phases of shapes (npha, ...)

        amp: np.ndarra
            Swapped version of amplitudes of shapes (namp, ...)
    """
    return pha, _dimswap(amp, axis)


def SwapPha(pha, amp, axis):
    """Swap phase across trials.

    Args:
        pha: np.ndarray
            Array of phases of shapes (npha, ...)

        amp: np.ndarra
            Array of amplitudes of shapes (namp, ...)

        axis: int
            Location of the trial axis.

    Return:
        pha: np.ndarray
            Swapped version of phases of shapes (npha, ...)

        amp: np.ndarra
            Original version of amplitudes of shapes (namp, ...)
    """
    return _dimswap(pha, axis), amp


def _dimswap(x, axis=0):
    """Swap values into an array at a specific axis.

    Args:
        x: np.ndarray
            Array of data to swap

    Kargs:
        axis: int, optional, (def: 0)
            Axis along which to perform swapping.

    Returns:
        x: np.ndarray
            Swapped version of x.
    """
    # Dimension vector :
    dimvec = [slice(None)] * x.ndim
    # Random integer vector :
    rndvec = np.arange(x.shape[axis])
    np.random.shuffle(rndvec)
    dimvec[axis] = rndvec
    # Return a swapped version of x :
    return x[dimvec]

###############################################################################
###############################################################################
#                            SHUFFLING
###############################################################################
###############################################################################

def ShufflePhaAmp(pha, amp, axis):
    """Randomly shuffle amplitudes

    [pha] = (nPha, npts, ntrials)
    [amp] = (nAmp, npts, ntrials)
    """
    return _dimswap(pha, axis), _dimswap(amp, axis)


def ShufflePha(pha, amp, axis):
    """Randomly shuffle phase

    [pha] = (nPha, npts, ntrials)
    [amp] = (nAmp, npts, ntrials)
    """
    return _dimswap(pha, axis), amp


def ShuffleAmp(pha, amp, axis):
    """Randomly shuffle amplitudes

    [pha] = (nPha, npts, ntrials)
    [amp] = (nAmp, npts, ntrials)
    """
    return pha, _dimswap(amp, axis)