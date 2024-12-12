# gelatoformatter
Python code to apply [GELATO](https://gelato.tng.iac.es/) formatting to a text file containing a supernova spectrum (or multiple SN spectra). 

This project was developed by Gabriel Finneran at University College Dublin, Ireland. You can contact me by email here: gabfin15@gmail.com.

If you use this code in your work, please consider adding an acknowledgment such as:

```
This work has made use of the \texttt{gelatoformatter} Python code,
developed by Gabriel Finneran at University College Dublin, Ireland.
Available at: \url{https://github.com/GabrielF98/gelatoformatter}
```

## Motivation
If you wish to use the [GELATO](https://gelato.tng.iac.es/) supernova identification tool, your spectrum must be 'correctly formatted', as GELATO will reject an improperly formatted supernova spectra. 

In this case 'correctly formatted' means that there must be wavelength and flux columns, the wavelength array must be equally spaced and the wavelength range must be within the GELATO range of 3500-9000 angstroms.

One solution to this problem is to provide GELATO with the FITS files of the spectra. However, this approach won't work if you don't have access to the FITS files; this is often the case when sourcing the spectrum from an online repository, such as [WISeREP](https://www.wiserep.org/) or [TNS](https://www.wis-tns.org/). 

This was the motivation for creating a simple Python script which can format any text spectrum file for use with Gelato.

## How it works

The code loads an input spectrum file specified by the user. This may be a file containing a single spectrum, or it may contain multiple spectra, provided that an elapsed-time since explosion column exists.

The code then trims the wavelength array so it fits within the GELATO range (if necessary).

The code then bins the spectrum so that each bin is the same width as the minimum wavelength bin in the input spectrum. The flux for each bin is computed using linear interpolation. Wavelengths of the bins are rounded to 2 decimal places.

The code then saves the output file, appending '_rescaled' to the filename.

**Note:**
In the case of a file with multiple spectra, the code uses the elapsed-time column to separate the spectra by age. The code then performs the above steps on all spectra. The filenames include the elapsed time.

## Running the code
The code can be imported as a library if desired. The code can be found in the rescale.py file.

Alternatively it can be run from command line. You can get help with running the code using:

```
python rescale.py -h
usage: rescale.py [-h] --filename FILENAME [--wavecol WAVECOL] [--fluxcol FLUXCOL] [--timecol TIMECOL] [--delim DELIM] [--hdr HDR]

Format a spectrum for upload to GELATO identification tool.

options:
  -h, --help           show this help message and exit
  --filename FILENAME  GRBSN Webtool Master file or a text file containing spectral data.
  --wavecol WAVECOL    Index of the column in the file which has the time information. Default is column 0.
  --fluxcol FLUXCOL    Index of the column in the file which has the time information. Default is column 1.
  --timecol TIMECOL    Index of the column in the file which has the elapsed time since explosion. This is useful if you have multiple
                       spectra for the same event in one file.
  --delim DELIM        File delimiter (tab/comma/space etc.)
  --hdr HDR            Number of header lines in your file. These will be skipped.
```

To run using a spectrum file from TNS (such as the one in the exampledata folder for SN2020bvc):

```
python rescale.py --filename exampledata/tns_2020bvc_2020-02-05_13-08-02_FTN_FLOYDS-N_Global_SN_Project.ascii  --fluxcol=1 --wavecol=0
```

If you are using a master spectrum file containing data from the [GRBSN webtool](https://grbsn.watchertelescope.ie), you can run it like this (see the exampledata folder for the file):

```
python rescale.py --filename exampledata/SN2020bvc_Spectra_Master.txt --timecol=0 --fluxcol=2 --wavecol=1 --hdr=1 --delim="        "
```

## Sources of example files
Files in the [exampledata/](https://github.com/GabrielF98/gelatoformatter/tree/main/exampledata) folder are taken from TNS and GRBSN.

[SN2020bvc_Spectra_Master.txt](https://github.com/GabrielF98/gelatoformatter/tree/main/exampledata) -> https://grbsn.watchertelescope.ie/SN2020bvc


[tns_2020bvc_2020-02-05_13-08-02_FTN_FLOYDS-N_Global_SN_Project.ascii](https://github.com/GabrielF98/gelatoformatter/tree/main/exampledata) -> https://www.wis-tns.org/object/2020bvc

