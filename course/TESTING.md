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
for a different relationship. Finish on the three-lens synthesis. There are 33
available manual states, but the presenter does not have to use every state in
every recording.

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
6. **Spatial anchors.** At 1920x1080, 1440x900, and 1024x768, open `3D spatial
   anchor` in Phases 4, 5, and 6. Confirm the selected views are Electrical room,
   Data hall and rack, and Thermal return; the child masthead and transport stay
   hidden; arrow keys cannot drift to another camera; and `Escape` or `Return to
   2D teaching` restores the same state and keyboard focus. Shrink through 900
   px while 3D is open and confirm the 2D state returns. At 844x390 and 390x844,
   confirm the 3D control is absent and the 2D course remains complete.

For feedback, record the phase and state ID with one concrete observation:

```text
phase_4_building / one_path_unavailable
What stalled: ...
Visual relationship wanted: ...
Evidence wording that felt awkward: ...
```

The frozen v1 comparison remains available locally at
`http://localhost:8000/course.html` and on GitHub Pages at
`/gigawatt/v1.html`. Use it only to compare the former 26-segment redline-led
runtime with v2; its historical acceptance evidence is not evidence for the
replacement course.

There is deliberately no target duration per phase or state. The presenter owns
the course length and spoken explanation.
