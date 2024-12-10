"""
Ensure that wavelength values are evenly spaced so the spectrum can be used in Gelato.
The data should be provided in the form of a GRBSN webtool standard spectrum file.
"""
import argparse

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


def rescaler(spectrum_data, filename):

    wavelength_allspectra = spectrum_data['obs_wavelength'].to_numpy(dtype=np.float64)
    flux_allspectra = spectrum_data['flux'].to_numpy()
    time_allspectra = spectrum_data['time'].to_numpy()

    # Select the spectra by epoch. This handles the case where one file contains many spectra.
    epochs = list(set(time_allspectra))

    # Loop over epochs.
    for epoch in epochs:
        print(epoch)
        epoch_indices = np.where(time_allspectra==epoch)[0]
        wavelength = wavelength_allspectra[epoch_indices]
        flux = flux_allspectra[epoch_indices]

        # Remove the data that is outside the operating range of Gelato

        u = np.where(wavelength>9000)[0]
        upper_index = -1
        if len(u) != 0:
            upper_index = u[0]

        lower_index = 0
        l = np.where(wavelength<3500)[0]
        if len(l) != 0:
            lower_index = l[-1]

        if upper_index == -1:
            wavelength = wavelength[lower_index:]
            flux = flux[lower_index:]

        else:
            wavelength = wavelength[lower_index:upper_index]
            flux = flux[lower_index:upper_index]

        # Calculate the min delta for the wavelengths. Make an array where all wavelengths have this diff.
        diffs = np.diff(wavelength)
        min_diff = min(diffs)
        max1 = wavelength[-1]
        max2 = wavelength[0]+(min_diff)*(len(wavelength))
        max_wlength = min(max1, max2)
        new_wavelength = np.linspace(wavelength[0], max_wlength, len(wavelength)+1)

        # Rescale the data with 1d interpolation.
        new_flux = interp1d(wavelength, flux)(new_wavelength)

        # Make a numpy 2D array with wavelength and flux
        data = np.vstack((np.round(new_wavelength, 2), new_flux)).T

        # Save
        np.savetxt(filename[:-4]+'_'+str(epoch)+'days_rescaled.txt', data,  fmt='%1.2f %1.7e')

def main(filename):
    spectrum_data = pd.read_csv(filename, sep='\t')
    rescaler(spectrum_data=spectrum_data, filename=filename)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Downlink data from an onboard storage channel.')
    parser.add_argument('--file', type=str,
                        required=True, help='GRBSN file containing spectral data.')
    parser.add_argument('--wavecol', type=str, default=0, help='Index of the column in the file which has the time information. Default is column 0.')
    parser.add_argument('--fluxcol', type=str, default=0, help='Index of the column in the file which has the time information. Default is column 1.')
    parser.add_argument('--timecol', type=str, help='Index of the column in the file which has the time information, if there is one.')
    parser.add_argument('--delim', type=str, help='File delimiter (tab/other)')
    args = parser.parse_args()
    main(args.file)