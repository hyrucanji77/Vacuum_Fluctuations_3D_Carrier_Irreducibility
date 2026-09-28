#!/usr/bin/env python3
"""Reproduce nominal scales and analytic checks in the accompanying manuscript.

No experimental data are simulated or fitted. Inputs come from Zhang et al.,
arXiv:2608.20311v1, Supplementary Materials (experimental system), except
h and k_B (SI definitions) and the explicitly rounded nominal isotope mass.
Python 3.10+; standard library only. Outputs are written beside this script.
"""
from __future__ import annotations
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
                tolerance: float = 2e-11) -> None:
    error = abs(a - b) / max(abs(a), abs(b), 1e-30)
    passed = math.isfinite(a) and math.isfinite(b) and error < tolerance
    records.append({'check': name, 'actual': a, 'expected': b,
                    'relative_error': error, 'tolerance': tolerance, 'passed': passed})
    if not passed:
        raise ArithmeticError(f'{name}: {a!r} != {b!r}; relative error {error:g}')


def main() -> None:
    records: list[dict] = []
    nominal = scale_row(FZ)
    omega = 2 * math.pi * FZ
    ell = nominal['oscillator_length_um'] * 1e-6
    sigma = nominal['rms_width_um'] * 1e-6
    kinetic = HBAR * omega / 4
    check_close(kinetic, HBAR**2 / (8 * MASS * sigma**2),
                'harmonic ground state saturates finite-energy width bound', records)
    check_close(round(ell / L, 4), 0.0154, 'manuscript rounded aspect ratio', records)
    # Compare independent expressions for the Gaussian quartic overlap coupling.
    a = 5e-9                       # Analytic test value; not a source scattering length.
    g3 = 4 * math.pi * HBAR**2 * a / MASS
    g2 = g3 / (math.sqrt(2 * math.pi) * ell)
    g2_b = math.sqrt(8 * math.pi) * HBAR**2 * a / (MASS * ell)
    check_close(g2, g2_b, 'Gaussian transverse overlap coupling identity', records)
    for multiplier in [0.2, 0.5, 2., 5.]:
        check_close((multiplier*a)/(multiplier*ell), a/ell,
                    f'planar coupling non-identifiability lambda={multiplier}', records)

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
    payload = {
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
    report = {'all_passed': all(r['passed'] for r in records), 'checks': len(records),
              'scope': 'Numerical checks of named analytic identities; not experimental validation.',
              'max_relative_error': max(r['relative_error'] for r in records),
              'details': records}
    (OUT/'analytic_checks.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'nominal': nominal, 'checks_passed': len(records)}, indent=2))

if __name__ == '__main__':
    main()
