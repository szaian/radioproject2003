#radio project
from astropy.io import fits
filename = '20260804-113216_TPI-CSCAN_LON-SUN_01#_01#.fits'
hdul = fits.open(filename)
hdul.info()
tab = hdul[1]
print(tab.columns)
print(tab.data['LEFT_POL'])
print(tab.data['Az_Offset'])
print(tab.data['El_Offset'])

import matplotlib.pyplot as plt

az_offset = tab.data['Az_Offset']
left_pol = tab.data['LEFT_POL']

plt.plot(az_offset, left_pol, 'o-')

plt.xlabel('Azimuth Offset (degrees)')
plt.ylabel('Total Power (counts)')
plt.title('Sun Cross-Scan: Azimuth')

plt.grid()
plt.show()