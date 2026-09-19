# Chapter 8: Clemente power conversion and VRM switching

Added 2026-09-18 after the user approved the placement proposal. Chapter 8 grows from 17 to 19 slides; existing slide IDs and aliases remain intact.

## New slide 10: Meta's GB300 power board

`#clemente-power-board` follows `#board-rails` (the direct-versus-intermediate architectural comparison).

The native diagram traces **nominal 51 V rack supply → NVIDIA-designed power distribution board → 12 V → local regulators → processor rails**. It names Meta's Clemente implementation rather than presenting the intermediate stage as mandatory for all GB300 systems.

Primary source: [Meta / Open Compute Project, Clemente Compute Tray Specification](https://www.opencompute.org/documents/clemente-compute-tray-ocp-specification-final-pdf), §§7.1, 7.2 and 8.1. [Version 1 URL](https://www.opencompute.org/documents/clemente-compute-tray-ocp-specification-v1-pdf).

Verified from the official indexed specification on 2026-09-18:

- Page 10 identifies the power distribution board as NVIDIA designed.
- Page 12 says the board converts ORv3 rack power to 12 V.
- Page 22 gives nominal 51 V, normal operating input 46–52 V.
- Exact processor-rail voltages and B300 regulator/phase counts are not established by these sections.

The source alternates nominal 48/50/51 V descriptions; the slide uses the explicit input specification's 51 V. It does not invent a distinct conversion between those values. Internal module regulation is a functional boundary, not a reproduction of an unpublished component schematic.

**Figure retrieval limitation:** both official PDF download URLs returned HTTP 403 locally, and web open/screenshot timed out. The official search index exposed the relevant specification text. The parent approved an exact native schematic as the fallback. No unrelated manufacturer's board photo is substituted or labeled Clemente. The slide's source attribution links to the official document.

### Suggested speaker notes

“This is a real version of the intermediate-rail architecture: Meta's Clemente GB300 compute tray. The rack provides nominal 51 volts. The tray's NVIDIA-designed power board converts that to 12 volts, then local regulators provide the processor rails. The first conversion is shared within the tray; the final voltage regulation happens close to the load.”

Do not call the last step a verified 1 V B300 specification. Similarly, a claimed phase count needs a named rail, controller and board boundary. One multiphase VRM is not many complete independent regulators.

## New slide 12: how the phases switch

`#vrm-switching` follows the existing `#multiphase` current-sharing comparison. `#vrm-phase-counts` remains immediately after it.

Primary source: [Texas Instruments, Benefits of a multiphase buck converter](https://www.ti.com/lit/an/slyt449/slyt449.pdf), Figures 1, 2 and 4, 1Q2012. Downloaded and inspected on 2026-09-18.

The user-supplied TIFF labels triangular traces “VRM Phase Voltages.” It is not embedded as-is. The replacement native SVG retains the intended lesson while distinguishing **rectangular switch-node voltages** from **triangular inductor currents**. A two-branch circuit shows a common rail, load and output capacitor. This is a fresh exact chart, not an AI edit or a claim about B300 hardware.

The worked ideal example has 12 V input, 3 V output, 25% duty cycle and two phases offset by half a period. Each inductor carries 20 A average with 6 A peak-to-peak ripple; their sum has 40 A average and 4 A peak-to-peak ripple. The two current panels use the same vertical amperes-per-pixel scale. The load sees the output rail after capacitor filtering; the summed inductor current is not mislabeled load current or a perfectly ripple-free output.

### Suggested speaker notes

“The switches make pulses of voltage. The inductors turn those pulses into currents that rise and fall. This second phase starts half a switching period later. Both currents join at the same rail, so one partly offsets the other's ripple. The capacitor handles the remaining shortfall and surplus while feedback regulates the rail voltage. These are phases inside one regulator, not the facility's AC phases.”

## Validation

- `node --test tests/rack-energy.test.mjs tests/rack-power.test.mjs`: 20 tests pass.
- Numeric tests check duty cycle, phase offset, mean phase and total current, and both ripple magnitudes.
- Both new hashes resolve in the existing controller; no deleted scene or alias.
- Playwright captures: 1440×900 and 390×844, light and dark. No page errors or horizontal overflow in 8 rendered states. Mobile diagrams stack with bottom padding for the fixed footer; vertical scrolling is expected.
- New figures are HTML/SVG in `course/prototypes/rack-energy-vrm.js`, with no new bitmap asset or source-image claim.

## Author-supplied Clemente figure — September 18 follow-up

The author supplied a replacement illustration. The slide now displays only that image and the existing OCP specification citation. Its embedded title replaces the duplicate HTML heading. TIFF-to-PNG conversion preserves the content, and CSS contains the complete frame. The illustration shows the verified 51 V → 12 V functional path; its rendered hardware geometry is conceptual. Provenance and source/output hashes are in `clemente-gb300-user.provenance.json`.
