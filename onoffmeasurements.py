from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt


def get_on_spectrum(filename, name):

    hdul = fits.open(filename)
    tab = hdul[1]

    statuses = np.char.strip(tab.data['STATUS'].astype(str))
    on_index = np.where(statuses == 'on')[0][0]

    spectrum = np.asarray(tab.data['LEFT_POL'][on_index], dtype=float)

    hdul.close()

    # Remove zero-filled channels
    valid = spectrum != 0
    spectrum = spectrum[valid]

    print(name)
    print("Number of valid channels:", len(spectrum))
    print("Minimum:", np.min(spectrum))
    print("Maximum:", np.max(spectrum))
    print("Mean:", np.mean(spectrum))

    return spectrum


# ============================================================
# SCP - COLD SOURCE
# ============================================================

scp = get_on_spectrum(
    '20260804-120340_SPECTRUM-PROJ01-SCP_03#_01#.fits',
    'SCP (COLD)'
)


# ============================================================
# TREES - HOT SOURCE
# ============================================================

trees = get_on_spectrum(
    '20260804-120653_SPECTRUM-PROJ01-TREES_04#_01#.fits',
    'TREES (HOT)'
)


# ============================================================
# PLOT SCP
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(np.arange(len(scp)), scp, color='deeppink')

plt.xlabel('Spectral Channel')
plt.ylabel('LEFT_POL Signal (counts)')
plt.title('SCP ON Spectrum')

plt.grid()

plt.savefig('scp_on_spectrum.png', dpi=300, bbox_inches='tight')
plt.close()


# ============================================================
# PLOT TREES
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(np.arange(len(trees)), trees, color='purple')

plt.xlabel('Spectral Channel')
plt.ylabel('LEFT_POL Signal (counts)')
plt.title('Trees ON Spectrum')

plt.grid()

plt.savefig('trees_on_spectrum.png', dpi=300, bbox_inches='tight')
plt.close()


# ============================================================
# PLOT BOTH TOGETHER
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    np.arange(len(scp)),
    scp,
    color='deeppink',
    label='SCP (cold)'
)

plt.plot(
    np.arange(len(trees)),
    trees,
    color='purple',
    label='Trees (hot)'
)

plt.xlabel('Spectral Channel')
plt.ylabel('LEFT_POL Signal (counts)')
plt.title('SCP and Trees ON Spectra')

plt.legend()
plt.grid()

plt.savefig('scp_trees_comparison.png', dpi=300, bbox_inches='tight')
plt.close()


print("\nGraphs saved:")
print("scp_on_spectrum.png")
print("trees_on_spectrum.png")
print("scp_trees_comparison.png")