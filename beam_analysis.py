# ============================================================
# AST2003 Radio Project
# Sun Cross-Scan Beam Characterization
# ============================================================

from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# ============================================================
# 1. Open the FITS file
# ============================================================

filename = '20260804-113216_TPI-CSCAN_LON-SUN_01#_01#.fits'

hdul = fits.open(filename)
print("===== PRIMARY HEADER =====")
print(hdul[1].header)

hdul.info()

tab = hdul[1]


# ============================================================
# 2. Extract the data
# ============================================================

az_offset = np.array(
    tab.data['Az_Offset'],
    dtype=float
)

left_pol = np.array(
    tab.data['LEFT_POL'],
    dtype=float
)


# ============================================================
# 3. Calculate the off-Sun baseline
# ============================================================

baseline_indices = np.r_[0:6, 20:25]

baseline_measurements = left_pol[baseline_indices]

baseline = np.mean(
    baseline_measurements
)

baseline_noise = np.std(
    baseline_measurements,
    ddof=1
)

baseline_uncertainty = (
    baseline_noise /
    np.sqrt(len(baseline_measurements))
)


print()
print("================================================")
print("BASELINE")
print("================================================")

print(
    f"Baseline = {baseline:.2f} counts"
)

print(
    f"Baseline scatter = {baseline_noise:.2f} counts"
)

print(
    f"Baseline uncertainty = "
    f"{baseline_uncertainty:.2f} counts"
)


# ============================================================
# 4. Subtract the baseline
# ============================================================

corrected_power = (
    left_pol - baseline
)


# ============================================================
# 5. Calculate uncertainty of corrected measurements
# ============================================================

corrected_power_uncertainty = np.sqrt(
    baseline_noise**2 +
    baseline_uncertainty**2
)

print()
print(
    f"Corrected-power uncertainty = "
    f"{corrected_power_uncertainty:.2f} counts"
)


y_errors = np.full(
    len(corrected_power),
    corrected_power_uncertainty
)


# ============================================================
# 6. Define the Gaussian function
# ============================================================

def gaussian(x, A, x0, sigma):

    return A * np.exp(
        -(x - x0)**2 /
        (2 * sigma**2)
    )


# ============================================================
# 7. Initial guesses
# ============================================================

A_guess = np.max(
    corrected_power
)

x0_guess = az_offset[
    np.argmax(corrected_power)
]

sigma_guess = 3.0

initial_guess = [
    A_guess,
    x0_guess,
    sigma_guess
]


# ============================================================
# 8. Fit the Gaussian
# ============================================================

fit_parameters, covariance = curve_fit(
    gaussian,
    az_offset,
    corrected_power,
    p0=initial_guess,
    sigma=y_errors,
    absolute_sigma=True,
    maxfev=10000
)


# ============================================================
# 9. Extract fitted parameters
# ============================================================

A_fit = fit_parameters[0]

x0_fit = fit_parameters[1]

sigma_fit = fit_parameters[2]


# ============================================================
# 10. Calculate parameter uncertainties
# ============================================================

A_error = np.sqrt(
    covariance[0, 0]
)

x0_error = np.sqrt(
    covariance[1, 1]
)

sigma_error = np.sqrt(
    covariance[2, 2]
)


print()
print("================================================")
print("GAUSSIAN FIT")
print("================================================")

print(
    f"Peak amplitude A = "
    f"{A_fit:.2f} +/- {A_error:.2f} counts"
)

print(
    f"Beam centre x0 = "
    f"{x0_fit:.4f} +/- "
    f"{x0_error:.4f} degrees"
)

print(
    f"Sigma = "
    f"{sigma_fit:.4f} +/- "
    f"{sigma_error:.4f} degrees"
)


# ============================================================
# 11. Calculate goodness of fit
# ============================================================

model_power = gaussian(
    az_offset,
    A_fit,
    x0_fit,
    sigma_fit
)

residuals = (
    corrected_power - model_power
)

chi_squared = np.sum(
    (residuals / y_errors)**2
)

degrees_of_freedom = (
    len(corrected_power) - 3
)

reduced_chi_squared = (
    chi_squared /
    degrees_of_freedom
)


print()
print("================================================")
print("GOODNESS OF FIT")
print("================================================")

print(
    f"Chi-squared = "
    f"{chi_squared:.2f}"
)

print(
    f"Degrees of freedom = "
    f"{degrees_of_freedom}"
)

print(
    f"Reduced chi-squared = "
    f"{reduced_chi_squared:.3f}"
)


# ============================================================
# 12. Calculate FWHM
# ============================================================

fwhm_factor = (
    2 * np.sqrt(2 * np.log(2))
)

fwhm = (
    fwhm_factor * sigma_fit
)


# ============================================================
# 13. Scale uncertainty using reduced chi-squared
# ============================================================

fwhm_uncertainty_formal = (
    fwhm_factor * sigma_error
)

fwhm_uncertainty = (
    fwhm_uncertainty_formal *
    np.sqrt(reduced_chi_squared)
)


print()
print("================================================")
print("FINAL BEAM WIDTH")
print("================================================")

print(
    f"FWHM = {fwhm:.4f} +/- "
    f"{fwhm_uncertainty:.4f} degrees"
)

print(
    f"Scaled FWHM uncertainty = "
    f"{fwhm_uncertainty:.4f} degrees"
)


# ============================================================
# 14. Create smooth Gaussian curve
# ============================================================

x_smooth = np.linspace(
    np.min(az_offset),
    np.max(az_offset),
    500
)

y_smooth = gaussian(
    x_smooth,
    A_fit,
    x0_fit,
    sigma_fit
)


# ============================================================
# 15. Plot the observed data
# ============================================================

plt.figure(
    figsize=(9, 6)
)

plt.errorbar(
    az_offset,
    corrected_power,
    yerr=y_errors,
    fmt='o',
    color='purple',
    ecolor='purple',
    capsize=3,
    label='Observed data'
)


# ============================================================
# 16. Plot the Gaussian fit
# ============================================================

plt.plot(
    x_smooth,
    y_smooth,
    color='pink',
    linewidth=2,
    label='Gaussian fit'
)


# ============================================================
# 17. Labels and title
# ============================================================

plt.xlabel(
    'Azimuth Offset (degrees)'
)

plt.ylabel(
    'Baseline-Corrected Power (counts)'
)

plt.title(
    'Sun Cross-Scan: Azimuth Beam Characterization'
)

plt.grid()

plt.legend()


# ============================================================
# 18. Display FWHM on graph
# ============================================================

result_text = (
    'FWHM = 6.34 +/- 0.13°'
)

plt.text(
    0.03,
    0.95,
    result_text,
    transform=plt.gca().transAxes,
    verticalalignment='top'
)


# ============================================================
# 19. Save graph
# ============================================================

plt.savefig(
    'sun_cross_scan_gaussian_fit.png',
    dpi=300,
    bbox_inches='tight'
)

plt.close()


print()
print(
    "Graph saved as: "
    "sun_cross_scan_gaussian_fit.png"
)