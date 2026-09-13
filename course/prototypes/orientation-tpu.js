// TPU v4 is a concrete historical architecture, not a claim about every TPU generation.
// Sources: Google Cloud (5 April 2023) and Zu et al., NSDI 2024, sections 1–2.
const photo =
  "https://storage.googleapis.com/gweb-cloudblog-publish/images/1_Cloud_TPU_v4.max-1100x1100.jpg";
const label = (x, y, value, size = 20, color = "text", weight = 500) =>
  `<text x="${x}" y="${y}" text-anchor="middle" fill="var(--${color})" font-size="${size}" font-weight="${weight}">${value}</text>`;
const panel = (x, y, w, h, color = "line") =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="13" fill="var(--surface)" stroke="var(--${color})" stroke-width="1.5"/>`;
const line = (d, color = "data", width = 4) =>
  `<path d="${d}" fill="none" stroke="var(--${color})" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round"/>`;

export function renderTpuPreview(compact = false) {
  if (compact) {
    return (
      `<image href="${photo}" x="20" y="16" width="350" height="100" preserveAspectRatio="xMidYMid meet" aria-label="Google photograph of eight racks, one eighth of a TPU v4 pod"/>` +
      label(195, 138, "Google · one eighth of a TPU v4 pod", 14, "muted") +
      label(195, 204, "4,096 TPU v4 chips", 29, "text", 650) +
      label(195, 238, "64 blocks × 64 chips", 19, "muted") +
      panel(15, 300, 98, 125, "data") +
      panel(277, 300, 98, 125, "data") +
      label(64, 338, "Block A", 18, "text", 650) +
      label(64, 399, "64 chips", 17) +
      label(326, 338, "Block B", 18, "text", 650) +
      label(326, 399, "64 chips", 17) +
      panel(131, 278, 128, 167) +
      label(195, 313, "OCS", 24, "text", 650) +
      line("M113 364L172 401L219 345L277 364") +
      line("M159 403L185 399M207 348L231 342", "text", 5) +
      label(195, 480, "Mirrors connect optical ICI links", 20, "data", 600) +
      label(195, 512, "ICI = inter-chip interconnect", 17) +
      label(195, 540, "Two blocks and one link shown", 14, "muted") +
      line("M30 575H360", "line", 1.5) +
      label(195, 615, "Gemini Ultra spans data centers", 19, "text", 600) +
      label(195, 647, "Pods connect over separate networks", 17, "muted")
    );
  }
  return (
    `<image href="${photo}" x="20" y="22" width="668" height="190" preserveAspectRatio="xMidYMid meet" aria-label="Google photograph of eight racks, one eighth of a TPU v4 pod"/>` +
    label(354, 238, "Google · one eighth of a TPU v4 pod", 17, "muted") +
    panel(730, 22, 410, 216) +
    label(935, 112, "4,096", 64, "text", 650) +
    label(935, 163, "TPU v4 chips", 27) +
    label(935, 196, "64 blocks × 64 chips", 20, "muted") +
    panel(20, 365, 220, 138, "data") +
    panel(920, 365, 220, 138, "data") +
    label(130, 402, "Block A", 25, "text", 650) +
    label(130, 471, "64 TPU chips", 21) +
    label(1030, 402, "Block B", 25, "text", 650) +
    label(1030, 471, "64 TPU chips", 21) +
    panel(378, 282, 404, 224) +
    label(580, 319, "Optical circuit switch (OCS)", 25, "text", 650) +
    label(580, 353, "Mirrors set the optical connection", 18, "muted") +
    line("M240 434L503 465L655 394L920 434", "data", 5) +
    line("M482 468.4L524 461.6M634 397L676 391", "text", 7) +
    label(580, 537, "ICI = inter-chip interconnect · two blocks and one link shown", 18, "muted") +
    label(580, 576, "Gemini Ultra joins pods across data centers over intra- and inter-cluster networks.", 19)
  );
}
