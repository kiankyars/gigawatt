// The user supplied this complete passage. Keep its wording and punctuation intact.
export const microsoftPowerManagementQuote = Object.freeze({
  id: "power-management-quote",
  label: "Microsoft · managing power oscillations",
  title: "Software, GPU thresholds and on-site storage",
  domain: "D05",
  objectives: Object.freeze(["D05.1", "D05.3"]),
  reading: "d05-paths-and-transitions",
  text: "We have also worked with our industry partners to codevelop power-management solutions to mitigate power oscillations created by large scale jobs, a growing challenge in maintaining grid stability as AI demand scales. This includes a software-driven solution that introduces supplementary workloads during periods of reduced activity, a hardware-driven solution where the GPUs enforce their own power thresholds and an on-site energy storage solution to further mask power fluctuations without utilizing excess power.",
  author: "Scott Guthrie",
  publisher: "Microsoft",
  publishedOn: "2025-11-12",
  displayDate: "12 November 2025",
  sourceTitle: "Infinite scale: The architecture behind the Azure AI superfactory",
  sourceUrl: "https://blogs.microsoft.com/blog/2025/11/12/infinite-scale-the-architecture-behind-the-azure-ai-superfactory/",
  reviewedOn: "2026-09-15",
  scope: "Microsoft describes partner-developed solutions in the Fairwater article’s power section, immediately after its Atlanta design discussion. This paragraph does not establish deployment at every Azure site or enumerate the implementation status of each solution at Atlanta.",
});

const escapeHTML = (value) => String(value).replace(/[&<>"']/g, (character) => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
})[character]);

export function renderMicrosoftPowerManagementQuote({ compact = false } = {}) {
  const quote = microsoftPowerManagementQuote;
  return `<figure class="continuity-case-quote${compact ? " continuity-case-quote--compact" : ""}">
    <blockquote cite="${escapeHTML(quote.sourceUrl)}"><p>${escapeHTML(quote.text)}</p></blockquote>
    <figcaption>
      <span class="continuity-case-quote__attribution">${escapeHTML(quote.author)} · ${escapeHTML(quote.publisher)} · <time datetime="${quote.publishedOn}">${quote.displayDate}</time></span>
      <a href="${escapeHTML(quote.sourceUrl)}" target="_blank" rel="noopener noreferrer">${escapeHTML(quote.sourceTitle)}</a>
    </figcaption>
  </figure>`;
}
