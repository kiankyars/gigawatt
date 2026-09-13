# Follow the watts through the rack

Generated reading view. Edit [`course/expansion/racks-compute-heat.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/racks-compute-heat.json), lesson `d06-conversion-ledger`, then run `uv run gigawatt-expand`.

**8. Rack power and the 800 V DC transition · Authored draft**

Build an electrical ledger from the rack inlet to useful device rails, with separate conversion losses and auxiliary loads.

**Driving question:** Why is the sum of processor power ratings not the power entering the rack?

## Draw boundaries before calculating

A rack is a distribution system containing several kinds of load. Accelerators perform arithmetic, host processors manage execution, memory holds working state, switches move information, and management hardware keeps the system observable. Fans and pumps may also draw electricity inside the chosen rack boundary. Begin with the measured inlet, then draw arrows to each converter and load. Label an arrow with both voltage and power. Voltage describes the electrical interface; power describes the rate of energy transfer. Two arrows can carry the same power at very different currents.

A processor rating is attached to a particular device and operating convention. It does not automatically include the memory, conversion losses or external switches supporting that processor. Nor does a collection of ratings establish simultaneous measured demand. For a first ledger, declare a steady operating point and give every branch an assumed load. Later, compare that ledger with telemetry at matching timestamps. If one meter averages a minute while another samples a burst, apparent missing watts may be a measurement-boundary problem.

## Follow one rack from its AC feed to the rear DC busbar

A busway tap or remote power panel supplies the rack through its qualified power cables, often called whips. A power shelf is an assembly holding multiple power supply units (PSUs), a connection to the rack bus and monitoring/control hardware. A PSU converts AC input into regulated DC output. The rack’s vertical busbar carries that output along the cabinet so trays can connect to a shared DC distribution system. The busbar is a conductor assembly, not a converter. Redundancy belongs to the actual sources, modules and paths, not to the name “power shelf.”

Use the named NVIDIA hardware accurately: the DGX GB rack guide describes a nominal 50–51 V DC rack bus and supplies an annotated DGX GB300 rear view identifying the power busbar. The enterprise GB300 NVL72 reference lists eight 33 kW shelves, each with six 5.5 kW PSUs, and an up-to-142-kW full-rack requirement. These are different quantities and documentation boundaries; adding module labels does not establish continuously usable redundant rack capacity. The local 50–51 V bus is distinct from the proposed 800 V hall-distribution interface. OCP ORv3, a particular OEM NVL72 rack and NVIDIA’s DGX implementation must not be treated as identical specifications.

## A three-phase shelf does not make every PSU a three-phase converter

Specify the electrical plane before labeling a voltage. In a balanced 480/277 V wye supply, 480 V is the RMS voltage between live phases and 480/√3 ≈ 277 V is the RMS voltage from a phase to neutral. Neither live phase is protective earth. A shelf can distribute the phases across single-phase PSU modules; its three-phase inlet does not imply that each module rectifies all three phases at 480 V.

Advanced Energy’s original ORv3 example makes the distinction concrete: its 3 kW PSU has a nominal 200–277 V single-phase AC input and a 50 V DC output, and multiple modules share a shelf. That product is an example of the interface distinction, not a claim about the precise wiring inside every GB300 shelf. A qualified 480/277 V path may omit an intermediate 480-to-208-V transformer used in another architecture, but the saved conversion stage does not establish a universal efficiency gain. Compare actual equipment loss at the same load and redundancy state.

## The board creates several rails before power reaches the die

After the rack bus, the tray’s qualified connector, protection and distribution carry power to its boards. An intermediate bus converter (IBC) can lower the rack voltage before point-of-load regulators create the rails required by the GPU, CPU, memory and other circuits. Texas Instruments’ TIDA-050095 is a concrete 48-to-12-V, 2 kW bus-converter reference design. Its transformer-less buck topology also demonstrates that a DC/DC converter need not contain a transformer. Other architectures use other intermediate voltages or conversion arrangements; do not infer that a GPU always receives 54 V directly at a final buck stage.

A voltage regulator module (VRM) controls a local rail near its load. “VRM” names the regulating function and associated power stages; it need not be one removable module. Input and output voltage, current capability, transients and sequencing are specific to the platform. There is no universal 12 V, 5 V or 3.3 V branch inventory for every AI tray. The teaching path 50 V rack bus → intermediate conversion → point-of-load VRM → die describes the functional order; an illustrative 48 V → 12 V → 1 V chain is labeled separately from the unpublished GB300 board schematic.

At an idealized 1 kW core rail and 1 V, I = P/V = 1,000 A. At 50 V the same ideal power is 20 A before conversion losses. This is why the final high-current route is short: even a hypothetical 100 microohm loop drops 0.1 V and dissipates 100 W at 1,000 A. Reducing that loop to 10 microohms reduces those numbers to 0.01 V and 10 W. These values illustrate the physical constraint, not a proposed rail tolerance or PCB design. A vertical rack busbar is also distinct from vertical power delivery beneath or through a chip package; “vertical” alone does not identify the scale.

## Multiphase regulation shares current and controls ripple

A multiphase buck regulator uses several switched power paths whose inductor currents join at the output. Interleaving their switching times reduces the combined ripple under the stated duty ratio and phase arrangement while sharing current and heat across stages. Feedback adjusts switching to regulate the output; capacitors support the remaining time-varying difference between inductor current and load current. These converter switching phases are not the three phases of the facility AC supply.

The output is not perfectly ripple-free. Ripple, transient droop, overshoot, parasitic resistance/inductance and control response remain finite. Phase count alone does not establish ripple or efficiency: the inductors, switching frequency, duty ratio, control method and operating load matter. The presentation’s one- and four-phase traces keep average total current fixed and state their normalized waveforms. They show cancellation of staggered ripple, not a measured GB300 VRM or a component-selection method.

## Conversion moves the loss as well as the voltage

For a converter with efficiency eta, useful output equals eta times electrical input. Therefore input equals output divided by eta, and loss equals input minus output. Work backward from the loads when the question is how much upstream capacity is required. If two converters operate in series, their efficiencies multiply. If two loads operate on parallel branches, their input powers add. Adding efficiencies, or applying a series product to parallel loads, gives an incorrect answer even when every component rating is accurate.

Conversion loss becomes heat where the conversion takes place. Moving an AC-to-DC stage into a separate power rack can move some heat and occupied space out of the compute rack. It does not make that heat disappear from the building. The final low-voltage regulation close to silicon still matters: supplying a high distribution voltage does not mean applying that voltage directly to a processor. Preserve the distinction between distribution bus, intermediate rail and point-of-load regulator in every diagram.

## Current is a local consequence of the boundary

At a declared DC boundary, P = V × I. A synthetic 100 kW load draws 2,000 A at 50 V and 125 A at 800 V. That sixteenfold difference follows from holding delivered power constant. It says nothing by itself about the total efficiency of two complete architectures. To compare conductor heating with I²R, first specify the same conductor resistance, including the return path. To compare conductor designs, resistance changes with geometry, length, temperature and connection details. Those are different comparisons.

For example, use a deliberately fixed 1 milliohm round-trip resistance. The idealized heating is 4 kW at 2,000 A and about 15.6 W at 125 A. This dramatic ratio is a property of the stipulated currents and unchanged resistance, not a predicted saving for a real rack. It excludes converters, connectors, insulation spacing, protection and cooling. A fair system comparison follows all losses from the same upstream point to the same useful loads, at the same operating conditions. The lower-current result is a reason to investigate architecture, not a completed design.

## Worked example: A synthetic rack power ledger

- A group of processor rails delivers 72 kW at a steady point.
- Point-of-load conversion efficiency is 92%. Other DC-bus loads total 12 kW, including all auxiliaries inside this example.
- The rack AC-to-DC shelf operates at 97% efficiency; no other electrical stages are inside the rack boundary.

1. Feed the processor regulators — 72 / 0.92 = 78.261 kW — The difference, 6.261 kW, is regulator loss.
2. Add parallel DC loads — 78.261 + 12 = 90.261 kW — The shelf supplies both branches; the 12 kW is already measured at its bus.
3. Find rack input — 90.261 / 0.97 = 93.052 kW — The shelf dissipates another 2.792 kW.
4. Close the ledger — 72 + 12 + 6.261 + 2.792 ≈ 93.052 kW — Rounding explains the last decimal; no load is counted twice.

**Result:** A 72 kW processor total corresponds to about 93.05 kW at this synthetic rack inlet.

**Model boundary:** The assumed efficiencies are illustrative operating points, not product specifications. Facility UPS losses and room cooling are outside this rack ledger.

## The tradeoff

Choice: Move a conversion stage outside the compute rack.

Benefit: Recover internal space and shift the location of converter heat and service work.

Cost: The external equipment still needs electrical capacity, cooling, protection and access; interconnecting losses must be included.

## When the situation changes

Trigger: An engineer allocates a feeder using processor power alone.

Mechanism: Parallel host, memory, switch and auxiliary demand plus conversion loss exceeds the omitted allowance.

Response: Reconcile a component ledger with inlet measurements for the specified workload and redundancy state before changing the allocation.

## Apply the idea

The 12 kW auxiliary branch increases to 18 kW while every other assumption remains fixed. How much additional AC input is required, and why is it not 6 kW?

<details>
<summary>Reveal the worked answer</summary>

Additional input is 6 / 0.97 = 6.186 kW; total rack input becomes about 99.238 kW.

Only the conversion stages upstream of a changed branch affect its incremental demand. Applying the 92% regulator efficiency would invent a path that this branch does not traverse. An actual shelf may change efficiency with loading, so the fixed-efficiency answer is a controlled approximation.

</details>

**The idea to keep:** Every efficiency has an input and output boundary; every watt entering the rack must have a destination.

## Sources and reading boundaries

- [NVIDIA NVL72 AI Factory — System Hardware & Components](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html) — The named rack includes compute, switching, management and power-shelf components; a rack is not only a GPU count. Read 2026-09-06. Mutable reference architecture, inspected as updated May 18, 2026. No advertised performance ratios or ambiguous aggregate-bandwidth recommendations are used.
- [NVIDIA DGX GB Rack Scale Systems — Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html#power-shelves) — Locate the DGX GB300 rear power busbar and distinguish PSUs, shelves and the nominal 50–51 V rack bus. Read 2026-09-12. Rack configuration and Power Shelves sections reviewed; manufacturer rear figure visually inspected. Shared GB200/GB300 guide has an approximately 120 kW consumption example that is not substituted for the enterprise GB300 up-to-142-kW requirement. This is not evidence of a one-BBU-per-NVL72 design or the unpublished board regulator implementation.
- [Advanced Energy — ORv3 Power Supply Unit](https://www.advancedenergy.com/en-us/products/ac-dc-power-supply-units/power-shelves/ocp-compliant/orv3-psu/) — A real 3 kW single-phase PSU with nominal 200–277 V AC input in a multi-module shelf; shelf input configuration differs from each PSU input. Read 2026-09-12. Product overview and Features inspected. This ORv3 product is not identified as the DGX GB300 power supply. No claimed peak efficiency is generalized to whole-rack conversion or an omitted 480-to-208-V transformer.
- [Texas Instruments — TIDA-050095 48V–12V 2kW four-phase bus converter](https://www.ti.com/tool/TIDA-050095) — Concrete intermediate-bus conversion example; DC/DC conversion can be transformer-less and can precede point-of-load regulation. Read 2026-09-12. Overview, Features and design-guide description reviewed; indexed System Description and specification table also inspected. No lab replication or claim that this reference design is installed in GB300. Manufacturer efficiency claims and separate maxima are not used as the course model. Multiphase waveforms are explicitly original normalized illustrations.
- [Texas Instruments — The decoupling capacitor: is it really necessary?](https://e2e.ti.com/blogs_/archives/b/precisionhub/posts/the-decoupling-capacitor-is-it-really-necessary) — Short local current paths and trace inductance explain why device decoupling is separate from distant stored energy. Read 2026-09-12. Authored article and figure descriptions 1–3 inspected. The example is an amplifier circuit, not a GPU benchmark. No suggested component value or layout instructions are imported; rack-level power transients are original stated models.
