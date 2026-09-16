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
