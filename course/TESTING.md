# Testing the course

Run the diagram server and open the complete player:

```sh
python3 -m http.server --directory diagram 8000
```

Open `http://localhost:8000/course.html`.

The useful test is not a timed read-through. Move through the 26 segments in
your own words and advance only when the explanation naturally changes what the
viewer should see. Within any segment, `Show context` widens the frame and
`Show evidence` exposes the claim boundary and primary sources. Those are
optional transformations, not a required sequence.

The renderer is local: after the page has loaded from the diagram server, the
course does not require a CDN or internet connection. Press `E` to open the
evidence drawer and `Escape` to close it; keyboard focus should return to the
evidence button.

Use three passes:

1. **Understanding.** Can the opening question lead you into the idea without
   reading prose? Can you explain the objective in your own language?
2. **Visual support.** Does the focused frame remain useful? If it becomes
   stale, does context or evidence create the coarse visual change you want?
3. **Handoff.** Does the final cue make the next segment feel like the natural
   next question?

For feedback, record the segment ID and one concrete observation:

```text
s14_facility_heat_rejection
What stalled: ...
Visual change wanted: ...
Evidence wording that felt awkward: ...
```

There is deliberately no target duration per segment and no expectation that
every available transformation be used. The presenter owns the course length.
