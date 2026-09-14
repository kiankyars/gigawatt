const photo = (name, alt, credit, contain = false) => `<figure class="case-photo${contain ? " case-contain" : ""}"><img src="../assets/references/${name}" alt="${alt}"><figcaption>${credit}</figcaption></figure>`;
const result = (markup, description) => ({ markup, description, format: "html" });
const svg = (label, body, view = "0 0 720 350") => `<svg class="case-diagram" viewBox="${view}" role="img" aria-label="${label}">${body}</svg>`;

export function renderSiteCase(id, state = {}) {
  if (id === "mineral-project") return result(
    `<div class="texas-case"><figure class="texas-chart"><img src="../assets/references/semianalysis-btm-by-state-2026.png" alt="SemiAnalysis BTM Tracker, 24 August 2026: Texas leads named states with about 17 GW of booked onsite generation; another 29 GW has no site chosen. The chart measures generator nameplate, excluding batteries."></figure><aside class="texas-project"><h2>Odessa · New Era</h2><p>Texas Critical Data Centers</p><dl><div><dt>493 acres</dt><dd>Land secured</dd></div><div><dt>1 operator</dt><dd>Surface waiver pending</dd></div></dl><small>Project update · 14 Aug 2026</small></aside></div>`,
    "The original SemiAnalysis chart ranks booked onsite generation by named-site state, not counts of data centers: Texas about 17 GW, with 29 GW of orders having no site selected. Separately, New Era reported 493 acres secured near Odessa but a final leasehold operator surface waiver still pending on August 14, 2026."
  );
  if (id === "ground-and-foundations") return result(
    `<div class="case-split">${photo("menard-ada-docklands-groundworks.webp", "Menard drilling rigs at ADA Infrastructure's London Docklands data-center site.", "Menard · ADA Infrastructure, London Docklands")}<div class="case-details"><h2>Former industrial ground</h2><div class="case-soil"><span>Up to 6 m of fill</span><span>Soft river deposits below</span></div><dl><div><dt>Buildings</dt><dd>Deep piles cast into the ground</dd></div><div><dt>External areas & utilities</dt><dd>≈7,000 ground-improvement columns</dd></div></dl><p>Column positions and utility depths had to fit together.</p></div></div>`,
    "ADA Infrastructure's London Docklands site had up to six metres of fill over soft alluvium and buried industrial obstructions. Menard installed about 7,000 ground-improvement columns across 40,000 square metres of external areas; CFA piles support the buildings. Utility depths and columns required coordination."
  );
  if (id === "outside-flood") return result(
    `<div class="case-status"><div class="case-heading"><h2>Equinix HO1 · Houston</h2><p>Hurricane Harvey · 28 August 2017</p></div><div class="case-status-pair"><article><b>Online</b><h3>Data center staffed and operating</h3><p>Equinix reported no interruption at HO1.</p></article><article><b>Roads closed</b><h3>Customers could not reach it</h3><p>Flooding blocked the surrounding streets.</p></article></div><div class="case-takeaway">The team stayed for days, pumping out water and keeping power on.</div></div>`,
    "Equinix reported that Houston HO1 remained staffed and operating on August 28, 2017 while surrounding streets were closed by flooding and customers could not reach it. Its later employee account describes staff staying for days and pumping water out while keeping power on. This is not a dry-campus claim or a reported bridge failure."
  );
  if (id === "neighbors-and-permits") return result(
    `<div class="case-split">${photo("parklane-rogers-rooftop-acoustic-barrier.jpg", "Actual acoustic screen around Rogers' rooftop data-center chillers, with neighboring residences beside it.", "Parklane · Rogers headquarters, Toronto")}<div class="case-details"><h2>Chillers opposite residences</h2><dl><div><dt>15 ft high</dt><dd>Screen around the rooftop plant</dd></div><div><dt>16 sections</dt><dd>Factory-built, then lifted into place</dd></div></dl><p>The wall interrupts the direct sound path while the open top allows airflow.</p></div></div>`,
    "Parklane's Rogers headquarters data-center retrofit in Toronto placed a 15-foot acoustic barrier around rooftop chillers facing residences. Sixteen factory-built wall sections were installed in one ten-hour day. The actual photo shows the screen and neighboring buildings; its sound reduction is not quantified here."
  );
  if (id === "hot-swap") return result(
    `<div class="case-hotswap">${photo("lenovo-gb300-power-shelf.png", "Lenovo GB300 power shelf showing six front-access 5.5 kW hot-swap power supply modules.", "Lenovo · GB300 NVL72 product guide", true)}<div class="case-hotswap-pair"><article><h2>Power-supply module</h2><p>Replace one while the remaining qualified supplies carry the load.</p></article><article><h2>Compute tray</h2><p>Lenovo requires that tray to be powered off before removal.</p></article></div></div>`,
    "Lenovo's GB300 shelf contains six 5.5 kW hot-swappable PSU modules. A supported module replacement can keep the rack powered when the remaining supplies and configuration support the load. The compute tray has a different service boundary: Lenovo requires it powered off before removal, so its workload must stop or move."
  );

  return null;
}
