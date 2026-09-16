const node = (content, className = '') => `<li class="dc-bus-node ${className}">${content}</li>`;

export function renderRackBusChoices() {
  return `<div class="dc-bus-choices">
    <section class="dc-bus-choice" aria-label="Step down at the rack entrance">
      <h2>Step down at the rack entrance</h2>
      <ol class="dc-bus-path">
        ${node('<strong>800 V DC</strong><span>Rack input</span>', 'dc-bus-input')}
        ${node('<strong>DC/DC</strong><span>Rack-entry converter</span>', 'dc-bus-converter')}
        ${node('<strong>~50 V</strong><span>Vertical busbar</span>', 'dc-bus-bar dc-bus-low')}
        ${node('<strong>Device conversion</strong><span>At the tray / board</span>', 'dc-bus-converter')}
        ${node('<strong>Device rails</strong><span>Chip voltage</span>', 'dc-bus-chip')}
      </ol>
    </section>
    <section class="dc-bus-choice" aria-label="Carry 800 volts down the rack and step down at the trays">
      <h2>Step down at the trays</h2>
      <ol class="dc-bus-path">
        ${node('<strong>800 V DC</strong><span>Rack input</span>', 'dc-bus-input')}
        ${node('<strong>800 V</strong><span>Vertical busbar</span>', 'dc-bus-bar dc-bus-high')}
        ${node('<strong>DC/DC</strong><span>Tray converter</span>', 'dc-bus-converter')}
        ${node('<strong>VRM</strong><span>Local regulation</span>', 'dc-bus-converter')}
        ${node('<strong>Device rails</strong><span>Chip voltage</span>', 'dc-bus-chip')}
      </ol>
    </section>
  </div>`;
}

export function renderDCChanges() {
  return `<div class="dc-hall-changes">
    <div class="dc-hall-comparison">
      <section class="dc-hall-column" aria-label="AC distribution in the data hall">
        <h2>AC in the data hall</h2>
        <div class="dc-hall-change"><h3>Power conversion</h3><p>AC → DC at the rack<br>DC → DC near the load</p></div>
        <div class="dc-hall-change"><h3>Rack space</h3><p>Power shelves inside the compute rack</p></div>
        <div class="dc-hall-change"><h3>Protection &amp; backup</h3><p>AC-rated protection<br>UPS and battery interfaces</p></div>
      </section>
      <section class="dc-hall-column dc-hall-column-dc" aria-label="800 volt DC distribution in the data hall">
        <h2>800 V DC in the data hall</h2>
        <div class="dc-hall-change"><h3>Power conversion</h3><p>AC → DC upstream<br>DC → DC near the load</p></div>
        <div class="dc-hall-change"><h3>Rack space</h3><p>AC/DC equipment moves to the power room</p></div>
        <div class="dc-hall-change"><h3>Protection &amp; backup</h3><p>DC-rated protection<br>Adapted backup interfaces</p></div>
      </section>
    </div>
    <p class="dc-path-efficiency">Compare losses across the full path.</p>
  </div>`;
}
