#radio project
from astropy.io import fits
filename = '20260804-113216_TPI-CSCAN_LON-SUN_01#_01#.fits'
hdul = fits.open(filename)
hdul.info()