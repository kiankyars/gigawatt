const result = (markup, description) => ({ markup, description, format: "html" });

export function renderCaseContext(id) {
  if (id === "docklands-context") return result(
    `<div class="context-feature context-docklands"><figure class="context-image"><img src="../assets/references/site-ada-docklands-proposed-campus.webp" alt="ADA Infrastructure’s proposed Docklands campus beside the Thames, shown in its June 2024 planning announcement."><figcaption>Proposed campus · ADA Infrastructure · June 2024</figcaption></figure><div class="context-landmarks"><p><strong>East London</strong><span>Royal Docks</span></p><p><strong>New campus</strong><span>Three planned data-center buildings</span></p><p><strong>Industrial past</strong><span>Old structures remain below ground</span></p></div></div>`,
    "ADA Infrastructure planned three data-center buildings in East London’s Royal Docks. The developer’s June 2024 visualization shows the proposed campus beside the Thames. Menard’s groundworks account identifies buried industrial structures beneath the site; the next slide explains their engineering consequences."
  );
  if (id === "harvey-context") return result(
    `<div class="context-feature context-harvey"><figure class="context-image"><img src="../assets/references/site-harvey-houston-road-2017.png" alt="Houston-area road submerged by Hurricane Harvey flooding, with the city skyline beyond, on August 28, 2017. Photograph credited to TxDOT by the National Weather Service."><figcaption>Houston-area flooding · 28 Aug 2017 · TxDOT / NWS</figcaption></figure><div class="context-landmarks context-timeline"><p><strong>25 Aug</strong><span>Landfall on the Texas coast</span></p><p><strong>26–27 Aug</strong><span>Flash flooding across Houston’s Harris County</span></p><p><strong>29–30 Aug</strong><span>More heavy rain worsens the floods</span></p></div></div>`,
    "Harvey made landfall on the Texas coast on August 25, 2017. The storm moved slowly and rain bands persisted. Rapid flash flooding spread across Harris County during the night of August 26–27; heavy rain on August 29–30 worsened the ongoing flooding. This August 28 TxDOT image depicts Houston-area road flooding, not Equinix HO1 or its specific access route."
  );
  return null;
}
