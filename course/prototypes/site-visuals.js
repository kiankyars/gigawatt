import { renderSiteReview } from "./site-review-visuals.js";
import { renderSiteCase } from "./site-cases.js";
import { renderCaseContext } from "./site-case-contexts.js";
import { renderSiteContext } from "./site-context-visuals.js";
import { renderOperations } from "./site-operations.js";

export function renderSite(id, state, compact = false) {
  const visual =
    renderSiteReview(id, state, compact) ?? renderCaseContext(id) ?? renderSiteCase(id, state, compact) ?? renderSiteContext(id, state, compact) ?? renderOperations(id, state, compact);
  if (!visual) throw new RangeError(`Unknown site scene: ${id}`);
  return visual;
}
