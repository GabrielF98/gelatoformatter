"""
Ensure that wavelength values are evenly spaced so the spectrum can be used in Gelato.
The data should be provided in the form of a GRBSN webtool standard spectrum file.
"""
import argparse
import os

import numpy as np
from scipy.interpolate import interp1d

# Set the min and max wavelengths for the trimming. By default use the Gelato wavelength range.
MIN_WAVELENGTH = 3500
MAX_WAVELENGTH = 9000


def load_spectrum(
    filename, *args, wave_col=0, flux_col=1, time_col=None, **kwargs
):
    """
    Load a spectrum from a file.
    Extract the wavelength column, flux column and (if it exists) the time column.
    Return these as numpy arrays.

    wave_col - The index of the wavelength column.
    flux_col - The index of the flux column.
    time_col - The index of any elapsed time column in the file,
               useful if there are multiple epochs in one file.
    """

    if time_col is None:
        wave, flux = np.genfromtxt(
            fname=filename,
            unpack=True,
            usecols=(wave_col, flux_col),
            *args,
            **kwargs,
        )
        time = None

    else:
        wave, flux, time = np.genfromtxt(
            fname=filename,
            unpack=True,
            usecols=(wave_col, flux_col, time_col),
            *args,
            **kwargs,
        )

    return wave, flux, time


def trim_spectrum(wave, flux):
    """
    Return the section of the wave and the flux arrays for which MIN_WAVELENGTH<wave<MAX_WAVELENGTH
    """
    trim_wave = wave[(wave > MIN_WAVELENGTH) & (wave < MAX_WAVELENGTH)]
    trim_flux = flux[(wave > MIN_WAVELENGTH) & (wave < MAX_WAVELENGTH)]
    return trim_wave, trim_flux


def rescale_spectrum(wave, flux):
    """
    Rescale the spectrum onto a new wavelength axis. Compute the flux in these new bins.

    Procedure:

    - Calculate the min delta for the wavelengths. Round to 2 d.p.
    - Make an array where all wavelengths have this diff.
    - Rescale the flux data onto this wavelength array with 1d interpolation.
    """
    min_diff = round(min(np.diff(wave)), 2)
    rescaled_wavelength = np.arange(wave[0], wave[-1], min_diff)
    rescaled_flux = interp1d(wave, flux)(rescaled_wavelength)

    return rescaled_wavelength, rescaled_flux


def run_rescaler(filename, *args, **kwargs):
    """
    Run all of the above functions to return the rescaled spectrum.

    Procedure:

    - Load input spectrum from a file.
    - Loop over epochs (if there are any).
    - Trim spectra.
    - Rescale the wavelength and re-bin the flux.
    - Stack the output into a 2-D array.
    - Save this array, appending _rescaled to the filename
      (and the epoch if there are multiple epochs).

    Rescaled spectrum has evenly spaced wavelength bins.
    """

    wavelengths, fluxes, times = load_spectrum(
        filename=filename, *args, **kwargs
    )

    # If only one epoch, do that one epoch.
    if times is None:
        trim_wave, trim_flux = trim_spectrum(wavelengths, fluxes)
        rescaled_wave, rescaled_flux = rescale_spectrum(trim_wave, trim_flux)

        # Make a numpy 2D array with wavelength and flux
        data = np.vstack((np.round(rescaled_wave, 2), rescaled_flux)).T

        # Save
        np.savetxt(
            os.path.splitext(filename)[0] + "_rescaled.txt",
            data,
            fmt="%1.2f %1.7e",
            delimiter="\t",
        )

    # Select the spectra by epoch. This handles the case where one file contains many spectra.
    else:
        epochs = np.unique(times)
        for epoch in epochs:
            epoch_indices = np.where(times == epoch)[0]
            wave = wavelengths[epoch_indices]
            flux = fluxes[epoch_indices]

            trim_wave, trim_flux = trim_spectrum(wave, flux)
            rescaled_wave, rescaled_flux = rescale_spectrum(
                trim_wave, trim_flux
            )

            # Make a numpy 2D array with wavelength and flux
            data = np.vstack((np.round(rescaled_wave, 2), rescaled_flux)).T

            # Save
            np.savetxt(
                os.path.splitext(filename)[0]
                + "_"
                + str(round(epoch, 2))
                + "_days_rescaled.txt",
                data,
                fmt="%1.2f %1.7e",
                delimiter="\t",
            )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Format a spectrum for upload to GELATO identification tool."
    )
    parser.add_argument(
        "--filename",
        type=str,
        required=True,
        help="GRBSN Webtool Master file or a text file containing spectral data.",
    )
    parser.add_argument(
        "--wavecol",
        type=int,
        default=0,
        help="Index of the column in the file which has the time information. Default is column 0.",
    )
    parser.add_argument(
        "--fluxcol",
        type=int,
        default=1,
        help="Index of the column in the file which has the time information. Default is column 1.",
    )
    parser.add_argument(
        "--timecol",
        type=int,
        default=None,
        help="Index of the column in the file which has the elapsed time since explosion. \
                This is useful if you have multiple spectra for the same event in one file.",
    )
    parser.add_argument(
        "--delim",
        default=",",
        type=str,
        help="File delimiter (tab/comma/space etc.)",
    )
    parser.add_argument(
        "--hdr",
        default=0,
        type=int,
        help="Number of header lines in your file. These will be skipped.",
    )
    args = parser.parse_args()

    run_rescaler(
        filename=args.filename,
        wave_col=args.wavecol,
        flux_col=args.fluxcol,
        time_col=args.timecol,
        skip_header=args.hdr,
        delimiter=args.delim,
    )
