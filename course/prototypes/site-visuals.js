import { renderSiteContext } from "./site-context-visuals.js";
import { renderOperations } from "./site-operations.js";

export function renderSite(id, state, compact = false) {
  const visual =
    renderSiteContext(id, state, compact) ?? renderOperations(id, state, compact);
  if (!visual) throw new RangeError(`Unknown site scene: ${id}`);
  return visual;
}
