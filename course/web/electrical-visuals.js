/* Legacy sample bridge; the same renderer is imported by Chapter 8. */
function electricalRenderers() {
  return createElectricalVisuals({ acdcWaveModel, getState: () => state, escapeHTML, fmt });
}
function electricalVisual(kind) { return electricalRenderers().electricalVisual(kind); }
function electricalContent(kind) { return electricalRenderers().electricalContent(kind); }
