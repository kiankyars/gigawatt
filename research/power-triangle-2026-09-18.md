# Chapter 6: the power triangle

After author review, `#power-triangle` follows `#power-factor-explained`, so the numerical comparison introduces its quantities first. The order is beer analogy → numerical comparison → power triangle. Chapter 6 has 30 slides; the triangle is slide 25.

## Teaching purpose

The beer picture is a memory cue, but its stacked heights could imply that real and reactive power add arithmetically. The native SVG instead uses a geometrically accurate right triangle: 900 kW horizontally, 675 kvar vertically and 1,125 kVA along the hypotenuse. The same load appears in the preceding transformer example. The visible equations are `S² = P² + Q²` and `PF = P / S = 0.80`.

## Speaker-note insertion

Real power is the average energy transfer, including useful output and losses. Reactive power describes energy exchanged with electric or magnetic fields; the 675 kvar is not 675 kW of waste heat. Apparent power determines the voltage-and-current burden on equipment. The real and reactive components are perpendicular, giving 1,125 kVA rather than their arithmetic sum of 1,575. Power factor is 900/1,125 = 0.80.

This triangle assumes sinusoidal voltage and current. Its angle is the phase displacement between them. Harmonic distortion can also lower true power factor, so a measured PF of 0.80 does not by itself establish 675 kvar. The preceding slide introduces this illustrative load and the 1,000 kVA transformer.

## Sources checked

- [Schneider Electric: definition of reactive power](https://www.electrical-installation.org/enwiki/Definition_of_reactive_power): perpendicular components, sinusoidal assumption, `S² = P² + Q²`, and `P/S = cos φ`. Linked below the new diagram.
- [Schneider Electric: definition of power factor](https://www.electrical-installation.org/enwiki/Definition_of_Power_Factor): `PF = P/S`; apparent power is the basis for equipment rating.
- [Schneider Electric: harmonic distortion and power factor](https://www.electrical-installation.org/enwiki/Harmonic_distortion_indicators_-_Power_factor): true power factor includes waveform distortion and must be distinguished from displacement power factor.

## Validation

- `node --test tests/distribution.test.mjs tests/distribution-model.test.mjs`: 12 passed.
- Playwright screenshots at 1280×720 and 390×844, light and dark: no runtime errors, horizontal overflow, clipped SVG labels or desktop footer overlap. Previous/next navigation connects beer → transformer comparison → triangle.
- Temporary QA output: `/tmp/gigawatt-power-triangle/`; raw-source server used port 8891. No staged-site files changed.
