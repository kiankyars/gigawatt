// Generated from teaching-sequences.json and domain-map.json.
// Run uv run gigawatt-expand; chapter numbering follows the curriculum order.
export const presentationLabels = Object.freeze({
  "primer": "1. Primer",
  "overview": "2. Data center overview",
  "workloads": "3. Workloads and requirements",
  "siting": "4. Siting, grid connection and supply",
  "physical-site": "5. Physical site, buildings and safety",
  "distribution": "6. Campus and building power distribution",
  "continuity": "7. Continuity, storage and protection",
  "rack-energy": "8. Rack power and the 800 V DC transition",
  "networking": "9. Networking and interconnects",
  "storage": "10. Storage, orchestration and recovery",
  "cooling": "11–12. From the chip to the outdoors",
  "procurement-cases": "13. Modular construction"
});
export const presentationRoutes = Object.freeze([
  {
    "path": "terminology-format.html",
    "next": {
      "number": 2,
      "title": "Data center overview",
      "href": "orientation-format.html?teach=1",
      "kind": "slides"
    }
  },
  {
    "path": "orientation-format.html",
    "next": {
      "number": 3,
      "title": "Workloads and requirements",
      "href": "workload-format.html?teach=1",
      "kind": "slides"
    }
  },
  {
    "path": "workload-format.html",
    "next": {
      "number": 4,
      "title": "Siting, grid connection and supply",
      "href": "siting-format.html?teach=1",
      "kind": "slides"
    }
  },
  {
    "path": "siting-format.html",
    "next": {
      "number": 5,
      "title": "Physical site, buildings and safety",
      "href": "site-format.html?teach=1",
      "kind": "slides"
    }
  },
  {
    "path": "site-format.html",
    "next": {
      "number": 6,
      "title": "Campus and building power distribution",
      "href": "distribution-format.html?teach=1",
      "kind": "slides"
    }
  },
  {
    "path": "distribution-format.html",
    "next": {
      "number": 7,
      "title": "Continuity, storage and protection",
      "href": "continuity-format.html?teach=1",
      "kind": "slides"
    }
  },
  {
    "path": "continuity-format.html",
    "next": {
      "number": 8,
      "title": "Rack power and the 800 V DC transition",
      "href": "rack-energy-format.html?teach=1",
      "kind": "slides"
    }
  },
  {
    "path": "rack-energy-format.html",
    "next": {
      "number": 9,
      "title": "Networking and interconnects",
      "href": "networking-format.html?teach=1",
      "kind": "slides"
    }
  },
  {
    "path": "networking-format.html",
    "next": {
      "number": 10,
      "title": "Storage, orchestration and recovery",
      "href": "storage-format.html?teach=1",
      "kind": "slides"
    }
  },
  {
    "path": "storage-format.html",
    "next": {
      "number": 11,
      "title": "Chip and rack heat capture",
      "href": "cooling-format.html?teach=1",
      "kind": "slides"
    }
  },
  {
    "path": "cooling-format.html",
    "next": {
      "number": 13,
      "title": "Design, procurement and commissioning",
      "href": "procurement-cases-format.html?teach=1#aws-houdini-prefab",
      "kind": "slides"
    }
  },
  {
    "path": "procurement-cases-format.html",
    "next": {
      "number": 14,
      "title": "Controls, operations and reliability",
      "href": "../index.html#d14-telemetry-and-observability",
      "kind": "reading"
    }
  }
]);
