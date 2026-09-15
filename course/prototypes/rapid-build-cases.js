const SEMIANALYSIS = "https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters";
const META = "https://engineering.fb.com/2025/09/29/data-infrastructure/metas-infrastructure-evolution-and-the-advent-of-ai/";
const CEI = "https://www.cei.com/core-markets/modular";

export const rapidBuildScenes = [
  {
    id: "meta-prometheus-tents",
    label: "Meta: weatherproof tents",
    title: "Meta put part of Prometheus under weatherproof tents.",
    pedagogical_role: "case-study",
    reference: "d12-hazards-and-site-evidence",
    sources: [META, SEMIANALYSIS],
    explanation: [
      "Meta’s September 29, 2025 engineering account says Prometheus combines conventional buildings, weatherproof tents and adjacent colocation facilities. The photograph comes directly from that account and shows the rapid enclosures under construction. It is a historical construction view, not current operating capacity.",
      "SemiAnalysis identifies these lightweight, fabric-clad structures at New Albany, Ohio. The construction lesson is to distinguish enclosing the racks from completing the facility: the prepared ground, electrical connections, heat rejection and commissioning still require coordinated site work. This slide makes no claim about the number of completed tents or present-day megawatts."
    ]
  },
  {
    id: "aws-houdini-prefab",
    label: "Amazon: factory-built data-hall sections",
    title: "Amazon’s Project Houdini moves data-hall assembly into factories.",
    pedagogical_role: "case-study",
    reference: "d12-hazards-and-site-evidence",
    sources: [SEMIANALYSIS, CEI],
    explanation: [
      "SemiAnalysis’s July 29, 2026 report describes Project Houdini as AWS’s prefabricated data-hall skid program and names Cupertino Electric as a partner. This is a factory-assembly case; the report does not establish that Amazon uses Meta’s fabric tent design.",
      "The photograph is Cupertino Electric’s own Edgerton, Wisconsin factory image. It illustrates the partner’s modular production environment, not an identified Houdini unit or an AWS project at Edgerton. CEI describes factory assembly and testing followed by delivery, installation and field verification. The two parallel workstreams on this slide explain the scheduling mechanism: the site can be prepared while sections are assembled elsewhere, then the interfaces and complete system are tested on site."
    ]
  }
];

const photo = (file, alt, credit) => `<figure class="rapid-build-photo"><img src="../assets/references/${file}" alt="${alt}"><figcaption>${credit}</figcaption></figure>`;
const detail = (heading, text) => `<div><h2>${heading}</h2><p>${text}</p></div>`;
const result = (markup, description) => ({ markup, description, format: "html" });

export function renderRapidBuildCase(id) {
  if (id === "meta-prometheus-tents") return result(
    `<div class="rapid-build-case">${photo("meta-prometheus-tents-construction.png", "Meta’s Prometheus construction photograph shows long weatherproof tent halls, with unfinished ground and equipment installation around them.", "Prometheus · New Albany, Ohio · Meta, published Sep 2025")}<div class="rapid-build-points">${detail("Fast enclosure", "Lightweight frame + fabric")}${detail("Site work", "Foundations, power and cooling")}${detail("Ready to operate", "Connect and commission")}</div></div>`,
    "Meta used weatherproof tent enclosures for part of Prometheus. The actual construction photograph shows the shell standing while work continues around it. Foundations, power, cooling and commissioning remain part of completing the facility."
  );
  if (id === "aws-houdini-prefab") return result(
    `<div class="rapid-build-case">${photo("cei-modular-factory-edgerton.jpg", "Cupertino Electric’s Edgerton factory, with electrical equipment and large infrastructure assemblies arranged in production areas.", "Cupertino Electric’s modular factory · Edgerton, Wisconsin")}<div class="rapid-build-points rapid-build-parallel">${detail("In the factory", "Assemble and test data-hall sections")}${detail("In parallel, on site", "Prepare foundations, enclosure and utilities")}${detail("At installation", "Connect sections and test the whole system")}</div></div>`,
    "Amazon’s Project Houdini moves data-hall assembly into factories. The image shows partner Cupertino Electric’s modular factory, not a specifically identified Amazon unit. Factory work and site preparation can proceed in parallel before the complete installation is connected and tested."
  );
  return null;
}
