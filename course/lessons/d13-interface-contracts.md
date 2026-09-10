# Two adequate products can form an inadequate system

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d13-interface-contracts`, then run `uv run gigawatt-expand`.

**D13 · Authored draft · Objectives:** D13.2

Translate requirements into measurable interfaces and use a simple flow calculation to expose an incompatibility before equipment arrives.

**Driving question:** What must be agreed at the boundary between a rack, a cooling unit and the facility?

## Start with the required behavior, not the catalog number

An owner requirement describes what the intended service must do. A design basis explains how the proposed arrangement will accomplish it. The WBDG commissioning-document guidance distinguishes these roles and connects them to reviewed records. In a data-center project, that distinction prevents a vendor selection from quietly redefining the service: an available component is not automatically an adequate response to the original workload, availability or operating envelope.

An interface contract should specify what crosses a boundary and under which conditions. For cooling, this includes temperatures, flow, pressure behavior, fluid compatibility and the division of control responsibility. For power, it includes the relevant electrical characteristics and protection assumptions. For information, it includes the meaning, units, timing and authority of exchanged signals. Physical connectors are only one part of compatibility; a connection can mate while the expected behavior remains impossible.

The contract also needs ownership. Who provides the requirement, who demonstrates it, who reviews the demonstration, and what happens when one side changes? A vague shared responsibility can leave both suppliers assuming the other side provides a necessary sensor or control function. Turning the interface into an explicit record exposes these gaps while the project can still change drawings or procurement terms.

## A simple energy balance can reject a nominally matching pair

Our synthetic rack requires removal of 1 MW through a single-phase water loop. At the stated load, its permitted temperature rise is at most 10 K. Use a supplied specific heat of 4.18 kJ/(kg·K), treated as constant for this exercise. The required mass flow is Q/(cp ΔT) = 1,000/(4.18 × 10) ≈ 23.9 kg/s. This calculation follows conservation of energy. It does not establish the pressure needed to move that flow through an actual rack.

Now suppose the proposed CDU has a headline rating above 1 MW, but the project’s documented connection limits flow through this rack path to 20 kg/s. At the allowed 10 K rise, that path carries only 836 kW in our simplified balance. A large thermal rating at some other test point does not remove the flow constraint. The pair cannot support the declared 1 MW brief without changing a requirement, component or arrangement and validating the revised conditions.

Raising the temperature difference is not a free arithmetic fix. The 10 K maximum was part of the rack operating brief. Permitting a larger rise would require evidence that device temperatures, materials, controls and supply/return requirements remain acceptable. Similarly, selecting a larger pump from one flow number would ignore pressure drop, fluid behavior and the actual connection limits. The energy calculation finds an incompatibility; it is not a complete selection tool.

## Acceptance criteria make a requirement observable

A requirement such as sufficient cooling is too vague to test. A stronger record identifies a declared heat load, inlet conditions, measurement locations, allowable behavior, duration and response to specified changes. Each acceptance condition should connect to recorded evidence. If temperature sensors are placed on different sides of a heat exchanger, their difference may not mean the quantity assumed in the flow calculation. The metering plan is therefore part of the interface agreement.

Control semantics deserve the same precision. State whether a reported flow is commanded, measured or inferred; whether an alarm denotes a warning or a protective action; and whether a value is instantaneous or averaged. Specify how stale or unavailable data is represented. A display that silently reuses its last good value can make a stopped communication path look like an unusually stable process. That is an interface failure even though the physical equipment has not changed.

When a revision arrives, compare it with the recorded interface before accepting the substitution. A lighter rack may alter center of gravity; a new CDU may change connection pressure; a software release may rename a signal or change its range. Record the affected requirements, retests and downstream documents. A disciplined change record saves time because it tells the project exactly what to re-examine instead of reopening every design question or assuming nothing consequential changed.

## Worked example: The missing 3.9 kg/s

- Synthetic rack heat duty 1,000 kW and maximum loop rise 10 K.
- Water specific heat is stipulated as 4.18 kJ/(kg·K).
- Documented path flow ceiling is 20 kg/s; steady, single-phase operation is assumed.

1. Required flow — 1,000 kJ/s / (4.18 kJ/(kg·K) × 10 K) = 23.9 kg/s — Units cancel to mass per time.
2. Duty at the stated flow ceiling — 20 × 4.18 × 10 = 836 kW — The allowed temperature rise and flow together bound this simple heat-transport model.
3. Unserved requirement — 1,000 − 836 = 164 kW — The proposed interface is short by 16.4 percent of the requested heat duty.

**Result:** The documented pairing does not meet the 1 MW requirement under these conditions, regardless of a larger rating at another test point.

**Model boundary:** No pump sizing, pressure-drop model, coolant specification or product capability is inferred beyond the supplied conditions.

## The tradeoff

Choice: Standardize interfaces before ordering several vendors’ equipment.

Benefit: It can make compatibility, substitutions and acceptance easier to evaluate.

Cost: It can constrain later product choices; poorly chosen common requirements can also exclude useful alternatives without improving the service.

## When the situation changes

Trigger: A component substitution preserves its headline MW rating but changes the accepted flow or control interface.

Mechanism: The system inherits an incompatibility not visible in the summary rating.

Response: Trace the changed interface to its requirements and evidence, then review the necessary redesign or retest before claiming equivalence.

## Apply the idea

A revised brief reduces heat duty to 800 kW with the same 10 K rise and 20 kg/s flow ceiling. Does it pass this energy-transport check?

<details>
<summary>Reveal the worked answer</summary>

Yes: 800/(4.18 × 10) ≈ 19.1 kg/s, below 20 kg/s.

The revised brief fits this particular flow-and-temperature calculation. It still requires evidence for exchanger performance, pressure, control behavior and the remaining interfaces. Passing one necessary condition is not the same as accepting the complete system.

</details>

**The idea to keep:** A product rating is useful only at the interface conditions the project actually needs. Assign ownership and acceptance evidence to the connection.

## Sources and reading boundaries

- [WBDG: Commissioning Documents](https://legacy.wbdg.org/building-commissioning/commissioning-documents) — The OPR, basis-of-design and review discussion supports requirements ownership and traceable acceptance documentation. Read 2026-09-06. Selected document-role and design-review passages inspected; no standard text or complete acceptance procedure is reproduced.
- [Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) — Design-phase feedback and early monitoring/control coordination are relevant to interface validation. Read 2026-09-06. Selected highlights reviewed. All rack/CDU numbers and failure scenarios here are synthetic, not ASHRAE product ratings.
