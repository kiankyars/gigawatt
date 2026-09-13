const aerial = "../assets/references/colossus-1-aerial.jpg";
const abilene =
  "https://www.oracle.com/cmsng/img/0cb07dd3d128f06e666f776839f78314.jpg";
const rack =
  "https://lenovopress.lenovo.com/assets/images/LP2357/Lenovo_GB300_NVL72_Rack_left_front_v3.jpg";
const tray =
  "https://lenovopress.lenovo.com/assets/images/LP2357/Lenovo%20NVIDIA%20GB300%20Compute%20rear%20view.png";
const result = (markup, description) => ({
  markup,
  description,
  format: "html",
});
const photo = (src, alt, credit = "", cls = "") =>
  `<figure class="site-photo ${cls}"><img src="${src}" alt="${alt}">${credit ? `<figcaption>${credit}</figcaption>` : ""}</figure>`;
const tag = (text, x, y) =>
  `<span class="site-tag" style="--x:${x}%;--y:${y}%">${text}</span>`;
const sceneImage = (name, alt, tags = "") =>
  `<div class="site-landscape"><div class="site-image-plane"><img src="../assets/generated/${name}.png" alt="${alt}">${tags}</div></div>`;
const svg = (label, content, view = "0 0 1000 440") =>
  `<svg class="site-schematic" viewBox="${view}" role="img" aria-label="${label}" xmlns="http://www.w3.org/2000/svg">${content}</svg>`;
const txt = (x, y, s, cls = "") =>
  `<text x="${x}" y="${y}" class="${cls}">${s}</text>`;
const building = (x, y, w = 300) =>
  `<path d="M${x},${y}v-70l25,-20h${w - 50}l25,20v70z" fill="var(--surface)" stroke="var(--text)" stroke-width="2"/><path d="M${x + 25},${y - 90}v90M${x + w - 25},${y - 90}v90" stroke="var(--line)"/>${Array.from({ length: 6 }, (_, i) => `<path d="M${x + 45 + (i * (w - 70)) / 6},${y - 64}v52" stroke="var(--power)" stroke-width="10"/>`).join("")}`;
function fiberPlan(shared) {
  const c = "var(--data)",
    d = "var(--power)";
  return svg(
    shared
      ? "Two fiber services share one entrance"
      : "Two fiber approaches enter separate sides",
    `<rect x="155" y="120" width="230" height="185" rx="6" fill="var(--panel)" stroke="var(--line)"/><path d="M180 140v140m35-140v140m35-140v140m35-140v140m35-140v140m35-140v140" stroke="var(--text)" stroke-width="12" opacity=".4"/>${shared ? `<path d="M25 32H65V215H155M25 365H85V235H155" fill="none" stroke="${c}" stroke-width="6"/><path d="M25 365H85V235H155" fill="none" stroke="${d}" stroke-width="6"/><rect x="130" y="192" width="48" height="64" rx="6" fill="var(--heat)" opacity=".2"/><path d="M138 200l33 49m0-49l-33 49" stroke="var(--heat)" stroke-width="4"/>${txt(240, 355, "One entrance exposed", "site-svg-small")}` : `<path d="M25 32H80V165H155" fill="none" stroke="${c}" stroke-width="6"/><path d="M425 365H455V260H385" fill="none" stroke="${d}" stroke-width="6"/>${txt(100, 100, "A", "site-svg-label")}${txt(430, 325, "B", "site-svg-label")}`}`,
    "0 0 480 400",
  );
}
export function renderSiteContext(id) {
  switch (id) {
    case "site-purpose":
      return result(
        `<div class="site-opening">${sceneImage("site-building-cutaway", "Conceptual cutaway linking the data hall, support rooms and equipment receiving route.")}<div class="site-opening-rail"><span><b>Parcel</b>Land & connections</span><span><b>Building</b>Rooms & routes</span><span><b>Equipment</b>Service & recovery</span></div></div>`,
        "The chapter follows three physical scales: land and connection rights at the parcel, rooms and routes within the building, then equipment service and recovery.",
      );
    case "greenfield-brownfield":
      return result(
        `<div class="site-site-pair"><article><h2>Abilene <span>New campus</span></h2>${photo(abilene, "Oracle aerial of the Crusoe-built Abilene AI campus.", "Oracle · July 2026")}<p>Purpose-built layout</p></article><article><h2>Colossus 1 <span>Former Electrolux factory</span></h2>${photo(aerial, "Official SpaceXAI aerial of Colossus 1 on Paul Lowery Road in Memphis.", "SpaceXAI")}<p>Existing shell & utility mains</p></article></div>`,
        "Actual aerials compare the new Abilene campus with Colossus 1 in the former Electrolux factory. Reuse preserved a shell and selected infrastructure while retaining site constraints.",
      );
    case "colossus-service":
      return result(
        `<div class="site-photo-ledger">${photo(aerial, "Colossus 1 occupies the former Electrolux factory.", "SpaceXAI")}<div class="site-ledger"><h2>First 150 MW of grid service</h2><div class="site-service-bar"><span>8</span><strong>142 MW · new substation</strong></div><p class="site-key"><i></i>8 MW · existing substation</p><div class="site-mains"><span><b>20-inch</b>Existing water main</span><span><b>16-inch</b>Existing gas main</span><span><b>8-inch</b>New gas tap</span></div><small>MLGW · historical 2025 update</small></div></div>`,
        "MLGW’s 2025 update reported 8 MW through the existing substation and 142 MW through a new one for the first 150 MW of grid service. Existing water and gas mains could be reused, with a new gas tap. These are historical utility-service quantities.",
      );
    case "usable-land":
      return result(
        sceneImage(
          "site-usable-parcel",
          "Concept campus fitted between a transmission easement and drainage area; neither is available for the building pads.",
          tag("Utility easement", 17, 44) +
            tag("Building pads", 53, 43) +
            tag("Drainage", 86, 43),
        ),
        "A concept parcel reserves the transmission corridor on one side and drainage on the other. The connected space between them must accommodate buildings, outdoor plant and access.",
      );
    case "rights-and-routes":
      return result(
        `<div class="site-section-wrap">${svg("Texas split estate: the surface and minerals can have separate owners", `<defs><pattern id="mineral-hatch" width="24" height="14" patternUnits="userSpaceOnUse"><path d="M0 12h12m5-7h6" stroke="#b8935b" opacity=".6"/></pattern></defs><path d="M45 200H955V382H45Z" fill="#c7b28c"/><path d="M45 235Q300 208 485 248T955 242V382H45Z" fill="#b4915f"/><path d="M45 300Q350 266 560 316T955 305V382H45Z" fill="url(#mineral-hatch)"/><path d="M45 200H955" stroke="var(--power)" stroke-width="8"/>${building(145, 196, 325)}<path d="M760 196L786 95H794L820 196M773 145H807M766 172H813M766 172L807 145M773 145L813 172M790 200v132h-145" fill="none" stroke="var(--heat)" stroke-width="6" stroke-linecap="round"/>${txt(65, 55, "TEXAS · SPLIT ESTATE", "site-svg-label")}${txt(490, 162, "Surface owner", "site-svg-title")}${txt(858, 137, "Well", "site-svg-small")}${txt(90, 294, "Mineral owner", "site-svg-title site-soil-text")}${txt(90, 329, "May retain rights to use the surface", "site-svg-small site-soil-text")}`)}<div class="site-single-callout">Deeds · mineral leases · surface-use agreements</div></div>`,
        "Texas surface and mineral estates can belong to separate owners. The mineral estate generally carries rights to reasonably necessary surface use; deeds, leases, ordinances and the accommodation doctrine can limit those rights. This is a conceptual Texas case, not a mineral dispute at Abilene.",
      );
    case "ground-and-foundations":
      return result(
        `<div class="site-comparison"><article><h2>Firm bearing layer near the surface</h2>${svg("A shallow foundation transfers the building load into firm near-surface ground", `<path d="M30 205H455V390H30Z" fill="#b5a17c"/><path d="M30 250H455M30 275H455M30 300H455M30 325H455M30 350H455" stroke="#92815f" opacity=".5"/>${building(75, 190, 320)}<path d="M96 190v24h-29v25h115v-25h-29v-24m165 0v24h-29v25h115v-25h-29v-24" fill="var(--power)"/>${txt(245, 374, "Shallow footings", "site-svg-label site-soil-text")}`, "0 0 490 410")}</article><article><h2>Weak or compressible upper layers</h2>${svg("Piles carry the building load past weak layers to deeper support", `<path d="M30 205H455V302H30Z" fill="#e0cfac"/><path d="M30 225Q125 200 215 234T455 220M30 259Q125 234 215 268T455 254" fill="none" stroke="#bda882"/><path d="M30 302H455V390H30Z" fill="#b5a17c"/>${building(75, 190, 320)}<path d="M60 195H190v19H60zm235 0H425v19H295zM85 214h16v125H85zm63 0h16v125h-16zm165 0h16v125h-16zm63 0h16v125h-16z" fill="var(--power)"/>${txt(245, 374, "Deep foundations", "site-svg-label site-soil-text")}`, "0 0 490 410")}</article></div>`,
        "A conceptual section contrasts shallow footings on competent near-surface material with deep foundations that transfer load past weaker layers. Geotechnical investigation selects the actual solution; piles are not the only possible response.",
      );
    case "outside-flood":
      return result(
        sceneImage(
          "site-flood-access",
          "Concept campus on dry high ground, with its only approach interrupted at a flooded bridge.",
        ),
        "The data hall remains on dry higher ground, but a flooded bridge prevents deliveries and service access. The vulnerability lies along an offsite dependency, not inside the building.",
      );
    case "fiber-diversity":
      return result(
        `<div class="site-fiber"><div class="site-case-band"><b>QTS Suwanee</b><span>Diverse entrances + redundant campus conduits</span></div><div class="site-comparison"><article><h2>Shared entrance</h2>${fiberPlan(true)}</article><article><h2>Separate approaches</h2>${fiberPlan(false)}</article></div></div>`,
        "QTS documents physical entrance diversity at Suwanee. These conceptual diagrams compare a shared entry point with separate approaches. The second removes the illustrated common exposure without asserting end-to-end independence.",
      );
    case "climate-and-water":
      return result(
        `<div class="site-site-pair site-cooling"><article><h2>Abilene</h2>${photo(abilene, "The Abilene AI campus.", "Oracle")}<div class="site-cooling-note"><b>Air-cooled chillers</b><span>No evaporative heat rejection</span></div></article><article><h2>Colossus 1</h2>${photo(aerial, "The Colossus 1 AI factory in Memphis.", "SpaceXAI")}<div class="site-cooling-note"><b>Cooling towers + air-cooled chillers</b><span>Towers consume makeup water</span></div></article></div>`,
        "Abilene uses non-evaporative air-cooled chillers. Colossus 1 has both evaporative cooling towers and air-cooled chillers, according to the TDEC cooling-use record and FAS original imagery analysis. A closed indoor liquid loop does not determine outdoor heat rejection.",
      );
    case "neighbors-and-permits":
      return result(
        sceneImage(
          "site-neighbor-boundary",
          "Concept illustration: outdoor plant, acoustic barrier, and neighboring homes; sound paths are reduced beyond the barrier.",
          tag("Outdoor plant", 40, 39) +
            tag("Acoustic barrier", 66, 53) +
            tag("Neighbors", 89, 66),
        ),
        "The concept locates an acoustic barrier between outdoor plant and neighboring homes. Placement, source sound and propagation inform the design; the illustration specifies no decibel reduction or compliant dimensions.",
      );
    case "phased-campus":
      return result(
        `<div class="site-phasing"><div class="site-phase-dates"><span><b>27 Oct 2025</b>First 50 MW ready for service</span><span><b>24 Nov 2025</b>Next 50 MW ready for service</span></div><div class="site-phase-plan"><div class="site-live-wing"><strong>Operating phase</strong><div class="site-rack-rows">${"<i></i>".repeat(18)}</div><span>Service entrance</span></div><div class="site-build-wing"><strong>Next phase</strong><div class="site-build-grid"></div><span>Construction entrance</span></div><div class="site-path-service">Operations access</div><div class="site-path-build">Construction access</div></div><small>Applied Digital · Polaris Forge 1 · CoreWeave tenant</small></div>`,
        "Applied Digital’s Polaris Forge 1 reached its first 50 MW ready-for-service milestone October 27, 2025, and the next 50 MW November 24. The generic site plan explains why live operations need routes protected from adjacent construction; it does not depict the actual campus plan.",
      );
    case "room-layout":
      return result(
        sceneImage(
          "site-building-cutaway",
          "Conceptual roof-off building with a rack hall, electrical room, mechanical gallery and receiving corridor.",
          tag("Electrical room", 47, 13) +
            tag("Data hall", 34, 43) +
            tag("Mechanical gallery", 82, 36) +
            tag("Receiving & service route", 73, 78),
        ),
        "A concept cutaway places the data hall next to its electrical and mechanical support rooms. Receiving and the internal service corridor connect equipment delivery to the rooms where maintenance occurs.",
      );
    case "gb300-physical":
      return result(
        `<div class="site-product"><article>${photo(rack, "Lenovo ThinkSystem NVIDIA GB300 NVL72 rack, actual product photograph.", "Lenovo")}<div><h2>GB300 NVL72</h2><b class="site-mass">≈1,580 <span>kg</span></b><p>Complete rack · configuration dependent</p></div></article><article>${photo(tray, "Rear of an actual Lenovo GB300 compute tray with power and coolant interfaces.", "Lenovo")}<div><h2>Compute tray</h2><b class="site-mass">29 <span>kg</span></b><p>Service with a material lift</p></div></article></div>`,
        "Lenovo specifies approximately 1,580 kilograms for the complete GB300 NVL72 rack, depending on configuration, and 29 kilograms for a compute tray. Actual product photographs anchor the structural and handling discussion.",
      );
    default:
      return null;
  }
}
