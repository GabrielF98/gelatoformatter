# gelatoflattener
Python code for formatting a text file containing a supernova spectrum.

This is especially beneficial if you wish to use the [GELATO](https://gelato.tng.iac.es/) supernova identification tool; this tool will reject a supernova spectrum if it isn't correctly formatted. In this case correctly formatted means having the right layout and separators, along with the wavelength array being evenly spaced.

An alternative which usually avoids this issue is to use FITS files with GELATO. However, this approach won't work if you don't have access to the FITS files. This is often the case when sourcing the spectrum from an online repository, such as [WISeREP](https://www.wiserep.org/) or [TNS](https://www.wis-tns.org/). 
