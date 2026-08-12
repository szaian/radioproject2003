import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# VALUES
# ============================================================

# Beam width
beam_measured = 6.34
beam_measured_unc = 0.13
beam_theoretical = 4.89

# Antenna temperature
Tant_measured = 647
Tant_measured_unc = 63
Tant_theoretical = 1843

# Percentage comparisons
beam_broader = ((beam_measured - beam_theoretical)
                / beam_theoretical) * 100

Tant_percentage = (Tant_measured / Tant_theoretical) * 100


# ============================================================
# COLOURS
# ============================================================

dark_purple = "#8E4585"
pink = "#D978B5"


# ============================================================
# GRAPH 1: BEAM WIDTH
# ============================================================

fig, ax = plt.subplots(figsize=(10, 7))

labels = ["Measured", "Theoretical"]
values = [beam_measured, beam_theoretical]
colours = [dark_purple, pink]

bars = ax.bar(
    labels,
    values,
    width=0.55,
    color=colours,
    edgecolor="black",
    linewidth=1.0
)

# Value labels above bars
ax.text(
    bars[0].get_x() + bars[0].get_width() / 2,
    beam_measured + 0.12,
    "6.34°",
    ha="center",
    va="bottom",
    fontsize=14
)

ax.text(
    bars[1].get_x() + bars[1].get_width() / 2,
    beam_theoretical + 0.12,
    "4.89°",
    ha="center",
    va="bottom",
    fontsize=14
)

# Title and axes
ax.set_title(
    "Measured and Theoretical Azimuth Beam Width",
    fontsize=18,
    pad=18
)

ax.set_ylabel(
    "Beam FWHM (degrees)",
    fontsize=14
)

ax.tick_params(axis="both", labelsize=12)

# Grid
ax.yaxis.grid(
    True,
    linestyle="--",
    alpha=0.35
)

ax.set_axisbelow(True)

# Give extra space above and below
ax.set_ylim(0, 8.0)

# ------------------------------------------------------------
# Top explanatory box
# ------------------------------------------------------------

ax.text(
    0.5,
    0.94,
    f"Measured beam is {beam_broader:.1f}% broader\n"
    "than the diffraction limit",
    transform=ax.transAxes,
    ha="center",
    va="center",
    fontsize=12,
    bbox=dict(
        boxstyle="round,pad=0.5",
        facecolor="white",
        edgecolor="gray",
        linewidth=1.2
    )
)

# ------------------------------------------------------------
# Equation box underneath graph
# ------------------------------------------------------------

equation_text = (
    r"$\bf{Measured:}$"
    "\n"
    r"$P(x)=A\exp\left[-\frac{(x-x_0)^2}{2\sigma^2}\right]$"
    "\n"
    r"$FWHM=2\sqrt{2\ln2}\,\sigma=2.355\sigma$"
    "\n\n"
    r"$\bf{Theoretical:}$"
    "\n"
    r"$FWHM=1.22\frac{\lambda}{D}$"
)

fig.text(
    0.5,
    0.025,
    equation_text,
    ha="center",
    va="bottom",
    fontsize=11,
    bbox=dict(
        boxstyle="round,pad=0.65",
        facecolor="white",
        edgecolor=dark_purple,
        linewidth=1.4
    )
)

# Leave room for equation box
plt.subplots_adjust(
    left=0.12,
    right=0.96,
    top=0.87,
    bottom=0.34
)

plt.savefig(
    "beam_width_theoretical_vs_measured.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# GRAPH 2: ANTENNA TEMPERATURE
# ============================================================

fig, ax = plt.subplots(figsize=(10, 7))

labels = ["Measured", "Theoretical"]
values = [Tant_measured, Tant_theoretical]
colours = [dark_purple, pink]

bars = ax.bar(
    labels,
    values,
    width=0.55,
    color=colours,
    edgecolor="black",
    linewidth=1.0
)

# Value labels above bars
ax.text(
    bars[0].get_x() + bars[0].get_width() / 2,
    Tant_measured + 45,
    "647 K",
    ha="center",
    va="bottom",
    fontsize=14
)

ax.text(
    bars[1].get_x() + bars[1].get_width() / 2,
    Tant_theoretical + 45,
    "1843 K",
    ha="center",
    va="bottom",
    fontsize=14
)

# Title and axes
ax.set_title(
    "Measured and Theoretical Antenna Temperature",
    fontsize=18,
    pad=18
)

ax.set_ylabel(
    "Antenna Temperature (K)",
    fontsize=14
)

ax.tick_params(axis="both", labelsize=12)

# Grid
ax.yaxis.grid(
    True,
    linestyle="--",
    alpha=0.35
)

ax.set_axisbelow(True)

# Y-axis range
ax.set_ylim(0, 2500)

# ------------------------------------------------------------
# Top explanatory box
# ------------------------------------------------------------

ax.text(
    0.5,
    0.94,
    f"Measured is {Tant_percentage:.1f}% of theoretical\n"
    f"(Aperture efficiency ≈ {Tant_percentage:.1f}%)",
    transform=ax.transAxes,
    ha="center",
    va="center",
    fontsize=12,
    bbox=dict(
        boxstyle="round,pad=0.5",
        facecolor="white",
        edgecolor="gray",
        linewidth=1.2
    )
)

# ------------------------------------------------------------
# Equation box underneath graph
# ------------------------------------------------------------

equation_text = (
    r"$\bf{Measured:}$"
    "\n"
    r"$T_{\mathrm{ant,meas}}=\frac{S_{\mathrm{meas}}}{G}$"
    "\n"
    r"$S_{\mathrm{meas}}:$ measured antenna signal"
    r"$\qquad G:$ forward gain (K/Jy)"
    "\n\n"
    r"$\bf{Theoretical:}$"
    "\n"
    r"$T_{\mathrm{ant,theory}}=\frac{A S_\nu}{2k}$"
    "\n"
    r"$S_\nu:$ source flux density"
    r"$\qquad k:$ Boltzmann constant"
)

fig.text(
    0.5,
    0.025,
    equation_text,
    ha="center",
    va="bottom",
    fontsize=11,
    bbox=dict(
        boxstyle="round,pad=0.65",
        facecolor="white",
        edgecolor=dark_purple,
        linewidth=1.4
    )
)

# Leave room for equation box
plt.subplots_adjust(
    left=0.12,
    right=0.96,
    top=0.87,
    bottom=0.34
)

plt.savefig(
    "antenna_temperature_theoretical_vs_measured.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# FINISHED
# ============================================================

print("Graphs successfully saved:")
print("1. beam_width_theoretical_vs_measured.png")
print("2. antenna_temperature_theoretical_vs_measured.png")