<!-- gigawatt-research:managed:start -->
# EFB703CFC3D — Schneider Electric — PM2200 total power calculation for accuracy verification

- **Url:** [Original source](https://productinfo.se.com/pm2200/5afc2b5546e0fb00011e5e9d/PM2200%20series%20User%20Manual/English/BM_PM2200seriesUserManual_0000074170.ditamap.xml/%24/C_VerifyingAccuracy_PowerTotCalcuation_0000034437)
- **Publisher:** Schneider Electric
- **Kind:** technical_documentation
- **Review status:** page_reviewed
- **Reviewed on:** 2026-09-08
- **Domains:** [D01](../../course/DOMAIN_MAP.md#d01), [D04](../../course/DOMAIN_MAP.md#d04), [D06](../../course/DOMAIN_MAP.md#d06)
- **Use:** The selected PM2200 manual page gives balanced three-phase real power as 3 × line-to-neutral voltage × current × power factor. The course uses the equivalent line-to-line form with RMS voltage and current.
- **Caution:** Reviewed only the linked calculation page, not the whole PM2200 manual. Its balanced three-phase formula supports the electrical relationship, not data-center topology, cable sizing, converter efficiency or any claimed measured savings. Numerical course examples are original calculations.
- **Discovered via:** 480 V AC versus 800 V DC teaching sample correction, 2026-09-08.

Catalog metadata fingerprint: 25e13b353210e6882c61eab1377efaaa82b42dfe5a9d50e1c54631460fcee4ad
<!-- gigawatt-research:managed:end -->

## Claim-level notes

Reviewed the section “Total power calculation for accuracy verification testing”
on 2026-09-08. The page gives the balanced wye relationship using phase-to-neutral
voltage, equal phase currents and a common power factor. The teaching example
uses the equivalent line-to-line RMS relationship.

## Teaching use

For the original 100 kW example, 480 V line-to-line RMS at PF 1 requires
120.281 A per AC line; 800 V across a DC pair requires 125 A per conductor.
Three AC conductors and two DC conductors with equal effective resistance yield
DC total conductor heat equal to 72% of the AC heat. This is an original
calculation, not a measured product saving. Equal conductor count, current,
copper volume and total loss are different comparison choices.

The final sample includes assumed converter losses at specified positions and
recalculates feeder currents from downstream demand. This source establishes
neither those assumed losses nor a whole-architecture efficiency advantage.
