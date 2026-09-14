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
    case "climate-and-water":
      return result(
        `<div class="site-site-pair site-cooling"><article><h2>Abilene</h2>${photo(abilene, "The Abilene AI campus.", "Oracle")}<div class="site-cooling-note"><b>Air-cooled chillers</b><span>Heat rejected to outdoor air</span></div></article><article><h2>Colossus 1</h2>${photo(aerial, "The Colossus 1 AI factory in Memphis.", "SpaceXAI")}<div class="site-cooling-note"><b>Cooling towers + air-cooled chillers</b><span>Makeup water = water added to replace losses</span></div></article></div>`,
        "Abilene uses non-evaporative air-cooled chillers. Colossus 1 has both evaporative cooling towers and air-cooled chillers, according to the TDEC cooling-use record and FAS original imagery analysis. Makeup water replaces evaporation, blowdown and other tower losses; the term does not specify potable or reclaimed water. This is a site-selection preview; the cooling chapters explain the mechanisms.",
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
