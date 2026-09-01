# Testing the course

Run the diagram server and open the canonical player:

```sh
python3 -m http.server --directory diagram 8000
```

Open `http://localhost:8000/course_v2.html`. The player and its six phase
renderers must be served over HTTP because the outer shell controls the
same-origin phase frames.

The useful test is not a timed read-through. Begin on the opening journey, enter
each of the six phases, and advance only when the explanation naturally calls
for a different relationship. Finish on the three-lens synthesis. The presenter
does not have to use every available manual state in every recording.

Use six passes:

1. **Journey.** Do Generate, Transmit, Campus, Building, Compute, and Reject heat
   feel like six necessary engineering problems in one service chain without
   implying that grid and onsite branches are one traced path?
2. **Visual support.** Can each state carry several minutes of explanation
   without the presenter having to invent the causal diagram? If a view becomes
   stale, name the relationship that should change; generic zooming is not a
   useful transformation.
3. **Evidence boundary.** Open the evidence drawer in every phase. Can you tell
   what is generic guidance, what is evidenced at Abilene, and what remains
   unknown without treating a null as zero?
4. **Boundary.** Does each phase input/output boundary make the next engineering
   problem feel necessary? Does the closing synthesis re-read the completed
   journey rather than add a seventh physical phase?
5. **Interaction.** Check the phase compass, state rail, previous/next controls,
   evidence drawer, `Escape`, and keyboard arrow/Home/End behavior. Repeat at
   1920x1080, 1440x900, 1024x768, 844x390, and 390x844 with no clipped labels or
   horizontal overflow.
6. **State-bound spatial views.** At 1920x1080, 1440x900, and 1024x768, select
   every configured state below. Confirm its named 3D camera or segment frame is
   the primary view, the child course chrome stays hidden, and the view-specific
   boundary remains readable. Use `Open 2D explanation` and `Return to 3D system
   view`; both must preserve the phase, state, and keyboard focus. Arrow keys
   must navigate the outer state rail rather than drift inside the embedded v1
   sequence. Shrink through 900 px and confirm the same state returns to its 2D
   explanation. At 844x390 and 390x844, confirm the 3D switch is absent and the
   2D course remains complete.

   - Phase 1: `abilene_selection` → `s01_fire_to_electricity` and
     `transmission_handoff` → `s02_generator_terminal`.
   - Phase 2: `abilene_grid_paths` → `campus_establishing`; confirm the view
     does not imply a resolved interface or common campus bus.
   - Phase 3: `abilene_unknown_merge` → `campus_establishing`; confirm the
     no-as-built-merge boundary is explicit.
   - Phase 4: `equipment_by_verb` → `s07_building_power_train`.
   - Phase 5: `orient_inside_rack` → `s08_rack_voltage_descent`.
   - Phase 6: `rack_cooling_split`, `technology_loop`, `cdu_boundary`,
     `parallel_residual_air`, `facility_heat_rejection`, `water_accounting`, and
     `whole_journey_closure` → `s10` through `s16` in order.

For feedback, record the phase and state ID with one concrete observation:

```text
phase_4_building / one_path_unavailable
What stalled: ...
Visual relationship wanted: ...
Evidence wording that felt awkward: ...
```

The byte-preserved v1 renderer remains available locally at
`http://localhost:8000/course.html` and is published at both
`/gigawatt/course.html` for v2 state views and `/gigawatt/v1.html` for direct
historical comparison. Reusing its validated renderer and frames does not reuse
the old sequence or its historical acceptance evidence as v2 evidence.

There is deliberately no target duration per phase or state. The presenter owns
the course length and spoken explanation.
