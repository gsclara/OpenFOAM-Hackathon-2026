# OpenFOAM Hackathon: Day 1
# Understanding Scale Separation using Canonical Flow Configuration

---

## Analysis Guidelines

The snapshot provided is from an LES of turbulent channel flow at $Re_\tau \approx 550$, using the Vreman SGS model and a log-law equilibrium wall model (EQWM). The domain is $L_x \times L_y \times L_z = 12.8 \times 2.0 \times 4.8$, with grid $513 \times 128 \times 257$ cells. Use `plot_slices.py` to visualise instantaneous fields and `plot_snapshot.py` for wall-normal profiles.

### Question 1 — Where does the SGS model do the most work?

Plot wall-normal profiles of the SGS viscosity `nu_t` (available because `sgs_model=1`) and compare it to the molecular viscosity $\nu = 1/550$. Compute the ratio $\nu_t / \nu$ as a function of $y^+$ and identify the region where the subgrid-scale contribution is largest. Why does the ratio peak away from the wall despite the near-wall turbulence being most intense?

> **Hint:** The EQWM already models the wall layer, so the first off-wall cell sits at $y^+ > 1$. Think about what the Vreman model does with resolved strain rate near the wall versus in the log layer.

### Question 2 — Can you identify near-wall streaks and their scaling?

Look at the $x$-normal (streamwise) slice of `U` in the $y$–$z$ plane. Near-wall low-speed streaks should be visible. Estimate their mean spanwise spacing $\Delta z$ from the slice and non-dimensionalise by the viscous length scale $\delta_\nu = \nu / u_\tau$. Does the spacing agree with the well-known value $\Delta z^+ \approx 100$ from DNS?

> **Hint:** $u_\tau = \sqrt{|\mathrm{d}P/\mathrm{d}x| \cdot \delta}$ with $\delta = L_y/2 = 1.0$ and $\mathrm{d}P/\mathrm{d}x = 1.0$. Count streak pairs across the span and divide $L_z$ by that count to get $\Delta z$.

### Question 3 — Do the resolved fluctuations reflect the correct turbulent stress hierarchy?

From the $x$-$z$ averaged profiles of `U`, `V`, `W`, compute the resolved RMS fluctuations $u'_\mathrm{rms}$, $v'_\mathrm{rms}$, $w'_\mathrm{rms}$ as a function of $y^+$. Assess whether the LES reproduces the expected ordering $u'_\mathrm{rms} > w'_\mathrm{rms} > v'_\mathrm{rms}$ and whether the peak of $u'_\mathrm{rms}$ occurs at $y^+ \approx 15$. Discuss what the difference between the peak location in this LES and the DNS value tells you about the interaction between the resolved scales and the wall model.

> **Hint:** The `plot_snapshot.py` script already computes $x$-$z$ means. Fluctuations are the deviation from this mean — you can compute them field-by-field before averaging the squared values.


