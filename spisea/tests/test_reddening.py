import numpy as np
from spisea import reddening, synthetic
import pylab as py
import pdb


def test_RedLawBrokenPowerLaw(plots=False):
    #===============================#
    # Test 1: 2-segment law
    #===============================#
    alpha1 = 2.23
    alpha2 = 3.0
    lambda_limits = [2.16, 1.63, 1.27]
    alpha_vals = [alpha1, alpha2]
    K_wave = 2.14

    red_law = reddening.RedLawBrokenPowerLaw(lambda_limits, alpha_vals, K_wave)

    # Calculate what the redlaw *should* be across wavelength range,
    # by-hand
    wave_test = np.arange(1.27, 2.15+0.001, 0.01)
    law_test = np.ones(len(wave_test)) * np.nan

    # 2.14 - 1.63
    idx = np.where( (wave_test > 1.63) & (wave_test <= 2.17))
    coeff = 1
    law_test[idx] = coeff * wave_test[idx] ** (-1*alpha1)

    # 1.63 - 1.27
    idx = np.where( (wave_test >= 1.27) & (wave_test <= 1.63))
    coeff  = (1.63 ** (-1*alpha1)) / (1.63 ** (-1*alpha2))
    law_test[idx] = coeff * wave_test[idx] ** (-1*alpha2)
    assert np.sum(np.isnan(law_test)) == 0

    # Put in terms of A_lambda / A_Ks, like the reddening object
    idx_K = np.where(abs(wave_test - K_wave) == min(abs(wave_test - K_wave)))
    law_test /= law_test[idx_K]

    # Compare law_test and the output from the redlaw object
    law_output = red_law.broken_powerlaw(wave_test, 1)
    
    assert len(law_test) == len(law_output)
    assert np.sum(np.isnan(law_output)) == 0

    # Calculate the difference between test calc and code output.
    # Make sure they agree within tolerance
    diff = law_output - law_test
    assert np.all(diff < 10**-4)

    # Let's also make sure the slope of the extinction law
    # in log-log space matches what it should be
    log_wave = np.log10(wave_test)
    log_output = np.log10(law_output)

    idx1 = np.where(abs(wave_test-1.28) == np.min(abs(wave_test-1.28)))
    idx2 = np.where(abs(wave_test-1.53) == np.min(abs(wave_test-1.53)))
    slope = (log_output[idx1] - log_output[idx2]) / (log_wave[idx1] - log_wave[idx2])
    assert abs(slope - (-1.0 * alpha2)) < 10**-4

    idx1 = np.where(abs(wave_test-1.7) == np.min(abs(wave_test-1.7)))
    idx2 = np.where(abs(wave_test-2.1) == np.min(abs(wave_test-2.1)))
    slope = (log_output[idx1] - log_output[idx2]) / (log_wave[idx1] - log_wave[idx2])
    assert abs(slope - (-1.0 * alpha1)) < 10**-4
    
    # If desired (debug only), make plot to see what law looks like
    if plots:
        # Test plot: these should match nearly exactly
        py.figure()
        py.loglog(wave_test, law_test, 'k.', ms=13, label='Test')
        py.loglog(wave_test, law_output, 'r.', ms=8, label='Code')
        py.loglog(red_law.wave*10**-4, red_law.obscuration, 'r-')
        py.axvline(1.63, linestyle='--', color='blue')
        py.xlabel('Wavelength')
        py.ylabel('A_lambda / A_Ks')
        py.legend()
        py.gca().invert_xaxis()
        py.title('2-segment Extlaw: should match')

    #===============================#
    # Test 1: 4-segment law
    #===============================#
    alpha1 = 2.23
    alpha2 = 3.0
    alpha3 = 2.5
    alpha4 = 3.7
    lambda_limits = [2.16, 1.63, 1.27, 0.8, 0.4]
    alpha_vals = [alpha1, alpha2, alpha3, alpha4]
    K_wave = 2.14

    red_law = reddening.RedLawBrokenPowerLaw(lambda_limits, alpha_vals, K_wave)

    # Calculate what the redlaw *should* be across wavelength range,
    # by-hand
    wave_test = np.arange(0.4, 2.15+0.001, 0.01)
    law_test = np.ones(len(wave_test)) * np.nan

    # 2.14 - 1.63
    idx = np.where( (wave_test >= 1.63) & (wave_test < 2.17))
    coeff = 1
    law_test[idx] = coeff * wave_test[idx] ** (-1*alpha1)

    # 1.63 - 1.27
    idx = np.where( (wave_test >= 1.27) & (wave_test < 1.63))
    coeff  = (1.63 ** (-1*alpha1)) / (1.63 ** (-1*alpha2))
    law_test[idx] = coeff * wave_test[idx] ** (-1*alpha2)
    
    # 1.27 - 0.8
    idx = np.where( (wave_test >= 0.8) & (wave_test < 1.27))
    coeff1 = (1.63 ** (-1*alpha1)) / (1.63 ** (-1*alpha2))
    coeff2 = (1.27 ** (-1*alpha2)) / (1.27 ** (-1*alpha3))
    coeff_f = coeff1 * coeff2
    law_test[idx] = coeff_f * wave_test[idx] ** (-1*alpha3)

    # 0.8 - 0.4
    idx = np.where( (wave_test >= 0.4) & (wave_test < 0.8))
    coeff1 = (1.63 ** (-1*alpha1)) / (1.63 ** (-1*alpha2))
    coeff2 = (1.27 ** (-1*alpha2)) / (1.27 ** (-1*alpha3))
    coeff3 = (0.8 ** (-1*alpha3)) / (0.8 ** (-1*alpha4))
    coeff_f = coeff1 * coeff2 * coeff3
    law_test[idx] = coeff_f * wave_test[idx] ** (-1*alpha4)
    
    assert np.sum(np.isnan(law_test)) == 0

    # Put in terms of A_lambda / A_Ks, like the reddening object
    idx_K = np.where(abs(wave_test - K_wave) == min(abs(wave_test - K_wave)))
    law_test /= law_test[idx_K]

    # Compare law_test and the output from the redlaw object
    law_output = red_law.broken_powerlaw(wave_test, 1)
    
    assert len(law_test) == len(law_output)
    assert np.sum(np.isnan(law_output)) == 0

    # Calculate the difference between test calc and code output.
    # Make sure they agree within tolerance
    diff = law_output - law_test
    assert np.all(diff < 10**-4)

    # Let's also make sure the slope of the extinction law
    # in log-log space matches what it should be
    log_wave = np.log10(wave_test)
    log_output = np.log10(law_output)

    idx1 = np.where(abs(wave_test-1.28) == np.min(abs(wave_test-1.28)))
    idx2 = np.where(abs(wave_test-1.53) == np.min(abs(wave_test-1.53)))
    slope = (log_output[idx1] - log_output[idx2]) / (log_wave[idx1] - log_wave[idx2])
    assert abs(slope - (-1.0 * alpha2)) < 10**-4

    idx1 = np.where(abs(wave_test-1.7) == np.min(abs(wave_test-1.7)))
    idx2 = np.where(abs(wave_test-2.1) == np.min(abs(wave_test-2.1)))
    slope = (log_output[idx1] - log_output[idx2]) / (log_wave[idx1] - log_wave[idx2])
    assert abs(slope - (-1.0 * alpha1)) < 10**-4

    idx1 = np.where(abs(wave_test-0.9) == np.min(abs(wave_test-0.9)))
    idx2 = np.where(abs(wave_test-1.2) == np.min(abs(wave_test-1.2)))
    slope = (log_output[idx1] - log_output[idx2]) / (log_wave[idx1] - log_wave[idx2])
    assert abs(slope - (-1.0 * alpha3)) < 10**-4

    idx1 = np.where(abs(wave_test-0.45) == np.min(abs(wave_test-0.45)))
    idx2 = np.where(abs(wave_test-0.7) == np.min(abs(wave_test-0.7)))
    slope = (log_output[idx1] - log_output[idx2]) / (log_wave[idx1] - log_wave[idx2])
    assert abs(slope - (-1.0 * alpha4)) < 10**-4
    
    # If desired (debug only), make plot to see what law looks like
    if plots:
        # Test plot: these should match nearly exactly
        py.figure()
        py.loglog(wave_test, law_test, 'k.', ms=13, label='Test')
        py.loglog(wave_test, law_output, 'r.', ms=8, label='Code')
        py.loglog(red_law.wave*10**-4, red_law.obscuration, 'r-')
        py.axvline(1.63, linestyle='--', color='blue')
        py.axvline(1.27, linestyle='--', color='blue')
        py.axvline(0.8, linestyle='--', color='blue')
        py.xlabel('Wavelength')
        py.ylabel('A_lambda / A_Ks')
        py.legend()
        py.gca().invert_xaxis()
        py.title('4-segment Extlaw: should match')

    return

