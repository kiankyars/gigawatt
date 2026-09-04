# Engineering reference

Primary sources checked on **2026-09-04**. Numerical exercises describe a generic teaching scenario. They do not establish any named campus's installed equipment, available capacity, measured demand, coolant conditions, or compute output.

## Quantities and conversions

| Mechanism | Equation and assumptions | Primary reference |
| --- | --- | --- |
| Power and energy | `E [MWh] = P [MW] × t [h]` for constant power; otherwise integrate power over time. A service rating is a capacity, not a measurement of demand. | [EIA, measuring electricity](https://www.eia.gov/energyexplained/electricity/measuring-electricity.php) |
| Balanced three-phase AC | `I [A] = P [MW] × 1000 / (√3 × V_LL [kV] × PF)`. Voltage is line-to-line RMS; PF is the real/apparent power ratio. The visual's sinusoidal, balanced example uses PF = 1. | [Schneider Electric, apparent power](https://www.electrical-installation.org/enwiki/Installed_apparent_power_%28kVA%29) |
| Resistive conductor heating | At fixed transferred real power, PF, and conductor resistance, `I ∝ 1/V`, and conductor loss `∝ I²R ∝ 1/V²`. Three equal phase conductors dissipate `3I²R`, with R the resistance per phase. This isolates resistive line losses; it does not calculate transformer losses, grid efficiency, or a feasible line design. | [OpenStax, transformers](https://openstax.org/books/university-physics-volume-2/pages/15-6-transformers) |
| DC distribution | `I [A] = P [kW] × 1000 / V [V]`, with power and voltage at the same DC boundary. AC input power requires conversion losses before using it as DC output power. | [Infineon, rack and processor power](https://www.infineon.com/applications/ai-data-center/data-center-power-solutions/server-rack-power-management) |
| Battery duration | `t [min] = 60 × usable stored E [MWh] × discharge efficiency / load P [MW]`. A constant-load energy estimate also requires adequate UPS/inverter power capacity. Usable energy, aging, temperature, discharge rate, and reserve policy determine actual runtime. | [Vertiv, UPS and BESS architectural roles](https://www.vertiv.com/en-us/insights/articles/white-papers/bess-and-ups-roles-in-large-data-center-power-architecture/) |
| Single-phase liquid heat transport | `Q̇ [kW] = ṁ [kg/s] × cp [kJ/(kg·K)] × ΔT [K]`. Use water `cp ≈ 4.18` as an explicit approximation. No phase change; steady operation; negligible heat leakage. Different coolants have different properties. | [DOE, thermodynamics and heat transfer handbook](https://www.energy.gov/sites/default/files/2026-04/DOE-HDBK-1012-92_VOL1.pdf) |

Worked checks: 100 MW at 13.8 kV gives 4,184 A; at 138 kV it gives 418 A, with one hundredth of the resistive conductor loss under the stated comparison. A hypothetical 120 kW **DC** bus at 50 V carries 2,400 A. A hypothetical 800 W processor rail at 0.8 V carries 1,000 A; this is not a GPU product specification. A 100 kW water-cooled heat load with a 10 K rise needs approximately 2.39 kg/s, or 144 L/min assuming 1 kg/L water density. A 5 MWh usable battery supplying 100 MW provides 3 minutes ideally or 2.7 minutes at 90% discharge efficiency.

## Boundaries that visuals must preserve

- **Facility versus IT:** [ISO/IEC 30134-2:2026](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso-iec%3A30134%3A-2%3Aed-2%3Av1%3Aen) defines PUE using total facility and IT energies over the same continuous 12 months. It separately defines designed and interim PUE. The interactive MW budget uses an **assumed steady facility-to-IT power ratio**, not an annual PUE silently applied to instantaneous load. At a ratio of 1.25, overhead is 25% of IT power and 20% of total facility power. IT includes networking and storage; dedicated compute-rack budgets must reserve their other loads first. PUE does not measure useful compute efficiency.
- **Electrical input becomes heat:** The [DOE/PNNL data-center model report](https://www.energy.gov/sites/default/files/2026-01/Data_Center_EMT_Models.pdf) describes most IT electricity becoming heat. For the steady teaching balance use approximately `Q̇_IT = P_IT`. Do not split watts into competing "useful computation" and "heat" streams: computation occurs while the electrical energy is ultimately dissipated. Generation losses occur outside the data-center boundary.
- **Liquid and air are parallel paths:** [NVIDIA's DGX GB rack guide](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html), updated March 3, 2026, documents 18 compute trays with 4 GPUs and 2 CPUs each, nominal 50–51 V DC power shelves, and approximately 120 kW rack consumption. CPUs/GPUs use liquid cold plates while other components retain air cooling. The 120 kW figure is a product reference, not a universal rack rating or measured demand. Dividing by 72 produces an allocation of whole-rack power per GPU, **not GPU TDP**. Rack count alone cannot establish throughput.
- **CDU heat exchange:** The [OCP liquid-to-liquid CDU methodology](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf) describes a heat exchanger separating technology and facility fluids. Draw closed supply/return loops; heat crosses the boundary while fluids stay separate. Available performance depends on both flow rates, temperatures, pressure, and coolant properties. `ΔT` around one loop is distinct from the heat exchanger's approach temperature. Flow arithmetic alone does not size a pump or CDU.
- **Heat rejection:** [DOE cooling guidance](https://www.energy.gov/cmei/femp/cooling-water-efficiency-opportunities-federal-data-centers) explains heat transport through facility loops, outdoor rejection, and added compressor heat. For a steady chiller balance, `Q̇_condenser ≈ Q̇_evaporator + W_compressor`. Facility pumps/fans add further heat within their respective boundaries. A dry cooler, an air-cooled chiller, and an evaporative tower are different systems. Liquid cooling alone establishes neither water consumption nor a zero-water campus.
- **Redundancy:** [Schneider's two-cord explanation](https://blog.se.com/datacenter/architecture/2014/08/06/two-cords-guarantee-power-redundancy-device/) requires compatible loads, distinct feeds, and sufficient surviving-path capacity. [Uptime's current criteria](https://uptimeinstitute.com/tier-certification) distinguish Tier III planned maintainability from Tier IV fault tolerance. A two-path diagram is not certification or a continuity guarantee.

## Calculation API

`course/web/math.js` exports pure functions. Power inputs may be zero; denominators must be positive; efficiencies/PF must be in `(0, 1]`; the assumed PUE ratio must be at least 1. All supplied values must be finite except the optional unbounded electrical limit. Rack counts must be nonnegative safe integers. Invalid inputs throw `RangeError`.

`capacityBudget(facilityMW, pue, coolingMW, rackKW, rackSlots, networkRacks, electricalMW = Infinity)` compares all constraints in **whole compute racks**:

- `facilityMW / pue` is IT power available under the assumed steady ratio.
- `coolingMW` is available heat removal for the represented IT, excluding cooling plant electrical demand.
- `rackKW` is an assumed full-rack operating/design allocation, not per-GPU TDP.
- `rackSlots` counts physical compute-rack positions; `networkRacks` counts racks the assumed network can support, not network-equipment racks.
- Optional `electricalMW` is usable downstream electrical capacity at the IT boundary.

Each MW limit is divided by rack power and rounded down. The smallest rack limit sets `supportedRacks`; `binding` lists every tied constraint. Returned `supportedITMW` and `facilityDrawMW` are steady scenario values. A fixed ratio simplifies real overhead behavior, which varies with load and conditions.

Canonical check: facility service 100 MW / assumed ratio 1.25 gives 80 MW IT. Downstream electrical capacity 70 MW, IT heat-removal capacity 60 MW, 900 rack positions, and a network supporting 900 compute racks at 100 kW/rack produce **600 supported racks**, **60 MW IT**, and **75 MW scenario facility draw**. This feasibility ceiling assumes ancillary IT loads and required spare capacity are already reserved in the entered budgets. It does not establish installed, commissioned, active, or productive compute.

The rendered experiments use these boundaries explicitly: the battery slider specifies usable energy at the UPS output (so no further efficiency factor is applied); line thickness in the DC-current comparison is qualitative; blue air and liquid supply arrows point toward the rack. The air-handler fans circulate air while its coil transfers heat onward.

Run numerical and invalid-input checks with `node --test tests/math.test.mjs`.
