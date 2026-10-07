import * as THREE from './vendor/three-0.180.0/three.module.min.js';

const TURN = Math.PI * 2;
const FLOW_SPEED = 2.2; // world units per second
const AMBIENT_FRAME_MS = 1000 / 30;
const UP = new THREE.Vector3(0, 1, 0);

// Camera stops, one per chapter. The orbit pivots on the subject; app.js supplies the
// free screen area, and the camera's view offset centres the subject inside it.
const STOPS = [
  { x: 0, z: 14, zoom: 1, angle: 0.42, elevation: 36 },
  { x: -9.5, z: -1.6, zoom: 2, angle: 0.9, elevation: 29 },
  { x: 1, z: 0, zoom: 2, angle: 0.5, elevation: 27 },
  { x: 4, z: -8, zoom: 2.15, angle: 1.03, elevation: 32 },
  { x: 8, z: 7.5, zoom: 2.35, angle: 0.72, elevation: 27 },
  { x: -5, z: 8, zoom: 2.7, angle: 0.34, elevation: 26 },
];

// Part label anchors inside the open server.
// Label anchors for equipment whose parts are spread out, or that is labelled on one
// example (one rack, one server, one aisle). Labels hang above their anchor.
const ITEM_ANCHORS = {
  utility: [-20, 0.9, -10],
  generator: [-10, 3.58, 3.6],
  ats: [-8.1, 2.25, -1.8],
  pdu: [-4, 4.05, -3.7],
  rack: [-3.8, 3.45, 3.6],
  server: [-1.75, 1.75, 4.45],
  leaf: [4.4, 2.95, 4.45],
  'rack-pdu': [0.82, 2.95, 4.4],
  'cold-aisle': [-2.6, 0.75, 5.05],
  'hot-aisle': [5.7, 0.75, 1.78],
  'facility-loop': [6, 0.95, -7.05],
  fiber: [10.8, 1.6, 8.5],
  'cable-tray': [6.1, 4.35, 3.25],
  technician: [-3.7, 2.1, 9],
};
// Meshes tagged with these ids select another item: a server in a rack opens the open server.
const PICK_ALIASES = { 'rack-server': 'server' };
const SERVER_ORIGIN = new THREE.Vector3(38, 0, -4);
const PART_ANCHORS = {
  cpu: [-3.2, 2, -1.2],
  gpu: [3, 2.3, -0.4],
  memory: [-6.3, 1.9, -1.2],
  storage: [-4, 1.7, 3.5],
  nic: [6.1, 1.8, -3.9],
  'cold-plate': [2.95, 1.6, -4.6],
  psu: [-5.7, 1.8, -3.9],
  fans: [3.3, 2.1, 3.45],
};

// Animated paths for "Follow the …". Standby lines are drawn dim and carry no packets.
const PATHS = {
  power: [
    {
      color: '#fff0a6',
      points: [
        [-20, 0.3, -18],
        [-20, 0.3, -6],
        [-11.45, 0.3, -6],
        [-11.45, 2.9, -6],
        [-10, 2.9, -6.6],
        [-10, 2.9, -1.8],
        [-5.4, 2.9, -1],
        [-5.4, 3.95, -3.3],
        [4.4, 3.95, -3.3],
        [4.4, 3.95, -2.75],
        [4.4, 1.6, -2.75],
      ],
    },
    {
      color: '#9c7f25',
      standby: true,
      points: [
        [-10, 2.05, 3.6],
        [-10, 2.6, 3.6],
        [-8.1, 2.6, 1],
        [-8.1, 2.6, -1.8],
        [-8.1, 1.8, -1.8],
      ],
    },
  ],
  cooling: [
    // IT loop: warm return from the rack to the CDU.
    {
      color: '#ff8a3d',
      points: [
        [2.35, 3.3, -3.7],
        [2.35, 3.3, -4.75],
        [1.3, 2.6, -5.3],
      ],
    },
    // Facility loop: heat from the CDU to the dry cooler, then into the outdoor air.
    {
      color: '#ff8a3d',
      points: [
        [1.3, 2.6, -5.6],
        [1.3, 2.6, -6.9],
        [4, 2.6, -6.9],
        [4, 2.6, -9],
        [4, 4.7, -9],
      ],
    },
    // Facility loop: cooled supply back to the CDU.
    {
      color: '#41b9ef',
      points: [
        [3.2, 1.6, -7.1],
        [0.9, 1.6, -7.1],
        [0.9, 1.6, -5.75],
      ],
    },
    // IT loop: cooled supply from the CDU to the rack.
    {
      color: '#41b9ef',
      points: [
        [0.7, 2.2, -4.85],
        [0.7, 3.25, -4.6],
        [0.7, 3.25, -2.75],
        [0.7, 1.8, -2.75],
      ],
    },
    // Room air: hot aisle to the air handler, then cooled air into the cold aisle.
    {
      color: '#ffb27a',
      points: [
        [0.3, 3.2, 1.78],
        [7.6, 3.2, 1.78],
        [8.2, 2.2, -0.5],
      ],
    },
    {
      color: '#9fdcf5',
      points: [
        [8.15, 1.2, -1.5],
        [7.6, 0.6, -1.88],
        [-3.8, 0.6, -1.88],
      ],
    },
  ],
  network: [
    // North–south: from the fiber entrance through the spine to a server.
    {
      color: '#ee6252',
      points: [
        [12.5, 0.4, 11.8],
        [12.5, 0.4, 9.3],
        [7.2, 3.1, 9.3],
        [7.2, 4.1, 3.25],
        [-3.8, 4.1, 3.25],
        [-3.8, 4.1, 4.55],
        [-3.8, 1.4, 4.55],
      ],
    },
    // East–west: from one server, up through the spine, down to a server in another row.
    {
      color: '#ffa0b4',
      points: [
        [0.3, 1.4, 4.55],
        [0.3, 4.6, 4.55],
        [0.3, 4.6, 3],
        [5.4, 4.6, 3],
        [5.4, 4.6, 8.4],
        [5.4, 2.75, 8.4],
        [8.9, 2.75, 8.4],
        [8.9, 4.6, 8.4],
        [8.9, 4.6, -0.4],
        [2.35, 4.6, -0.4],
        [2.35, 4.6, -1],
        [2.35, 1.4, -1],
      ],
    },
  ],
};

// 5×7 voxel glyphs for the ground lettering.
const GLYPHS = {
  A: ['01110', '11011', '11011', '11111', '11011', '11011', '11011'],
  C: ['01111', '11000', '11000', '11000', '11000', '11000', '01111'],
  D: ['11110', '11011', '11011', '11011', '11011', '11011', '11110'],
  E: ['11111', '11000', '11000', '11110', '11000', '11000', '11111'],
  G: ['01111', '11000', '11000', '11011', '11011', '11011', '01111'],
  I: ['11111', '00100', '00100', '00100', '00100', '00100', '11111'],
  K: ['11011', '11011', '11110', '11100', '11110', '11011', '11011'],
  L: ['11000', '11000', '11000', '11000', '11000', '11000', '11111'],
  M: ['10001', '11011', '11111', '10101', '10101', '10001', '10001'],
  N: ['10001', '11001', '11101', '11111', '10111', '10011', '10001'],
  O: ['01110', '11011', '11011', '11011', '11011', '11011', '01110'],
  P: ['11110', '11011', '11011', '11110', '11000', '11000', '11000'],
  R: ['11110', '11011', '11011', '11110', '11100', '11010', '11011'],
  S: ['01111', '11000', '11000', '01110', '00011', '00011', '11110'],
  T: ['11111', '00100', '00100', '00100', '00100', '00100', '00100'],
  U: ['11011', '11011', '11011', '11011', '11011', '11011', '01110'],
  V: ['11011', '11011', '11011', '11011', '01010', '01010', '00100'],
  W: ['10001', '10001', '10101', '10101', '11111', '11011', '10001'],
};

const lerp = THREE.MathUtils.lerp;
const clamp = THREE.MathUtils.clamp;

/**
 * Builds the voxel landscape inside `container` and returns its controller, or null
 * when WebGL is unavailable. All labels, colours and chapter structure come from
 * `options`, so the world holds geometry only.
 */
export function createWorld(container, options = {}) {
  const {
    onSelect = () => {},
    onEmptyClick = () => {},
    onReady = () => {},
    onHotspotHidden = () => {},
    hotspotLayer = container,
    tooltip = null,
    chapterIds = [],
    labelsByChapter = {},
    itemLabels = {},
    itemChapter = {},
    colors = {},
    names = {},
    serverParts = [],
  } = options;
  if (chapterIds.length !== STOPS.length) throw new Error(`The world has ${STOPS.length} camera stops.`);

  const deviceRatio = () => Math.min(window.devicePixelRatio || 1, 2);
  // The backing store is capped near 4.2 megapixels so large displays stay affordable.
  const pixelRatio = (w, h) => Math.min(deviceRatio(), Math.sqrt(4.2e6 / Math.max(1, w * h)));
  let renderer;
  try {
    // When the canvas renders at a high pixel ratio, the extra resolution already hides
    // aliasing, so MSAA is skipped.
    renderer = new THREE.WebGLRenderer({
      antialias: pixelRatio(innerWidth, innerHeight) < 1.5,
      alpha: false,
      powerPreference: 'low-power',
    });
  } catch {
    return null;
  }
  renderer.setClearColor(0x080808, 1);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const canvas = renderer.domElement;
  canvas.setAttribute('aria-hidden', 'true');
  container.prepend(canvas);

  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-20, 20, 20, -20, 0.1, 180);
  scene.add(new THREE.AmbientLight(0xffffff, 1.1));
  const light = new THREE.DirectionalLight(0xffffff, 2.1);
  light.position.set(-12, 24, 16);
  scene.add(light);
  const fill = new THREE.DirectionalLight(0xbecbdf, 0.45);
  fill.position.set(18, 8, -10);
  scene.add(fill);

  const root = new THREE.Group();
  const serverRoot = new THREE.Group();
  serverRoot.position.copy(SERVER_ORIGIN);
  scene.add(root, serverRoot);

  // Static voxels are recorded as matrices and built into one InstancedMesh per
  // group, material and pick id. Animated groups (van, fans) get ordinary meshes.
  const UNIT = new THREE.BoxGeometry(1, 1, 1);
  const materials = new Map();
  const material = (color, unlit = false) => {
    const key = (unlit ? 'b' : 'l') + color;
    if (!materials.has(key)) {
      materials.set(key, unlit ? new THREE.MeshBasicMaterial({ color }) : new THREE.MeshLambertMaterial({ color }));
    }
    return materials.get(key);
  };
  const batches = new Map();
  const pickables = [];
  const nodeMeshes = new Map();
  const dummy = new THREE.Object3D();

  function addVoxel(group, mat, node, matrix) {
    if (group !== root && group !== serverRoot && !group.userData.batch) {
      const mesh = new THREE.Mesh(UNIT, mat);
      matrix.decompose(mesh.position, mesh.quaternion, mesh.scale);
      group.add(mesh);
      return;
    }
    const key = `${group.uuid}|${mat.uuid}|${node || ''}`;
    if (!batches.has(key)) batches.set(key, { group, mat, node, matrices: [] });
    batches.get(key).matrices.push(matrix);
  }

  function box(x, y, z, w, h, d, color, node = null, group = root) {
    dummy.position.set(x, y + h / 2, z);
    dummy.quaternion.identity();
    dummy.scale.set(w, h, d);
    dummy.updateMatrix();
    addVoxel(group, material(color), node, dummy.matrix.clone());
  }

  function line(points, color, width = 0.055, group = root, node = null) {
    for (let i = 1; i < points.length; i++) {
      const a = new THREE.Vector3(...points[i - 1]);
      const b = new THREE.Vector3(...points[i]);
      dummy.position.copy(a).add(b).multiplyScalar(0.5);
      dummy.scale.set(width, width, a.distanceTo(b));
      dummy.up.copy(UP);
      dummy.lookAt(b);
      dummy.updateMatrix();
      addVoxel(group, material(color, true), node, dummy.matrix.clone());
    }
  }

  // ── Site and data hall ──────────────────────────────────────────────────────
  // A cutaway facility makes infrastructure paths visible without hiding the servers.
  box(0, -0.9, 0, 28, 0.7, 24, '#161616');
  box(0, -0.2, 0, 27.7, 0.15, 23.7, '#242424');
  for (let x = -13; x <= 13; x++)
    line(
      [
        [x, -0.025, -11.8],
        [x, -0.025, 11.8],
      ],
      '#383838',
      0.014,
    );
  for (let z = -11; z <= 11; z++)
    line(
      [
        [-13.8, -0.025, z],
        [13.8, -0.025, z],
      ],
      '#383838',
      0.014,
    );
  box(1, 0, 0, 15, 0.25, 13, '#424242');
  box(1, 0.25, 0, 14.5, 0.08, 12.5, '#555555');
  // Low walls and columns imply the hall while keeping a continuous cutaway.
  box(1, 0.33, -6.2, 14.8, 1.1, 0.22, '#9b9b9b');
  box(-6.3, 0.33, 0, 0.22, 1.1, 12.5, '#9b9b9b');
  for (const x of [-6.25, 8.25]) for (const z of [-6.2, 6.2]) box(x, 0.33, z, 0.22, 3.9, 0.22, '#bdbdbd');
  for (const x of [-6.25, 8.25]) box(x, 4.23, 0, 0.22, 0.18, 12.6, '#858585');
  box(1, 4.23, -6.2, 14.7, 0.18, 0.22, '#858585');

  // Rows alternate direction: fronts share the cold aisles, backs share the hot aisle.
  for (let r = 0; r < 3; r++) {
    for (let n = 0; n < 5; n++) {
      const x = -3.8 + n * 2.05;
      const z = -3.7 + r * 3.65;
      const f = r === 1 ? -1 : 1;
      box(x, 0.34, z, 1.25, 2.65, 1.35, '#1a1a1a', 'rack');
      box(x, 0.35, z + f * 0.69, 1.14, 2.53, 0.06, '#080808', 'rack');
      box(x, 2.99, z, 1.29, 0.08, 1.4, '#525252', 'rack');
      for (let s = 0; s < 6; s++) {
        box(x, 0.55 + s * 0.3, z + f * 0.738, 1.03, 0.19, 0.035, '#3c3c3c', 'rack-server');
        box(
          x - 0.35,
          0.6 + s * 0.3,
          z + f * 0.763,
          0.065,
          0.045,
          0.025,
          s % 3 === 0 ? '#f7ce46' : '#32bb43',
          'rack-server',
        );
        box(x + 0.2, 0.59 + s * 0.3, z + f * 0.762, 0.32, 0.02, 0.025, '#101710', 'rack-server');
      }
      // The top unit is the rack's leaf switch.
      box(x, 0.55 + 6 * 0.3, z + f * 0.738, 1.03, 0.19, 0.035, '#64504c', 'leaf');
      for (let k = 0; k < 4; k++)
        box(x - 0.38 + k * 0.23, 0.62 + 6 * 0.3, z + f * 0.763, 0.08, 0.05, 0.02, '#f2693c', 'leaf');
      box(x + 0.52, 0.45, z + f * 0.73, 0.055, 2.35, 0.045, '#777777', 'rack-pdu');
      // Rear exhaust grille.
      for (let g = 0; g < 4; g++) box(x, 0.7 + g * 0.5, z - f * 0.69, 1, 0.08, 0.04, '#2e2e2e', 'rack');
    }
  }
  box(1, 0.34, -1.88, 12, 0.018, 0.8, '#256e94', 'cold-aisle');
  box(1, 0.34, 1.78, 12, 0.018, 0.8, '#8a4a1c', 'hot-aisle');
  box(1, 0.34, 5.05, 12, 0.018, 0.8, '#256e94', 'cold-aisle');

  // Overhead power busways (yellow) and network trays (red).
  for (const z of [-3.7, -0.05, 3.6]) {
    box(0.3, 3.5, z, 12.5, 0.13, 0.22, '#eccc37', 'pdu');
    box(0.3, 3.75, z - 0.35, 12.5, 0.14, 0.25, '#bb392b', 'cable-tray');
  }

  // ── Power yard ──────────────────────────────────────────────────────────────
  box(-10, 0, -4, 4.8, 0.2, 7.2, '#555555', 'power');
  box(-10, 0.2, -5.3, 2.55, 1.75, 2.3, '#777777', 'transformer');
  for (let x = -11.2; x <= -8.8; x += 0.3) box(x, 0.35, -4.09, 0.12, 1.35, 0.16, '#aaaaaa', 'transformer');
  for (const x of [-10.65, -10, -9.35]) {
    box(x, 1.95, -5.3, 0.16, 0.7, 0.16, '#cccccc', 'transformer');
    box(x, 2.37, -5.3, 0.4, 0.1, 0.4, '#8a8a8a', 'transformer');
  }
  for (let i = 0; i < 3; i++) {
    const x = -11.35 + i * 1.13;
    box(x, 0.2, -1.8, 0.95, 2.3, 1.3, '#8d8d8d', 'switchgear');
    box(x, 1.35, -1.125, 0.43, 0.55, 0.035, '#1f1f1f', 'switchgear');
    box(x, 2.13, -1.115, 0.06, 0.06, 0.03, '#f7ce46', 'switchgear');
  }
  // The transfer switch lets the standby generator take over the load.
  box(-8.1, 0.2, -1.8, 0.6, 1.6, 0.9, '#8d8d8d', 'ats');
  box(-8.1, 1.15, -1.33, 0.3, 0.3, 0.03, '#1f1f1f', 'ats');
  box(-10, 0, 3.6, 4.8, 0.2, 4.6, '#555555', 'generator');
  box(-10, 0.2, 3.6, 3.7, 1.85, 2.5, '#dcbe37', 'generator');
  for (let i = 0; i < 7; i++) box(-10.9 + i * 0.28, 0.5, 4.87, 0.1, 1.22, 0.06, '#595137', 'generator');
  box(-8.75, 1.9, 3.1, 0.18, 1.3, 0.18, '#777777', 'generator');
  box(-8.9, 3.08, 3.1, 0.5, 0.15, 0.25, '#555555', 'generator');
  line(
    [
      [-9.2, 0.26, 2.35],
      [-8.1, 0.26, 2.35],
      [-8.1, 0.26, -1.35],
    ],
    '#8a7a3a',
    0.1,
  ); // standby feeder
  for (let i = 0; i < 2; i++) {
    box(-5.4, 0.34, -3 + i * 2, 1.05, 2.2, 1.4, '#656565', 'ups');
    for (let j = 0; j < 4; j++) box(-5.4, 0.55 + j * 0.43, -2.28 + i * 2, 0.8, 0.25, 0.03, '#9d9d9d', 'ups');
  }

  // ── Cooling plant ───────────────────────────────────────────────────────────
  for (let i = 0; i < 3; i++) {
    const x = -0.2 + i * 4;
    box(x, 0, -9, 3.5, 0.25, 3.5, '#666666', 'cooling');
    box(x, 0.25, -9, 3.25, 1.65, 3.15, '#999999', 'heat-rejection');
    box(x, 1.9, -9, 3.28, 0.12, 3.18, '#b8b8b8', 'heat-rejection');
    for (const dz of [-0.72, 0.72]) {
      box(x, 2.02, -9 + dz, 1.32, 0.12, 1.17, '#282828', 'heat-rejection');
      box(x, 2.15, -9 + dz, 1.09, 0.045, 0.2, '#666666', 'heat-rejection');
      box(x, 2.15, -9 + dz, 0.2, 0.045, 0.99, '#666666', 'heat-rejection');
    }
    for (let j = 0; j < 6; j++) box(x - 1.64, 0.42 + j * 0.21, -9, 0.035, 0.08, 2.8, '#525252', 'heat-rejection');
  }
  for (const x of [1, 5]) {
    box(x, 0.34, -5.3, 1.3, 1.75, 0.8, '#278aba', 'cdu');
    box(x, 1.4, -4.88, 0.62, 0.32, 0.03, '#163540', 'cdu');
  }
  // Facility water loop: warm return (orange) and cooled supply (blue) between the CDUs and the dry coolers.
  for (const [dx, y, z, color] of [
    [0.25, 0.55, -6.95, '#c9662f'],
    [-0.25, 0.4, -7.2, '#2f86c9'],
  ]) {
    for (const x of [1, 5])
      line(
        [
          [x + dx, y, -5.7],
          [x + dx, y, z],
        ],
        color,
        0.12,
        root,
        'facility-loop',
      );
    line(
      [
        [-0.2 + dx, y, z],
        [7.8 + dx, y, z],
      ],
      color,
      0.12,
      root,
      'facility-loop',
    );
    for (const x of [-0.2, 3.8, 7.8])
      line(
        [
          [x + dx, y, z],
          [x + dx, y, -7.42],
        ],
        color,
        0.12,
        root,
        'facility-loop',
      );
  }
  box(8.8, 0, -0.5, 1.25, 2.4, 4, '#aaaaaa', 'air-handler');
  for (let i = 0; i < 9; i++) box(8.8, 0.45 + i * 0.2, 1.52, 1.03, 0.07, 0.05, '#505050', 'air-handler');

  // ── Network yard: two separate fiber entrances and the spine switches ─────
  box(7.2, 0, 8.4, 6.3, 0.2, 3.8, '#555555', 'network');
  for (let i = 0; i < 3; i++) {
    box(5.4 + i * 1.75, 0.2, 8.4, 1.3, 2.35, 1.4, '#353535', 'switch');
    for (let j = 0; j < 6; j++) {
      box(5.4 + i * 1.75, 0.43 + j * 0.32, 9.12, 1.1, 0.21, 0.04, '#64504c', 'switch');
      for (let k = 0; k < 4; k++)
        box(5.02 + i * 1.75 + k * 0.23, 0.5 + j * 0.32, 9.15, 0.08, 0.05, 0.02, '#f2693c', 'switch');
    }
  }
  box(10.8, 0, 8.5, 1.1, 1.2, 0.8, '#bc6d59', 'fiber');
  box(4.6, 0, 11.3, 0.5, 0.35, 0.5, '#bc6d59', 'fiber');
  line(
    [
      [12.5, 0.17, 11.9],
      [12.5, 0.17, 8.4],
      [9.5, 0.17, 8.4],
    ],
    '#ee6252',
    0.12,
  );
  line(
    [
      [4.6, 0.17, 11.9],
      [4.6, 0.17, 10.2],
      [5.4, 0.17, 10.2],
    ],
    '#ee6252',
    0.12,
  );

  // ── Operations, access gate and small pixel people ──────────────────────────
  box(-4.5, 0, 8.5, 5.6, 0.2, 3.5, '#555555', 'operations');
  box(-4.5, 0.2, 7.1, 5.6, 1.7, 0.2, '#888888', 'operations');
  box(-6.6, 0.2, 8.45, 0.18, 1.7, 2.6, '#888888', 'operations');
  box(-4.5, 0.2, 7.8, 3.8, 1.1, 0.8, '#555555', 'monitoring');
  for (let i = 0; i < 3; i++) {
    box(-5.65 + i * 1.12, 1.3, 7.85, 0.89, 0.68, 0.09, '#202e24', 'monitoring');
    box(-5.65 + i * 1.12, 1.4, 7.9, 0.74, 0.48, 0.035, '#278fb9', 'monitoring');
  }
  box(-2.3, 0, 11, 0.15, 1.5, 0.15, '#999999', 'security');
  box(-5.8, 0, 11, 0.15, 1.5, 0.15, '#999999', 'security');
  box(-4.05, 1.3, 11, 3.5, 0.13, 0.13, '#dddddd', 'security');
  for (let i = 0; i < 5; i++) box(-5.3 + i * 0.62, 1.29, 11.08, 0.3, 0.15, 0.03, '#e0604a', 'security');
  box(-6.1, 0.34, 5.1, 0.15, 1, 0.4, '#d85349', 'fire');

  function person(x, z, color) {
    box(x, 0, z, 0.35, 0.55, 0.28, '#36483b', 'technician');
    box(x, 0.55, z, 0.55, 0.57, 0.3, color, 'technician');
    box(x, 1.12, z, 0.37, 0.37, 0.36, '#d9b791', 'technician');
    box(x, 1.45, z, 0.43, 0.12, 0.4, '#e5d36e', 'technician');
  }
  person(-3.7, 9, '#b5a1cb');
  person(5.7, 5.4, '#609abb');
  person(-9.2, 7, '#e17a55');

  function tree(x, z, size = 1) {
    box(x, 0, z, 0.25, 1, 0.25, '#726447');
    box(x, 0.75, z, 1.4 * size, 1.1 * size, 1.4 * size, '#1b7032');
    box(x, 1.4, z, 1 * size, 0.95 * size, 1 * size, '#279340');
    box(x, 2.1, z, 0.45 * size, 0.45 * size, 0.45 * size, '#3cad42');
  }
  for (const [x, z] of [
    [-12.7, 9.5],
    [-13.3, -6.2],
    [12.6, -9.5],
    [12.8, 3.5],
    [11.8, 10.2],
    [-0.2, 11.1],
  ])
    tree(x, z, 0.8);
  for (let i = 0; i < 12; i++) box(-11.5 + i * 1.8, 0.01, 11.6, 0.55, 0.06, 0.18, '#258e32');

  // ── Server chassis, drawn at its own scale beside the facility ─────────────
  const sb = (x, y, z, w, h, d, color, id) => box(x, y, z, w, h, d, color, id, serverRoot);
  sb(0, 0, 0, 16, 0.3, 10, '#788680', 'server');
  sb(0, 0.3, -4.9, 16, 1.5, 0.2, '#aeb9b0', 'server');
  sb(-7.9, 0.3, 0, 0.2, 1.2, 10, '#aeb9b0', 'server');
  sb(7.9, 0.3, 0, 0.2, 1.2, 10, '#8a9990', 'server');
  sb(0, 0.3, 0, 15, 0.1, 9, '#234d37', 'server');
  // The CPU keeps a finned air heatsink.
  sb(-3.2, 0.4, -1.2, 3, 0.25, 3, '#aeb3a6', 'cpu');
  sb(-3.2, 0.65, -1.2, 2.3, 0.15, 2.3, '#424844', 'cpu');
  for (let i = 0; i < 9; i++) sb(-4.2 + i * 0.25, 0.8, -1.2, 0.12, 0.65, 2.25, '#bbc5b9', 'cpu');
  for (let i = 0; i < 4; i++) {
    sb(-6.45 + i * 0.48, 0.4, -1.2, 0.17, 0.85, 3, '#448259', 'memory');
    for (let j = 0; j < 5; j++) sb(-6.34 + i * 0.48, 0.63, -2.36 + j * 0.52, 0.06, 0.42, 0.35, '#151e18', 'memory');
  }
  // The GPUs are liquid-cooled: a cold plate on each, with supply and return tubes to a rear manifold.
  for (let i = 0; i < 3; i++) {
    const x = 0.8 + i * 2.15;
    sb(x, 0.4, -0.4, 1.6, 0.45, 5.4, '#547a9f', 'gpu');
    sb(x, 0.85, -0.9, 1.2, 0.2, 1.6, '#6cb4c1', 'cold-plate');
    sb(x, 1.05, -0.9, 0.8, 0.08, 1.1, '#9cd6de', 'cold-plate');
    sb(x - 0.25, 1.05, -3.15, 0.12, 0.12, 2.9, '#41b9ef', 'cold-plate');
    sb(x + 0.25, 1.05, -3.15, 0.12, 0.12, 2.9, '#ff8a3d', 'cold-plate');
  }
  sb(3, 1.1, -4.6, 6, 0.15, 0.15, '#6cb4c1', 'cold-plate');
  for (let i = 0; i < 4; i++) {
    sb(-5.7 + i * 1.5, 0.4, 3.5, 1.2, 0.6, 1.8, '#cba94d', 'storage');
    sb(-5.7 + i * 1.5, 0.55, 4.43, 0.86, 0.24, 0.03, '#393c29', 'storage');
  }
  for (let i = 0; i < 3; i++) {
    sb(1.2 + i * 2.1, 0.4, 3.45, 1.5, 1.4, 1.5, '#536c62', 'fans');
    sb(1.2 + i * 2.1, 0.65, 4.23, 1.17, 0.93, 0.05, '#263e35', 'fans');
    sb(1.2 + i * 2.1, 1.03, 4.28, 0.8, 0.18, 0.04, '#759383', 'fans');
  }
  sb(-5.7, 0.4, -3.9, 3.4, 1.1, 1.5, '#9b9e85', 'psu');
  sb(6.1, 0.4, -3.9, 2.1, 0.6, 1.3, '#b36f55', 'nic');
  for (let i = 0; i < 3; i++) sb(5.4 + i * 0.5, 0.55, -4.59, 0.3, 0.25, 0.1, '#202d24', 'nic');

  // ── Lettering and landscape ─────────────────────────────────────────────────
  function voxelText(text, x, z, scale = 0.5, color = '#727272', accent = false, group = root) {
    let cursor = x;
    for (const char of text) {
      const rows = GLYPHS[char];
      if (rows) {
        rows.forEach((row, r) =>
          [...row].forEach((v, c) => {
            if (v !== '1') return;
            const signal = accent && (r * 17 + c * 3 + Math.round(cursor * 10)) % 31 === 0;
            const tint = signal ? ['#e83329', '#e0c82c', '#238cbf', '#228c39'][(c + r) % 4] : color;
            box(cursor + c * scale, 0.04, z + r * scale, scale * 0.93, scale * 0.5, scale * 0.93, tint, null, group);
          }),
        );
      }
      cursor += scale * 6;
    }
  }
  // The title belongs to the overview and each system's name to its own stop, so the
  // overview stays uncluttered. 'server' lettering shows while the open server is in focus.
  const words = {};
  const wordGroup = (key) => {
    if (!words[key]) {
      const g = new THREE.Group();
      g.userData.batch = true;
      g.userData.target = 0;
      g.scale.y = 0;
      g.visible = false;
      root.add(g);
      words[key] = g;
    }
    return words[key];
  };
  voxelText('DATA', -17, 15, 1, '#888888', true, wordGroup('overview'));
  voxelText('CENTER', -17, 24, 1, '#888888', true, wordGroup('overview'));
  voxelText('POWER', -21, -13, 0.38, '#c2ac34', false, wordGroup('power'));
  voxelText('COMPUTE', -1.6, 12.3, 0.21, '#53a957', false, wordGroup('compute'));
  voxelText('COOLING', -3, -16.6, 0.3, '#328abd', false, wordGroup('cooling'));
  voxelText('NETWORK', 8.4, 13, 0.29, '#ba4234', false, wordGroup('network'));
  voxelText('PEOPLE', -13, 12, 0.3, '#888888', false, wordGroup('operations'));
  voxelText('INSIDE', 26, -16.8, 0.4, '#888888', false, wordGroup('server'));
  voxelText('A SERVER', 26.5, -13.6, 0.3, '#888888', false, wordGroup('server'));

  const ground = new THREE.Mesh(new THREE.PlaneGeometry(170, 140), new THREE.MeshLambertMaterial({ color: '#080808' }));
  ground.rotation.x = -Math.PI / 2;
  ground.position.set(7, -0.1, 10);
  scene.add(ground);
  // Floor tiles are split into chunks so off-screen chunks are frustum-culled.
  {
    const tileGeometry = new THREE.BoxGeometry(0.22, 0.075, 0.22);
    const tileMaterial = new THREE.MeshLambertMaterial({ color: '#242424' });
    const m = new THREE.Matrix4();
    const [NX, NZ, CX, CZ] = [170, 135, 34, 27];
    for (let cx = 0; cx < NX; cx += CX) {
      for (let cz = 0; cz < NZ; cz += CZ) {
        const chunk = new THREE.InstancedMesh(tileGeometry, tileMaterial, CX * CZ);
        let i = 0;
        for (let x = cx; x < cx + CX; x++) {
          for (let z = cz; z < cz + CZ; z++)
            chunk.setMatrixAt(i++, m.makeTranslation((x - 85) * 0.8, 0.003, (z - 55) * 0.8));
        }
        chunk.computeBoundingSphere();
        chunk.matrixAutoUpdate = false;
        scene.add(chunk);
      }
    }
  }
  // Pixel groves create depth and frame the journey without a floating model plinth.
  for (let i = 0; i < 34; i++) {
    if (i === 4) continue; // keeps the POWER lettering clear
    tree(-31 + (i % 5) * 2.7, -10 + Math.floor(i / 5) * 5.5, 0.55 + (i % 3) * 0.16);
  }
  for (let i = 0; i < 24; i++) tree(17 + (i % 4) * 2.7, -21 + Math.floor(i / 4) * 4, 0.55 + (i % 3) * 0.16);
  for (let i = 0; i < 12; i++) tree(-25 + i * 4.8, 38 + ((i * 7) % 4), 0.7);
  for (let i = 0; i < 130; i++) {
    const x = ((i * 37) % 111) - 47;
    const z = ((i * 19) % 81) - 29;
    if (Math.abs(x) < 15 && Math.abs(z) < 13) continue;
    if (x > -23 && x < 22 && z > 14 && z < 33) continue;
    box(x, 0, z, 0.18, 0.13, 0.6, '#1f682c');
    box(x + 0.25, 0, z + 0.15, 0.18, 0.3, 0.18, '#278438');
  }
  for (let i = 0; i < 29; i++) {
    const x = ((i * 23) % 84) - 39;
    const z = ((i * 31) % 75) - 23;
    if (Math.abs(x) < 16 && Math.abs(z) < 13) continue;
    box(x, 0.1, z, 0.5, 0.5, 0.5, ['#d52c24', '#d5bb30', '#2586b2', '#278e39'][i % 4]);
  }
  // A utility corridor of transmission towers feeds the transformer yard.
  for (const z of [-18, -1, 17]) {
    const x = -20;
    line(
      [
        [x - 1.2, 0, z - 0.8],
        [x - 0.4, 8, z - 0.3],
        [x + 0.4, 8, z - 0.3],
        [x + 1.2, 0, z - 0.8],
      ],
      '#777777',
      0.13,
      root,
      'utility',
    );
    line(
      [
        [x - 1.2, 0, z + 0.8],
        [x - 0.4, 8, z + 0.3],
        [x + 0.4, 8, z + 0.3],
        [x + 1.2, 0, z + 0.8],
      ],
      '#777777',
      0.13,
      root,
      'utility',
    );
    for (let y = 0; y < 7; y += 1.4) {
      const w = 1.2 - y * 0.1;
      line(
        [
          [x - w, y, z + 0.7],
          [x + w - 0.14, y + 1.4, z + 0.6],
        ],
        '#666666',
        0.08,
        root,
        'utility',
      );
      line(
        [
          [x + w, y, z + 0.7],
          [x - w + 0.14, y + 1.4, z + 0.6],
        ],
        '#666666',
        0.08,
        root,
        'utility',
      );
    }
    box(x, 6.5, z, 5.4, 0.19, 0.25, '#888888', 'utility');
    box(x, 8, z, 3.5, 0.19, 0.25, '#999999', 'utility');
    for (const dx of [-2.4, 2.4]) box(x + dx, 6.1, z, 0.16, 0.4, 0.16, '#bfbfbf', 'utility');
  }
  for (const x of [-22.4, -17.6])
    line(
      [
        [x, 6.15, -18],
        [x, 5.2, -9.5],
        [x, 6.15, -1],
        [x, 5.2, 8],
        [x, 6.15, 17],
      ],
      '#787878',
      0.035,
      root,
      'utility',
    );
  line(
    [
      [-20, 0.2, -18],
      [-20, 0.2, -6],
      [-11.3, 0.2, -6],
    ],
    '#d4b931',
    0.1,
    root,
    'utility',
  );

  // ── Animated pieces ─────────────────────────────────────────────────────────
  // A service van drives the perimeter road. It starts on the road, so it is never
  // drawn inside the hall when motion is off.
  const van = new THREE.Group();
  van.position.set(14, 0, -26);
  root.add(van);
  box(0, 0.4, 0, 1.5, 1.4, 2.8, '#cb3027', null, van);
  box(0, 0.4, 1.8, 1.5, 1.1, 0.9, '#cb3027', null, van);
  box(0, 1.05, 2.27, 1.2, 0.35, 0.025, '#318eb8', null, van);
  for (const x of [-0.8, 0.8]) for (const z of [-0.7, 1.5]) box(x, 0.1, z, 0.25, 0.55, 0.6, '#292929', null, van);
  const fanGroups = [];
  for (const x of [-0.2, 3.8, 7.8]) {
    for (const z of [-9.72, -8.28]) {
      const f = new THREE.Group();
      f.position.set(x, 2.24, z);
      root.add(f);
      box(0, 0, 0, 1.05, 0.06, 0.14, '#a9a9a9', null, f);
      box(0, 0, 0, 0.14, 0.06, 1.05, '#a9a9a9', null, f);
      fanGroups.push(f);
    }
  }

  for (const b of batches.values()) {
    const inst = new THREE.InstancedMesh(UNIT, b.mat, b.matrices.length);
    b.matrices.forEach((m, i) => inst.setMatrixAt(i, m));
    inst.userData.node = b.node;
    inst.computeBoundingBox();
    inst.computeBoundingSphere();
    b.group.add(inst);
    if (b.node) {
      pickables.push(inst);
      if (!nodeMeshes.has(b.node)) nodeMeshes.set(b.node, []);
      nodeMeshes.get(b.node).push(inst);
    }
  }
  batches.clear();
  scene.updateMatrixWorld(true);
  for (const group of [root, serverRoot]) {
    for (const child of group.children) if (child.isInstancedMesh) child.matrixAutoUpdate = false;
  }
  const boundsCache = new Map();
  function boundsOf(id) {
    if (!boundsCache.has(id)) {
      const meshes = nodeMeshes.get(id);
      if (!meshes?.length) return null;
      const bounds = new THREE.Box3();
      meshes.forEach((m) => bounds.expandByObject(m));
      boundsCache.set(id, bounds);
    }
    return boundsCache.get(id);
  }

  // Selection outline drawn on the ground around the focused equipment.
  const halo = new THREE.Group();
  halo.visible = false;
  scene.add(halo);
  const haloMaterial = new THREE.MeshBasicMaterial({ color: 0xf7ce46 });
  for (const [x, z, w, d] of [
    [0, -1.15, 2.5, 0.045],
    [0, 1.15, 2.5, 0.045],
    [-1.25, 0, 0.045, 2.3],
    [1.25, 0, 0.045, 2.3],
  ]) {
    const m = new THREE.Mesh(UNIT, haloMaterial);
    m.position.set(x, 0.1, z);
    m.scale.set(w, 0.04, d);
    halo.add(m);
  }

  // ── State ───────────────────────────────────────────────────────────────────
  let progress = 0;
  let focusId = null;
  let selected = null;
  let needsRender = true;
  let paused = false;
  let reduced = false;
  let covered = false;
  let azimuth = STOPS[0].angle;
  let targetAzimuth = azimuth;
  let zoom = 1;
  let targetZoom = 1;
  let elevation = STOPS[0].elevation;
  let targetElevation = elevation;
  let orbit = 0;
  const target = new THREE.Vector3(STOPS[0].x, 0, STOPS[0].z);
  const lookAt = target.clone();
  let width = 1;
  let height = 1;
  let safe = null;
  let offX = 0;
  let offY = 0;
  let targetOffX = 0;
  let targetOffY = 0;
  let flowId = null;
  let flowGroup = null;
  let flowPackets = [];
  let flowTime = 0;

  // ── Hotspots ────────────────────────────────────────────────────────────────
  // Chapter labels show in the overview, equipment labels in their own chapter,
  // and part labels while the open server is in focus.
  const spots = [];
  function addSpot(id, kind, position, text) {
    const el = document.createElement('button');
    el.type = 'button';
    el.className = 'hotspot hotspot-item';
    el.textContent = text;
    if (names[id] && names[id].toUpperCase() !== text) el.title = names[id];
    el.style.setProperty('--node-color', colors[itemChapter[id] || id] || '#f7ce46');
    el.hidden = true;
    el.addEventListener('click', () => onSelect(id));
    hotspotLayer.append(el);
    spots.push({ id, kind, el, position, w: 0, h: 0, x: NaN, y: NaN, shown: false, sel: false });
  }
  for (const [id, text] of Object.entries(itemLabels)) {
    if (PART_ANCHORS[id]) {
      addSpot(id, 'part', new THREE.Vector3(...PART_ANCHORS[id]).add(SERVER_ORIGIN), text);
      continue;
    }
    const bounds = boundsOf(id);
    if (!bounds) continue;
    let anchor;
    if (ITEM_ANCHORS[id]) anchor = new THREE.Vector3(...ITEM_ANCHORS[id]);
    else {
      anchor = bounds.getCenter(new THREE.Vector3());
      anchor.y = bounds.max.y + 0.35;
    }
    addSpot(id, 'item', anchor, text);
  }
  function measureSpots() {
    const hidden = spots.map((s) => s.el.hidden);
    for (const s of spots) {
      s.el.style.visibility = 'hidden';
      s.el.hidden = false;
    }
    for (const s of spots) {
      s.w = s.el.offsetWidth;
      s.h = s.el.offsetHeight;
    }
    spots.forEach((s, i) => {
      s.el.hidden = hidden[i];
      s.el.style.visibility = '';
    });
    needsRender = true;
  }
  measureSpots();
  document.fonts?.ready.then(measureSpots);

  const _v = new THREE.Vector3();
  const spotById = new Map(spots.map((spot) => [spot.id, spot]));
  const labelsOf = (chapter) => labelsByChapter[chapter] || [];
  // The stop whose labels and lettering are shown: the scroll position's, or with
  // equipment in focus, the stop that labels it (else its own chapter).
  function contextChapter() {
    const chapter = chapterIds[Math.round(progress)];
    if (!focusId || serverParts.includes(focusId)) return chapter;
    return labelsOf(chapter).includes(focusId) ? chapter : itemChapter[focusId];
  }
  function updateHotspots() {
    const r = safe || { l: 0, r: width, t: 0, b: height };
    const settled = Math.abs(progress - Math.round(progress)) < 0.2;
    const partFocus = serverParts.includes(focusId);
    let wanted;
    if (partFocus) wanted = serverParts.filter((id) => spotById.get(id)?.kind === 'part');
    else if (flowId || (!focusId && !settled)) wanted = [];
    else wanted = labelsOf(contextChapter()).filter((id) => spotById.get(id)?.kind === 'item');
    // The selected label is placed first, so other labels give way to it.
    if (selected && wanted.includes(selected)) wanted = [selected, ...wanted.filter((id) => id !== selected)];
    const shown = new Map();
    const placed = [];
    for (const id of wanted) {
      const s = spotById.get(id);
      _v.copy(s.position).project(camera);
      const x = Math.round((_v.x * 0.5 + 0.5) * width);
      const y = Math.round((-_v.y * 0.5 + 0.5) * height);
      const box = [x - s.w / 2 - 4, y - s.h, x + s.w / 2 + 4, y + 16]; // label above, 16 px leader below
      if (_v.z <= -1 || _v.z >= 1 || box[0] < r.l || box[2] > r.r || box[1] < r.t || box[3] > r.b) continue;
      // Labels that would overlap one already placed are skipped.
      if (placed.some((p) => box[0] < p[2] && box[2] > p[0] && box[1] < p[3] && box[3] > p[1])) continue;
      placed.push(box);
      shown.set(id, [x, y]);
    }
    for (const s of spots) {
      const at = shown.get(s.id);
      const show = !!at;
      if (show !== s.shown) {
        if (!show && s.el === document.activeElement) onHotspotHidden();
        s.shown = show;
        s.el.hidden = !show;
      }
      if (show && (at[0] !== s.x || at[1] !== s.y)) {
        [s.x, s.y] = at;
        s.el.style.transform = `translate(${s.x}px, ${s.y}px) translate(-50%, -100%)`;
      }
      const sel = selected === s.id;
      if (sel !== s.sel) {
        s.sel = sel;
        s.el.classList.toggle('selected', sel);
      }
    }
  }

  // Each stop's lettering rises out of the ground when the stop is shown.
  function wordTargets() {
    const key = serverParts.includes(focusId) ? 'server' : contextChapter();
    for (const [id, group] of Object.entries(words)) group.userData.target = id === key ? 1 : 0;
  }
  function wordsMoving() {
    wordTargets();
    return Object.values(words).some((g) => Math.abs(g.userData.target - g.scale.y) > 0.005);
  }
  function updateWords(k) {
    for (const g of Object.values(words)) {
      g.scale.y += (g.userData.target - g.scale.y) * k;
      if (Math.abs(g.userData.target - g.scale.y) <= 0.005) g.scale.y = g.userData.target;
      g.visible = g.scale.y > 0.001;
      g.updateMatrixWorld(true);
    }
  }

  // ── Camera ──────────────────────────────────────────────────────────────────
  // The view offset centres the subject in the free screen area. It eases with the
  // camera, except on a window resize, where it snaps.
  function targetView() {
    const r = safe || { l: 0, r: width, t: 0, b: height };
    targetOffX = width / 2 - (r.l + r.r) / 2;
    targetOffY = height / 2 - (r.t + r.b) / 2;
  }
  function applyView() {
    camera.setViewOffset(width, height, offX, offY, width, height);
    camera.zoom = zoom;
    camera.updateProjectionMatrix();
  }

  function resize() {
    const w = container.clientWidth;
    const h = container.clientHeight;
    if (!w || !h) return;
    width = w;
    height = h;
    renderer.setPixelRatio(pixelRatio(w, h));
    renderer.setSize(w, h);
    const aspect = w / h;
    const v = aspect < 1 ? 23 / aspect : 22;
    camera.left = -v * aspect;
    camera.right = v * aspect;
    camera.top = v;
    camera.bottom = -v;
    targetView();
    offX = targetOffX;
    offY = targetOffY;
    applyView();
    updatePose();
    measureSpots();
  }

  function updatePose() {
    const r = safe || { l: 0, r: width, t: 0, b: height, side: false };
    const t = reduced ? Math.round(progress) : progress;
    const index = Math.min(STOPS.length - 2, Math.floor(t));
    const a = STOPS[index];
    const b = STOPS[index + 1];
    const q = t - index;
    const u = q * q * (3 - 2 * q);
    target.set(lerp(a.x, b.x, u), 0, lerp(a.z, b.z, u));
    targetAzimuth = lerp(a.angle, b.angle, u) + orbit;
    targetElevation = lerp(a.elevation, b.elevation, u);
    // Chapter framings were tuned at 1024×768; scale their limits by the actual pixels per unit.
    const ppu = width / (camera.right - camera.left);
    const s = ppu / 17.45;
    targetZoom = lerp(a.zoom, b.zoom, u) * Math.min(1, (r.r - r.l) / (480 * s), (r.b - r.t) / (220 * s));
    const bounds = focusId && boundsOf(focusId);
    if (bounds) {
      bounds.getCenter(target);
      target.y = 0;
      const part = serverParts.includes(focusId);
      targetAzimuth = 0.6 + orbit;
      targetElevation = 29;
      // Fit the whole chassis for server parts, or the item itself, inside the free area.
      const fit = part ? boundsOf('server') || bounds : bounds;
      targetZoom = fitZoom(fit, part ? 2.1 : 2.5, r, ppu);
    }
    // A camera move leaves any hover name stale.
    hideTooltip();
    canvas.style.cursor = 'grab';
    needsRender = true;
  }

  const _right = new THREE.Vector3();
  const _up = new THREE.Vector3();
  const _toward = new THREE.Vector3();
  const _corner = new THREE.Vector3();
  // The largest zoom at which `bounds`, seen from the target pose, fits in rect `r`.
  function fitZoom(bounds, maxZoom, r, ppu) {
    const az = targetAzimuth;
    _right.set(Math.cos(az), 0, -Math.sin(az));
    _toward.set(Math.sin(az) * 42, targetElevation, Math.cos(az) * 42).normalize();
    _up.crossVectors(_toward, _right);
    let ex = 0;
    let ey = 0;
    for (let i = 0; i < 8; i++) {
      _corner
        .set(
          i & 1 ? bounds.max.x : bounds.min.x,
          i & 2 ? bounds.max.y : bounds.min.y,
          i & 4 ? bounds.max.z : bounds.min.z,
        )
        .sub(target);
      ex = Math.max(ex, 2 * Math.abs(_corner.dot(_right)));
      ey = Math.max(ey, 2 * Math.abs(_corner.dot(_up)));
    }
    return Math.min(maxZoom, (0.9 * (r.r - r.l)) / (ex * ppu || 1), (0.9 * (r.b - r.t)) / (ey * ppu || 1));
  }

  function isMoving() {
    return (
      Math.abs(targetAzimuth - azimuth) > 1e-4 ||
      Math.abs(targetZoom - zoom) > 1e-4 ||
      target.distanceToSquared(lookAt) > 1e-5 ||
      Math.abs(targetElevation - elevation) > 1e-4 ||
      Math.abs(targetOffX - offX) > 0.5 ||
      Math.abs(targetOffY - offY) > 0.5 ||
      wordsMoving()
    );
  }

  // Drops whole turns from the orbit without moving the camera, so a reset never spins.
  function normalizeOrbit() {
    const turns = Math.round(orbit / TURN);
    if (!turns) return;
    orbit -= turns * TURN;
    azimuth -= turns * TURN;
    targetAzimuth -= turns * TURN;
  }

  new ResizeObserver(resize).observe(container);
  let dprQuery = null;
  const watchPixelRatio = () => {
    dprQuery = matchMedia(`(resolution: ${window.devicePixelRatio}dppx)`);
    dprQuery.addEventListener(
      'change',
      () => {
        resize();
        watchPixelRatio();
      },
      { once: true },
    );
  };
  watchPixelRatio();
  canvas.addEventListener('webglcontextrestored', () => {
    needsRender = true;
  });

  // ── Pointer: drag to orbit, click to select, hover for a name ───────────────
  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();
  let drag = null;
  let dragged = false;
  function pick(clientX, clientY) {
    const rect = container.getBoundingClientRect();
    pointer.set(((clientX - rect.left) / rect.width) * 2 - 1, (-(clientY - rect.top) / rect.height) * 2 + 1);
    raycaster.setFromCamera(pointer, camera);
    const node = raycaster.intersectObjects(pickables, false)[0]?.object.userData.node || null;
    return PICK_ALIASES[node] || node;
  }
  canvas.style.cursor = 'grab';
  canvas.addEventListener('pointerdown', (e) => {
    if (e.button !== 0 || !e.isPrimary) return;
    drag = { x: e.clientX, y: e.clientY, orbit, id: e.pointerId };
    dragged = false;
    canvas.setPointerCapture(e.pointerId);
    hideTooltip();
  });
  canvas.addEventListener('pointermove', (e) => {
    if (drag && drag.id === e.pointerId) {
      const dx = e.clientX - drag.x;
      if (Math.hypot(dx, e.clientY - drag.y) > 5) dragged = true;
      if (dragged && Math.abs(dx) > 5) {
        orbit = drag.orbit - dx * 0.006;
        updatePose();
      }
      return;
    }
    if (e.pointerType === 'mouse') queueHover(e.clientX, e.clientY);
  });
  const endDrag = () => {
    if (!drag) return;
    drag = null;
    normalizeOrbit();
  };
  canvas.addEventListener('pointerup', endDrag);
  canvas.addEventListener('lostpointercapture', endDrag);
  canvas.addEventListener('pointercancel', () => {
    drag = null;
    dragged = false;
  });
  // Selection runs on click, not pointerup, so a synthesized touch click cannot land on
  // UI that the selection itself just opened.
  canvas.addEventListener('click', (e) => {
    if (dragged) {
      dragged = false;
      return;
    }
    const node = pick(e.clientX, e.clientY);
    if (node) onSelect(node);
    else onEmptyClick();
  });
  let hoverAt = null;
  function queueHover(x, y) {
    if (!hoverAt) requestAnimationFrame(runHover);
    hoverAt = { x, y };
  }
  function runHover() {
    const { x, y } = hoverAt;
    hoverAt = null;
    const node = drag ? null : pick(x, y);
    canvas.style.cursor = node ? 'pointer' : 'grab';
    if (!tooltip) return;
    if (!node || !names[node]) return hideTooltip();
    tooltip.textContent = names[node];
    tooltip.style.transform = `translate(${Math.round(x + 14)}px, ${Math.round(y + 16)}px)`;
    tooltip.hidden = false;
  }
  function hideTooltip() {
    if (tooltip) tooltip.hidden = true;
  }
  canvas.addEventListener('pointerleave', hideTooltip);

  // ── Flows ───────────────────────────────────────────────────────────────────
  const flowMaterials = new Map();
  function flowMaterial(color, kind) {
    const key = kind + color;
    if (!flowMaterials.has(key)) {
      const opacity = kind === 'tube' ? 0.55 : kind === 'standby' ? 0.4 : 1;
      flowMaterials.set(key, new THREE.MeshBasicMaterial({ color, transparent: opacity < 1, opacity }));
    }
    return flowMaterials.get(key);
  }
  function setFlow(id) {
    flowId = PATHS[id] ? id : null;
    needsRender = true;
    if (flowGroup) root.remove(flowGroup);
    flowGroup = null;
    flowPackets = [];
    if (!flowId) return;
    flowGroup = new THREE.Group();
    root.add(flowGroup);
    // Size tubes and packets in pixels so they stay visible on small screens.
    const pxPerUnit = width / ((camera.right - camera.left) / Math.max(targetZoom, 0.1));
    const tubeWidth = Math.max(0.075, 3 / pxPerUnit);
    const packetSize = Math.max(0.25, 8 / pxPerUnit);
    for (const def of PATHS[flowId]) {
      const points = def.points.map((p) => new THREE.Vector3(...p));
      const lengths = [0];
      for (let i = 1; i < points.length; i++) lengths.push(lengths.at(-1) + points[i].distanceTo(points[i - 1]));
      for (let i = 1; i < points.length; i++) {
        const tube = new THREE.Mesh(UNIT, flowMaterial(def.color, def.standby ? 'standby' : 'tube'));
        tube.position
          .copy(points[i - 1])
          .add(points[i])
          .multiplyScalar(0.5);
        tube.scale.set(tubeWidth, tubeWidth, points[i - 1].distanceTo(points[i]));
        tube.lookAt(points[i]);
        flowGroup.add(tube);
      }
      if (def.standby) continue;
      const total = lengths.at(-1);
      const count = Math.max(4, Math.round(total / 2.4));
      for (let n = 0; n < count; n++) {
        const packet = new THREE.Mesh(UNIT, flowMaterial(def.color, 'packet'));
        packet.scale.setScalar(packetSize);
        flowGroup.add(packet);
        flowPackets.push({ mesh: packet, points, lengths, total, offset: (n * total) / count });
      }
    }
    placePackets();
  }
  function placePackets() {
    for (const p of flowPackets) {
      const d = (flowTime * FLOW_SPEED + p.offset) % p.total;
      let i = 1;
      while (i < p.lengths.length - 1 && p.lengths[i] < d) i++;
      const span = p.lengths[i] - p.lengths[i - 1] || 1;
      p.mesh.position.copy(p.points[i - 1]).lerp(p.points[i], (d - p.lengths[i - 1]) / span);
    }
  }

  // ── Render loop ─────────────────────────────────────────────────────────────
  // Frames render only when something changed. Ambient motion (fans, van, packets)
  // is capped at 30 fps, and nothing renders while the canvas is covered.
  let last = performance.now();
  let lastDraw = 0;
  let readyFired = false;
  function frame(now) {
    requestAnimationFrame(frame);
    if (document.hidden) {
      last = now;
      return;
    }
    const moving = isMoving();
    const ambient = !paused && !covered;
    if (!needsRender && !moving && (!ambient || now - lastDraw < AMBIENT_FRAME_MS - 1)) {
      if (!ambient) last = now; // so the next camera move eases from a fresh clock
      return;
    }
    const elapsed = Math.min((now - last) / 1000, 0.25);
    last = now;
    lastDraw = now;
    needsRender = false;
    let k = reduced ? 1 : 1 - Math.pow(0.91, elapsed * 60);
    if (target.distanceTo(lookAt) > 20) k = Math.max(k, 0.25); // long jumps never linger
    azimuth += (targetAzimuth - azimuth) * k;
    zoom += (targetZoom - zoom) * k;
    elevation += (targetElevation - elevation) * k;
    lookAt.lerp(target, k);
    offX += (targetOffX - offX) * k;
    offY += (targetOffY - offY) * k;
    updateWords(reduced ? 1 : 1 - Math.pow(0.82, elapsed * 60));
    if (!isMoving()) {
      azimuth = targetAzimuth;
      zoom = targetZoom;
      elevation = targetElevation;
      lookAt.copy(target);
      offX = targetOffX;
      offY = targetOffY;
    }
    camera.position.set(lookAt.x + Math.sin(azimuth) * 42, elevation, lookAt.z + Math.cos(azimuth) * 42);
    camera.lookAt(lookAt);
    if (camera.zoom !== zoom || camera.view?.offsetX !== offX || camera.view?.offsetY !== offY) applyView();
    if (!paused) {
      flowTime += Math.min(elapsed, 0.05);
      fanGroups.forEach((f) => (f.rotation.y = flowTime * 1.8));
      van.position.z = ((flowTime * 1.9) % 62) - 26;
      placePackets();
    }
    camera.updateMatrixWorld();
    if (covered && readyFired) return;
    updateHotspots();
    renderer.render(scene, camera);
    if (!readyFired) {
      readyFired = true;
      onReady();
    }
  }
  resize();
  updatePose();
  requestAnimationFrame(frame);

  return {
    journey(value) {
      if (!Number.isFinite(value)) return;
      progress = clamp(value, 0, STOPS.length - 1);
      if (!focusId) updatePose();
      needsRender = true;
    },
    select(id) {
      focusId = id;
      selected = id;
      const bounds = boundsOf(id);
      halo.visible = !!bounds;
      if (bounds) {
        const center = bounds.getCenter(new THREE.Vector3());
        const size = bounds.getSize(new THREE.Vector3());
        halo.position.set(center.x, 0.45, center.z);
        halo.scale.set(Math.max(size.x / 2.4, 0.7), 1, Math.max(size.z / 2.2, 0.7));
        haloMaterial.color.set(colors[itemChapter[id] || id] || '#f7ce46');
      }
      updatePose();
    },
    clearFocus() {
      focusId = null;
      selected = null;
      halo.visible = false;
      updatePose();
    },
    flow: setFlow,
    reset() {
      normalizeOrbit();
      orbit = 0;
      updatePose();
    },
    orbitBy(delta) {
      orbit += delta;
      normalizeOrbit();
      updatePose();
    },
    get orbit() {
      return orbit;
    },
    pause(value) {
      paused = value;
      needsRender = true;
    },
    setReducedMotion(value) {
      reduced = value;
      updatePose();
    },
    setSafeRect(rect) {
      safe = rect;
      targetView();
      updatePose();
    },
    cover(value) {
      if (covered === value) return;
      covered = value;
      needsRender = true;
    },
    isSettled() {
      return !needsRender && !isMoving();
    },
  };
}
