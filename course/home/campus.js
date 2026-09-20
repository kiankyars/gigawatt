import * as THREE from './vendor/three.module.js';
import { OrbitControls } from './vendor/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from './vendor/CSS2DRenderer.js';

// Procedural campus recovered from diagram/mock_3d.html at fdb3763.
// This is a conceptual illustration: positions, quantities and routes are schematic.
export function createCampus({ mount, onSelect = () => {} }) {
  if (!mount) throw new Error('The campus viewer needs a mount element.');
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(38, 1, 1, 8000);
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0xfafaf7, 0);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.domElement.className = 'campus-canvas';
  renderer.domElement.setAttribute('aria-label', 'Interactive 3D data center campus. Drag to orbit; scroll or pinch to zoom. Use the system buttons for keyboard navigation.');
  renderer.domElement.style.cssText = 'display:block;width:100%;height:100%;touch-action:none;';
  mount.appendChild(renderer.domElement);

  const labels = new CSS2DRenderer();
  labels.domElement.className = 'campus-labels';
  labels.domElement.style.cssText = 'position:absolute;inset:0;pointer-events:none;overflow:hidden;';
  labels.domElement.setAttribute('aria-hidden', 'true');
  mount.appendChild(labels.domElement);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.09;
  controls.maxPolarAngle = Math.PI * 0.48;
  controls.minDistance = 130;
  controls.maxDistance = 7000;
  controls.zoomSpeed = 0.8;
  controls.panSpeed = 0.65;

  scene.add(new THREE.HemisphereLight(0xffffff, 0xd8d8cf, 1.2));
  const sun = new THREE.DirectionalLight(0xffffff, 1.7);
  sun.position.set(500, 900, 400);
  scene.add(sun);

  const V = { grid: 0x185f8f, mv: 0x2580a7, ac: 0x278a76, dc: 0x57b894 };
  const T = { die: 0xb3261e, hot: 0xd3552c, warm: 0xe8853b, air: 0xf0b34e };
  const STEEL = 0x9a9a92, DARK = 0x3a3a36;
  const selectable = [], labelObjects = [], flowMeshes = { power: [], heat: [] };
  let zone = 'power';
  const mat = color => new THREE.MeshLambertMaterial({ color });
  function addMesh(geometry, color, x, y, z) {
    const mesh = new THREE.Mesh(geometry, mat(color));
    mesh.position.set(x, y, z);
    mesh.userData.zone = zone;
    scene.add(mesh);
    if (zone) selectable.push(mesh);
    return mesh;
  }
  function box(w, h, d, color, x, y, z, ry = 0) {
    const mesh = addMesh(new THREE.BoxGeometry(w, h, d), color, x, y, z);
    mesh.rotation.y = ry;
    return mesh;
  }
  function cyl(r, h, color, x, y, z, rz = 0) {
    const mesh = addMesh(new THREE.CylinderGeometry(r, r, h, 20), color, x, y, z);
    mesh.rotation.z = rz;
    return mesh;
  }
  function tag(x, y, z, title, subtitle, overview = false) {
    const element = document.createElement('div');
    element.className = 'campus-tag';
    element.dataset.system = zone;
    element.style.cssText = 'color:#202725;background:rgba(250,250,247,.94);border:1px solid #bac2ba;border-radius:5px;padding:5px 8px;font:600 11px/1.25 Inter,Helvetica Neue,Arial,sans-serif;white-space:nowrap;box-shadow:0 2px 8px #172c2310;';
    element.append(document.createTextNode(title));
    if (subtitle) {
      const detail = document.createElement('small');
      detail.textContent = subtitle;
      detail.style.cssText = 'display:block;color:#626d66;font-weight:400;font-size:10px;margin-top:2px;';
      element.appendChild(detail);
    }
    const label = new CSS2DObject(element);
    label.position.set(x, y, z);
    label.userData = { zone, overview };
    scene.add(label);
    labelObjects.push(label);
  }
  function path(points) {
    // Piecewise linear paths preserve the schematic's right-angle equipment routing.
    const curve = new THREE.CurvePath();
    points.slice(1).forEach((point, i) => curve.add(new THREE.LineCurve3(
      new THREE.Vector3(...points[i]), new THREE.Vector3(...point)
    )));
    return curve;
  }
  function tube(points, color, radius = 2.4, flow = 'power') {
    const curve = path(points);
    const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, 96, radius, 8), new THREE.MeshBasicMaterial({ color }));
    mesh.userData.zone = flow === 'heat' ? 'cooling' : 'power';
    mesh.material.transparent = true;
    scene.add(mesh);
    flowMeshes[flow].push(mesh);
    return curve;
  }

  // Original ground, generation yard, towers and substation dimensions.
  zone = null;
  const ground = addMesh(new THREE.PlaneGeometry(2320, 950), 0xeceada, -130, -1, 0);
  ground.rotation.x = -Math.PI / 2;

  zone = 'power';
  box(220, 55, 180, STEEL, -950, 27.5, 0);
  for (let i = 0; i < 10; i++) cyl(9, 42, DARK, -1040 + i * 20, 76, i % 2 ? 55 : -55);
  box(46, 40, 46, 0x6b6b62, -800, 20, 0);
  for (let i = -1; i <= 1; i++) cyl(2.5, 22, 0xc9c9bd, -800 + i * 12, 50, 0);
  tag(-950, 128, 0, 'On-site generation', 'Separate source option', true);

  function towerAt(x) {
    box(8, 240, 8, STEEL, x, 120, 0);
    box(120, 6, 6, STEEL, x, 225, 0);
    box(90, 6, 6, STEEL, x, 195, 0);
  }
  towerAt(-600); towerAt(-380);
  // Grid power enters independently of the on-site generation yard.
  tube([[-730, 230, 0], [-600, 228, 0], [-490, 200, 0], [-380, 228, 0], [-270, 195, 0], [-180, 170, 0]], V.grid, 3);
  tag(-490, 278, 0, 'Transmission', 'Grid connection', true);

  for (const [w, d, x, z] of [[200, 4, -80, 90], [200, 4, -80, -90], [4, 180, 20, 0], [4, 180, -180, 0]]) {
    box(w, 26, d, 0xc9c9bd, x, 13, z);
  }
  box(60, 50, 50, 0x6b6b62, -80, 25, 0);
  for (let i = -1; i <= 1; i++) cyl(3, 26, 0xc9c9bd, -80 + i * 16, 62, 0);
  box(20, 34, 20, STEEL, -140, 17, -40);
  tag(-80, 116, 0, 'Substation', 'Step down the voltage', true);
  tube([[-180, 170, 0], [-80, 60, 0], [-80, 12, 0], [150, 12, 0]], V.mv, 2.8);
  // The optional generation feeder joins campus distribution, not the HV corridor.
  tube([[-800, 28, 0], [-760, 28, 0], [-760, 12, -195], [80, 12, -195], [80, 12, 0]], V.mv, 2.4);
  for (let i = 0; i < 3; i++) box(50, 26, 22, 0xf0efe6, 20 + i * 60, 13, 150);
  tag(80, 65, 150, 'Battery storage', 'Energy reserve');

  // Recovered building shell. Its translucent roof reveals the original rack rows.
  zone = 'compute';
  const BX = 480, BW = 620, BD = 300, BH = 130;
  box(BW, 8, BD, 0xdedcd0, BX, 4, 0);
  box(BW, BH, 8, 0xd4d2c6, BX, BH / 2 + 8, -BD / 2);
  box(8, BH, BD, 0xd4d2c6, BX - BW / 2, BH / 2 + 8, 0);
  box(8, BH, BD, 0xd4d2c6, BX + BW / 2, BH / 2 + 8, 0);
  const roof = box(BW, 10, BD, 0xe6e4d8, BX, BH + 13, 0);
  roof.material.transparent = true;
  roof.material.opacity = 0.26;
  roof.material.depthWrite = false;
  // A translucent cutaway is explanatory context, not a clickable cover over racks.
  selectable.splice(selectable.indexOf(roof), 1);
  tag(BX + 190, 90, 215, 'Data hall', 'Electrical power → compute', true);

  zone = 'power';
  box(34, 40, 30, 0x6b6b62, BX - 250, 28, -60);
  tag(BX - 250, 83, -60, 'Unit substation', 'Medium → low voltage');
  for (let i = 0; i < 3; i++) box(22, 52, 26, 0xf0efe6, BX - 180 + i * 30, 34, -80);
  tag(BX - 145, 128, -80, 'UPS lineups', 'Bridge brief power interruptions');

  zone = 'compute';
  let lit;
  for (let row = 0; row < 2; row++) {
    for (let i = 0; i < 8; i++) {
      const mesh = box(26, 74, 34, row === 1 && i === 2 ? 0x2a6656 : DARK, BX - 60 + i * 42, 45, row ? 40 : -30);
      if (row === 1 && i === 2) lit = mesh.position.clone();
    }
  }
  tag(lit.x, 118, lit.z + 48, 'Compute racks', 'Power supplies → processors');

  zone = 'cooling';
  for (let i = 0; i < 4; i++) {
    box(60, 16, 44, 0xf0efe6, BX - 180 + i * 120, BH + 26, 20);
    cyl(16, 6, STEEL, BX - 180 + i * 120, BH + 37, 20);
  }
  tag(BX + 10, BH + 130, 65, 'Heat rejection', 'Transfer heat to the air', true);

  tube([[150, 12, 0], [BX - 250, 12, -60], [BX - 250, 46, -60]], V.mv, 2.8);
  tube([[BX - 250, 46, -60], [BX - 180, 60, -80], [BX - 120, 60, -80], [BX - 120, 100, -40], [lit.x, 100, lit.z], [lit.x, 70, lit.z]], V.ac, 2.8);
  const heatCurve = tube([[lit.x, 70, lit.z], [lit.x, 110, lit.z], [lit.x, BH + 20, lit.z], [BX + 60, BH + 26, 20], [BX + 60, BH + 130, 20]], T.hot, 3, 'heat');
  // Thermal lines illustrate heat transfer, not a complete hydraulic loop.
  tube([[BX + 60, BH + 34, 20], [BX + 60, BH + 130, 20]], T.air, 2.2, 'heat');

  const wattCurve = path([
    [-730, 230, 0], [-600, 228, 0], [-490, 200, 0], [-380, 228, 0], [-270, 195, 0], [-180, 170, 0],
    [-80, 60, 0], [-80, 12, 0], [150, 12, 0], [BX - 250, 12, -60], [BX - 250, 46, -60],
    [BX - 180, 60, -80], [BX - 120, 60, -80], [BX - 120, 100, -40], [lit.x, 100, lit.z], [lit.x, 70, lit.z]
  ]);
  function makePulse(color, radius) {
    const mesh = new THREE.Mesh(new THREE.SphereGeometry(radius, 16, 12), new THREE.MeshBasicMaterial({ color }));
    scene.add(mesh);
    return mesh;
  }
  const powerPulses = [makePulse(V.grid, 6.5), makePulse(V.grid, 6.5)];
  const heatPulse = makePulse(T.die, 6);

  const presets = {
    campus: { target: [-105, 92, 0], position: [250, 680, 1390], bounds: [[-1090, 0, -230], [840, 295, 250]] },
    power: { target: [-390, 100, 0], position: [170, 600, 1110], bounds: [[-1090, 0, -230], [430, 300, 190]] },
    compute: { target: [490, 90, 20], position: [820, 370, 660], bounds: [[160, 0, -170], [820, 265, 250]] },
    cooling: { target: [505, 155, 30], position: [750, 440, 660], bounds: [[270, 80, -130], [750, 285, 180]] }
  };
  let currentFocus = 'campus', currentFlow = 'all';
  let motion = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let disposed = false, frame = 0, tween = null, lastTime = 0, elapsed = 0;
  let pointerStart = null;
  const raycaster = new THREE.Raycaster();

  function showLabels() {
    const compact = mount.clientWidth < 660;
    labelObjects.forEach(label => {
      label.visible = currentFocus === 'campus'
        ? label.userData.overview && (!compact || ['power', 'compute', 'cooling'].includes(label.userData.zone))
        : label.userData.zone === currentFocus;
      // Keep small viewports readable by shortening the secondary labels.
      const detail = label.element.querySelector('small');
      if (detail) detail.style.display = compact ? 'none' : 'block';
    });
  }
  function destination(name) {
    const preset = presets[name];
    const target = new THREE.Vector3(...preset.target);
    const offset = new THREE.Vector3(...preset.position).sub(target);
    // Fit model corners rather than assuming the user's viewport is full screen.
    // Extra horizontal clearance keeps projected HTML labels inside the hero.
    const fitCamera = camera.clone();
    const [low, high] = preset.bounds;
    const direction = offset.clone().normalize();
    function fits(distance) {
      fitCamera.position.copy(target).addScaledVector(direction, distance);
      fitCamera.lookAt(target);
      fitCamera.updateMatrixWorld();
      for (const x of [low[0], high[0]]) for (const y of [low[1], high[1]]) for (const z of [low[2], high[2]]) {
        const point = new THREE.Vector3(x, y, z).project(fitCamera);
        if (Math.abs(point.x) > 0.86 || Math.abs(point.y) > 0.78) return false;
      }
      return true;
    }
    let near = offset.length(), far = near;
    while (!fits(far) && far < 12000) far *= 1.4;
    for (let pass = 0; pass < 12; pass++) {
      const midpoint = (near + far) / 2;
      if (fits(midpoint)) far = midpoint; else near = midpoint;
    }
    offset.setLength(far);
    return { target, position: target.clone().add(offset) };
  }
  function focus(name = 'campus', immediate = false) {
    if (!presets[name] || disposed) return;
    currentFocus = name;
    const next = destination(name);
    showLabels();
    if (immediate || !motion) {
      tween = null;
      camera.position.copy(next.position);
      controls.target.copy(next.target);
      controls.update();
    } else {
      tween = { started: performance.now(), fromPosition: camera.position.clone(), fromTarget: controls.target.clone(), ...next };
    }
    mount.dataset.focus = name;
  }
  function setFlow(value) {
    if (!['all', 'power', 'heat', 'none'].includes(value)) return;
    currentFlow = value;
    for (const [kind, meshes] of Object.entries(flowMeshes)) {
      const visible = value === 'all' || value === kind;
      meshes.forEach(mesh => { mesh.material.opacity = visible ? 1 : 0.12; });
    }
    powerPulses.forEach(pulse => { pulse.visible = value === 'all' || value === 'power'; });
    heatPulse.visible = value === 'all' || value === 'heat';
    mount.dataset.flow = value;
  }
  function setMotion(value) {
    motion = Boolean(value);
    if (!motion && tween) focus(currentFocus, true);
    mount.dataset.motion = String(motion);
  }
  function resize() {
    if (disposed) return;
    const width = Math.max(1, mount.clientWidth), height = Math.max(1, mount.clientHeight);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height, false);
    labels.setSize(width, height);
    focus(currentFocus, true);
  }
  function pick(event) {
    if (!pointerStart || Math.hypot(event.clientX - pointerStart.x, event.clientY - pointerStart.y) > 6) return;
    const bounds = renderer.domElement.getBoundingClientRect();
    raycaster.setFromCamera(new THREE.Vector2((event.clientX - bounds.left) / bounds.width * 2 - 1, -(event.clientY - bounds.top) / bounds.height * 2 + 1), camera);
    const hit = raycaster.intersectObjects(selectable, false)[0];
    if (hit) { focus(hit.object.userData.zone); onSelect(hit.object.userData.zone); }
    pointerStart = null;
  }
  function pointerDown(event) { pointerStart = event.button === 0 ? { x: event.clientX, y: event.clientY } : null; }
  function cancelTween() { tween = null; }
  renderer.domElement.addEventListener('pointerdown', pointerDown);
  renderer.domElement.addEventListener('pointerup', pick);
  controls.addEventListener('start', cancelTween);

  function tick(now) {
    if (disposed) return;
    const delta = lastTime ? Math.min(now - lastTime, 80) : 0;
    lastTime = now;
    if (motion && !document.hidden) elapsed += delta;
    if (tween) {
      const t = Math.min(1, (now - tween.started) / 780);
      const eased = 1 - Math.pow(1 - t, 3);
      camera.position.lerpVectors(tween.fromPosition, tween.position, eased);
      controls.target.lerpVectors(tween.fromTarget, tween.target, eased);
      if (t === 1) tween = null;
    }
    powerPulses.forEach((pulse, i) => {
      const t = (elapsed / 11000 + i / 2) % 1;
      pulse.position.copy(wattCurve.getPointAt(t));
      pulse.material.color.setHex(t < 0.58 ? V.grid : t < 0.86 ? V.mv : V.ac);
    });
    const heatT = (elapsed / 5500 + 0.2) % 1;
    heatPulse.position.copy(heatCurve.getPointAt(heatT));
    heatPulse.material.color.setHex(heatT < 0.65 ? T.hot : T.air);
    controls.update();
    if (!document.hidden) {
      renderer.render(scene, camera);
      labels.render(scene, camera);
    }
    frame = requestAnimationFrame(tick);
  }

  const observer = new ResizeObserver(resize);
  observer.observe(mount);
  resize(); setFlow(currentFlow); setMotion(motion);
  frame = requestAnimationFrame(tick);

  return {
    focus,
    reset: () => focus('campus'),
    setFlow,
    setMotion,
    resize,
    dispose() {
      if (disposed) return;
      disposed = true;
      cancelAnimationFrame(frame);
      observer.disconnect();
      renderer.domElement.removeEventListener('pointerdown', pointerDown);
      renderer.domElement.removeEventListener('pointerup', pick);
      controls.removeEventListener('start', cancelTween);
      controls.dispose();
      scene.traverse(object => {
        object.geometry?.dispose();
        const materials = Array.isArray(object.material) ? object.material : [object.material];
        materials.forEach(material => material?.dispose());
      });
      renderer.dispose();
      renderer.domElement.remove();
      labels.domElement.remove();
    }
  };
}
