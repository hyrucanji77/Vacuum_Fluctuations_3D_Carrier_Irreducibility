#!/usr/bin/env python3
"""Reproduce nominal scales and analytic checks in the accompanying manuscript.

No experimental data are simulated or fitted. Inputs come from Zhang et al.,
arXiv:2608.20311v1, Supplementary Materials (experimental system), except
h and k_B (SI definitions) and the explicitly rounded nominal isotope mass.
Python 3.10+; standard library only. Outputs are written beside this script.
"""
from __future__ import annotations
from collections import Counter
import csv
import json
import math
from pathlib import Path

H = 6.62607015e-34                  # Exact SI defining constant, J s.
HBAR = H / (2.0 * math.pi)
KB = 1.380649e-23                  # Exact SI defining constant, J K^-1.
U_NOMINAL = 1.66054e-27             # Deliberately rounded, kg; not a new mass measurement.
MASS = 39.0 * U_NOMINAL
FZ = 1000.0                       # Rounded source-reported frequency, Hz.
L = 33e-6                         # Rounded source-reported in-plane side, m.
ALPHA = 0.72                      # Rounded source convention, not exact 1 - 0.53^2.
MU_S_OVER_H = 900.0
MU_D_OVER_H = 120.0
OUT = Path(__file__).resolve().parent


def scale_row(frequency_hz: float) -> dict[str, float]:
    if not math.isfinite(frequency_hz) or frequency_hz <= 0:
        raise ValueError('The confinement frequency must be finite and positive.')
    omega = 2 * math.pi * frequency_hz
    ell = math.sqrt(HBAR / (MASS * omega))
    sigma = ell / math.sqrt(2)
    gap = HBAR * omega
    return {
        'frequency_kHz': frequency_hz / 1000,
        'oscillator_length_um': ell * 1e6,
        'rms_width_um': sigma * 1e6,
        'gap_over_kB_nK': gap / KB * 1e9,
        'zero_point_over_kB_nK': gap / (2 * KB) * 1e9,
        'kinetic_over_kB_nK': gap / (4 * KB) * 1e9,
        'g2D_relative_to_1kHz': math.sqrt(frequency_hz / FZ),
    }


def check_close(a: float, b: float, name: str, records: list[dict],
                tolerance: float = 2e-11, *, category: str = 'analytic_check') -> None:
    error = abs(a - b) / max(abs(a), abs(b), 1e-30)
    passed = math.isfinite(a) and math.isfinite(b) and error < tolerance
    records.append({'check': name, 'category': category, 'actual': a, 'expected': b,
                    'relative_error': error, 'tolerance': tolerance, 'passed': passed})
    if not passed:
        raise ArithmeticError(f'{name}: {a!r} != {b!r}; relative error {error:g}')



def check_absolute(actual: float, expected: float, name: str, records: list[dict],
                   tolerance: float = 2e-11, *, category: str = 'analytic_check') -> None:
    """Check identities which may vanish; use absolute tolerance near zero."""
    error = abs(actual - expected)
    passed = math.isfinite(actual) and math.isfinite(expected) and error <= tolerance
    records.append({'check': name, 'category': category, 'actual': actual, 'expected': expected,
                    'absolute_error': error,
                    'relative_error': error / max(1., abs(actual), abs(expected)),
                    'tolerance': tolerance, 'tolerance_type': 'absolute', 'passed': passed})
    if not passed:
        raise ArithmeticError(f'{name}: absolute error {error:g}')


def check_upper(actual: float, bound: float, name: str, records: list[dict],
                tolerance: float = 2e-11, *, category: str = 'analytic_check') -> None:
    """Check a non-negative amplitude against a mathematically specified bound."""
    violation = max(0., actual - bound, -actual)
    passed = (math.isfinite(actual) and math.isfinite(bound)
              and violation <= tolerance)
    records.append({'check': name, 'category': category, 'actual': actual, 'expected': bound,
                    'kind': 'upper_bound', 'absolute_violation': violation,
                    'relative_error': violation / max(1., abs(actual), abs(bound)),
                    'tolerance': tolerance, 'passed': passed})
    if not passed:
        raise ArithmeticError(f'{name}: {actual:g} exceeds {bound:g}')


def simpson(function, low: float, high: float, intervals: int = 6000) -> float:
    """Finite-interval Simpson quadrature for explicitly declared toy profiles."""
    if intervals <= 0 or intervals % 2 or high <= low:
        raise ValueError('Simpson integration requires positive even intervals and low < high.')
    step = (high - low) / intervals
    return step / 3 * math.fsum(
        (1 if i in (0, intervals) else 4 if i % 2 else 2)
        * function(low + step * i) for i in range(intervals + 1))


def revision_checks(records: list[dict]) -> dict:
    """Additional analytic benchmarks; none estimates actual pulse leakage or axial temperature."""
    ratio = 20. * ALPHA * MU_S_OVER_H / FZ
    check_close(ratio, 12.96, 'readout scaled energy / nominal transverse gap', records)
    unscaled = math.sqrt(ALPHA) * ratio
    check_close(round(unscaled, 1), 11.,
                'printed-value consistency: unscaled Rabi energy / transverse gap',
                records, category='printed_value_consistency')

    thermal = []
    for temperature_nk in [6., 12.]:
        x = H * FZ / (KB * temperature_nk * 1e-9)
        b = math.exp(-x)
        # This is a canonical independent oscillator, not the full Bose-gas mode fraction.
        probabilities = [(1-b) * b**nu for nu in range(100)]
        check_close(math.fsum(probabilities), 1.,
                    f'canonical axial probability normalization T={temperature_nk}nK', records)
        check_close(math.fsum(probabilities[1:]), b,
                    f'canonical excited tail equals Boltzmann factor T={temperature_nk}nK', records)
        check_close(probabilities[1] / probabilities[0], b,
                    f'canonical first-level population ratio T={temperature_nk}nK', records)
        mean_nu = math.fsum(nu * p for nu, p in enumerate(probabilities))
        check_close(mean_nu, b / (1-b),
                    f'canonical mean excitation distinct from excited fraction T={temperature_nk}nK', records)
        thermal.append({'temperature_nK': temperature_nk, 'gap_over_kBT': x,
                        'canonical_excited_probability': b,
                        'canonical_excited_percent': 100*b,
                        'canonical_mean_nu': mean_nu})

    # Zhang et al., arXiv:2608.20311v1, p. 5: scattering lengths 31, -53, 220 a0.
    # A common transverse profile gives the same coupling ratios; its common prefactor is set to one.
    # Exact algebra at Z0 is tested, not a measured common transverse profile.
    guu, gud, gdd = 31., -53., 220.
    kappa = (guu + gdd - 2*gud) / 4
    z0 = (gdd - guu) / (4*kappa)
    gd = (guu*gdd - gud*gud) / (4*kappa)
    for density in [0.1, 1., 3.]:
        for dz in [0., -0.001, 0.001, 0.05]:
            z = z0 + dz
            nup, ndn = density*(1+z)/2, density*(1-z)/2
            uup, udn = guu*nup+gud*ndn, gud*nup+gdd*ndn
            check_absolute(uup-udn, 2*kappa*density*dz,
                           f'mean-field difference n={density}, deltaZ={dz}', records)
            if dz == 0.:
                check_absolute(uup, gd*density,
                               f'balanced up-spin common potential n={density}', records)
                check_absolute(udn, gd*density,
                               f'balanced down-spin common potential n={density}', records)

    profiles = []
    for width_up in [0.97, 1., 1.03, 1.3]:
        width_down = 1.
        def f0(z, width):
            return math.exp(-z*z/(2*width*width)) / (math.pi*width*width)**0.25
        def f2(z, width):
            return (2*z*z/(width*width)-1) / math.sqrt(2) * f0(z, width)
        end = 12*max(width_up, width_down)
        overlap0 = math.sqrt(2*width_up*width_down / (width_up**2+width_down**2))
        overlap2 = overlap0 * (width_up**2-width_down**2) / (
            math.sqrt(2)*(width_up**2+width_down**2))
        numeric0 = simpson(lambda z: f0(z,width_up)*f0(z,width_down), -end, end)
        numeric2 = simpson(lambda z: f0(z,width_up)*f2(z,width_down), -end, end)
        check_absolute(numeric0, overlap0, f'Gaussian ground-profile overlap ell_up={width_up}', records)
        check_absolute(numeric2, overlap2, f'Gaussian nu=2 overlap ell_up={width_up}', records)
        tail_weight = max(0., 1-overlap0**2)
        check_upper(overlap2**2, tail_weight,
                    f'nu=2 overlap lies within complementary weight ell_up={width_up}', records)
        if width_up == width_down:
            check_absolute(overlap2, 0., 'common-profile uniform-RF off-sector matrix element', records)
            check_absolute(tail_weight, 0., 'common-profile total complementary overlap is zero', records)
        profiles.append({'width_ratio': width_up/width_down,
                         'ground_profile_overlap': overlap0,
                         'second_mode_overlap': overlap2,
                         'complementary_overlap_weight': tail_weight})

    # Finite matching transformations only. lambda -> 0 is not claimed to be physical.
    base = scale_row(FZ)
    families = []
    for lam in [0.2, 0.25, 1/3, 0.5, 1., 1.04, 1.1]:
        row = scale_row(FZ/lam**2)
        new_spin_ratio = MU_S_OVER_H / (FZ/lam**2)
        check_close(row['oscillator_length_um']/base['oscillator_length_um'], lam,
                    f'matched-carrier transverse width lambda={lam}', records)
        check_close(new_spin_ratio, 0.9*lam*lam,
                    f'matched-carrier spin / gap lambda={lam}', records)
        check_close(row['kinetic_over_kB_nK']/base['kinetic_over_kB_nK'], lam**-2,
                    f'matched-carrier localization cost lambda={lam}', records)
        check_close(lam*row['g2D_relative_to_1kHz'], 1.,
                    f'matched simultaneous length and scattering scaling lambda={lam}', records)
        families.append({'lambda': lam, 'frequency_kHz': row['frequency_kHz'],
                         'mu_s_over_gap': new_spin_ratio,
                         'kinetic_resource_multiplier': lam**-2})
    lam_max = math.sqrt(0.1/0.9)
    check_close(lam_max, 1/3, 'lambda screening threshold for epsilon_star=0.1', records)

    # Exact two-sector constant Hamiltonian [[0,v],[v,delta]], with hbar=1.
    # Tests the Duhamel amplitude bound, including resonant and large-detuning cases.
    for coupling in [0., 0.02, 0.1, 1., 3.]:
        for detuning in [0., 0.5, 5.]:
            omega = math.hypot(coupling, detuning/2)
            for duration in [0.001, 0.1, 1., 3.]:
                amplitude = (0. if omega == 0. else
                             abs(coupling/omega * math.sin(omega*duration)))
                bound = min(1., abs(coupling)*duration)
                check_upper(amplitude, bound,
                            f'finite-pulse leakage bound v={coupling}, delta={detuning}, T={duration}', records)
    return {
        'readout_ratios': {'scaled_Omega_prime_over_gap': ratio,
                           'unscaled_Omega_over_gap': unscaled},
        'thermal_benchmark_assumptions':
            'T_z equals spin fit and independent canonical harmonic oscillator; not a measured Bose-gas fraction.',
        'conditional_axial_thermal_benchmarks': thermal,
        'mean_field_balance_test': {'interaction_ratios': [guu,gud,gdd],
                                    'exact_Z0_for_these_ratios': z0,
                                    'scope': 'Algebraic equality, not experimental profile certification.'},
        'toy_Gaussian_overlap_tests': profiles,
        'matched_carrier_scaling_cases': families,
        'pulse_bound_scope': 'Exactly solvable two-sector toy Hamiltonians; no actual experimental leakage fit.'}


def dispersion_checks(records: list[dict]) -> None:
    """Check Eq. (51) directly and Eq. (52) along four finite Josephson-limit rays.

    e = epsilon_k / mu_s_prime and q = hbar*Omega_prime / mu_s_prime.
    The expanded SI expression is compared with the dimensionless product.
    The joint zero is a polynomial check only, not a harmonic vacuum mode.
    Limit tests use squared-frequency error, not frequency error or a fitted spectrum.
    """
    mu = ALPHA * H * MU_S_OVER_H
    frequency_unit = mu / HBAR
    for e in [0., 0.02, 0.5, 2.]:
        for q in [0., 0.04, 1., 20.]:
            k2 = 2 * MASS * mu * e / HBAR**2
            omega_prime = q * frequency_unit
            expanded = (omega_prime * (omega_prime + 2 * frequency_unit)
                        + (mu + HBAR * omega_prime) / MASS * k2
                        + HBAR**2 / (4 * MASS**2) * k2**2)
            check_close(expanded / frequency_unit**2, (e+q) * (e+q+2),
                        f'Eq. (51) expanded versus factorized dispersion e={e}, q={q}',
                        records, category='dispersion_identity')
    for e0, q0 in [(1., 0.), (0., 1.), (1., 1.), (1., 2.)]:
        previous_error = math.inf
        for scale in [0.1, 0.01, 0.001]:
            e, q = scale*e0, scale*q0
            k2 = 2 * MASS * mu * e / HBAR**2
            omega_prime = q * frequency_unit
            exact = (e+q) * (e+q+2) * frequency_unit**2
            josephson = 2*mu*omega_prime/HBAR + mu/MASS*k2
            error = (exact-josephson) / exact
            label = f'e0={e0}, q0={q0}, scale={scale}'
            check_close(error, (e+q)/(2+e+q),
                        'Eq. (52) relative squared-frequency error ' + label,
                        records, category='josephson_limit')
            check_upper(error, min(previous_error, (e+q)/2),
                        'Eq. (52) Josephson convergence and error bound ' + label,
                        records, category='josephson_limit')
            previous_error = error


def main() -> None:
    records: list[dict] = []
    nominal = scale_row(FZ)
    omega = 2 * math.pi * FZ
    ell = nominal['oscillator_length_um'] * 1e-6
    sigma = nominal['rms_width_um'] * 1e-6
    kinetic = HBAR * omega / 4
    check_close(kinetic, HBAR**2 / (8 * MASS * sigma**2),
                'harmonic ground state saturates finite-energy width bound', records)
    check_close(round(ell / L, 4), 0.0154,
                'printed-value consistency: oscillator-length / box-side aspect ratio',
                records, category='printed_value_consistency')
    # Compare independent expressions for the Gaussian quartic overlap coupling.
    a = 5e-9                       # Analytic test value; not a source scattering length.
    g3 = 4 * math.pi * HBAR**2 * a / MASS
    g2 = g3 / (math.sqrt(2 * math.pi) * ell)
    g2_b = math.sqrt(8 * math.pi) * HBAR**2 * a / (MASS * ell)
    check_close(g2, g2_b, 'Gaussian transverse overlap coupling identity', records)
    # Arithmetic cancellation only; the scale_row-based family in revision_checks
    # supplies the nontrivial implementation checks for Proposition 14.1.
    for multiplier in [0.2, 0.5, 2., 5.]:
        check_close((multiplier*a)/(multiplier*ell), a/ell,
                    f'arithmetic sanity: common-factor cancellation lambda={multiplier}',
                    records, category='arithmetic_sanity')

    # Dimensionless a = epsilon/mu_s_prime + hbar*Omega_prime/mu_s_prime.
    # Covariance uses [Q,P]=i; no factor-of-two convention from external texts is imported.
    for a_mode in [0.025, 0.1, 0.5, 1., 3., 20.]:
        b_mode = a_mode + 2.
        w = math.sqrt(a_mode * b_mode)
        r = math.sqrt(b_mode / a_mode)
        check_close(r - 1/r, 2/w, f'covariance anisotropy a={a_mode}', records)
        for occupation in [0., 0.05, 0.5, 3.]:
            s = occupation + 0.5
            cqq, cpp = s*r, s/r
            check_close(cqq*cpp, s*s, f'equilibrium determinant a={a_mode}, N={occupation}', records)
            amp = cqq - cpp
            check_close(amp, 2*s/w, f'direct readout amplitude a={a_mode}, N={occupation}', records)
            check_close(w*amp, 2*occupation+1,
                        f'dimensionless collapse a={a_mode}, N={occupation}', records)
            for theta in [0.0, 0.13, 0.7, 1.3]:
                c, sn = math.cos(theta), math.sin(theta)
                rotated_q = cqq*c*c + cpp*sn*sn
                expected = (cqq+cpp)/2 + (cqq-cpp)*math.cos(2*theta)/2
                check_close(rotated_q, expected,
                            f'quadrature tomography a={a_mode}, N={occupation}, theta={theta}', records)
        # Deep-Rabi initial vacuum limit reproduces the source quench formula.
        check_close((r*r-1)/2, 1/a_mode, f'quench Rabi limit a={a_mode}', records)

    for ri in [1., 1.15, 2., 4.]:
        for rf in [1., 1.3, 3.]:
            for occupation in [0., 0.2, 2.]:
                s0 = occupation + 0.5
                for theta in [0., 0.13, 0.7, 1.3]:
                    c, sn = math.cos(theta), math.sin(theta)
                    q = s0*(ri*c*c + rf*rf/ri*sn*sn)
                    p = s0*(ri/(rf*rf)*sn*sn + c*c/ri)
                    qp = s0*(rf/ri-ri/rf)*c*sn
                    check_close(q*p-qp*qp, s0*s0,
                                f'quench determinant ri={ri}, rf={rf}, N={occupation}, theta={theta}', records)
    for x in [0.05, 0.2, 1., 3., 8.]:
        # A(w) = coth(w/(2T))/w with T=1, mu_s_prime/hbar=1.
        amplitude = lambda w: 1 / (w * math.tanh(w/2))
        eps = 1e-5
        beta_fd = -(math.log(amplitude(x*math.exp(eps))) -
                    math.log(amplitude(x*math.exp(-eps)))) / (2*eps)
        beta = 1 + x/math.sinh(x)
        check_close(beta_fd, beta, f'local spectral slope x={x}', records, 2e-8)
    for q in [0.5, 1., 2., 4.]:
        row = scale_row(q*FZ)
        check_close(row['oscillator_length_um']/nominal['oscillator_length_um'],
                    q**-0.5, f'width confinement scaling q={q}', records)
        check_close(row['kinetic_over_kB_nK']/nominal['kinetic_over_kB_nK'],
                    q, f'kinetic confinement scaling q={q}', records)
    additional = revision_checks(records)
    dispersion_checks(records)
    payload = {
        'revision_diagnostics': additional,
        'status': 'nominal analytic calculation; no new experimental data or fit',
        'source': 'Zhang et al., arXiv:2608.20311v1, Supplementary Materials',
        'mass_model': '39 times deliberately rounded u = 1.66054e-27 kg',
        'source_inputs': {'fz_hz_approx': FZ, 'box_side_m_approx': L,
                          'mu_s_over_h_Hz_approx': MU_S_OVER_H,
                          'mu_d_over_h_Hz_approx': MU_D_OVER_H, 'alpha_approx': ALPHA},
        'derived_nominal': nominal,
        'derived_ratios': {'ell_over_L': ell/L, 'sigma_over_L': sigma/L,
                           'mu_d_over_gap': MU_D_OVER_H/FZ,
                           'mu_s_over_gap': MU_S_OVER_H/FZ,
                           'mu_s_prime_over_gap': ALPHA*MU_S_OVER_H/FZ},
        'illustrative_only': {'variance_relative_SE_M70': math.sqrt(2/69),
                              'variance_relative_SE_M120': math.sqrt(2/119),
                              'finite_readout_r_at_zero_epsilon': math.sqrt(1.1)},
    }
    (OUT/'nominal_scales.json').write_text(json.dumps(payload, indent=2)+'\n')
    family = [scale_row(f) for f in [500., 1000., 2000., 4000.]]
    with (OUT/'confinement_family.csv').open('w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(family[0]))
        writer.writeheader(); writer.writerows(family)
    categories = dict(sorted(Counter(r['category'] for r in records).items()))
    auxiliary = sum(categories.get(key, 0) for key in
                    ['arithmetic_sanity', 'printed_value_consistency'])
    report = {'all_passed': all(r['passed'] for r in records), 'checks': len(records),
              'analytic_or_model_checks': len(records)-auxiliary,
              'auxiliary_checks': auxiliary, 'counts_by_category': categories,
              'scope': ('Finite-case analytic checks and illustrative model benchmarks; '
                        'arithmetic sanity and printed-value consistency counted separately; '
                        'not proofs or experimental validation.'),
              'max_relative_error': max(r['relative_error'] for r in records),
              'details': records}
    (OUT/'analytic_checks.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'nominal': nominal, 'checks_passed': len(records),
                      'analytic_or_model_checks': len(records)-auxiliary,
                      'auxiliary_checks': auxiliary, 'counts_by_category': categories}, indent=2))

if __name__ == '__main__':
    main()
