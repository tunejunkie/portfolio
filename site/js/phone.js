// Code-built 3D iPhone (three.js). One WebGL canvas, many phones sharing geometry.
// World units = CSS pixels at z=0, origin at viewport centre, +y up.
import * as THREE from 'three';

const W = 0.482, H = 1, D = 0.05;           // body proportions (iPhone 15/16 Pro)
const R = 0.07;                             // outer corner radius
const RIM = 0.0085;                         // metal rim visible from the front
const BEZ = 0.0115;                         // black glass bezel around the display
const IN = RIM + BEZ;                       // display inset
const SR = R - IN * 0.85;                   // display corner radius
const EB = 0.007, ET = 0.013;               // edge bevel: lateral size, depth (rounds the titanium sides)

function rrect(w, h, r) {
  const s = new THREE.Shape(), x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r);
  s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r);
  s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
  return s;
}
// squircle-ish corners look closer to Apple's continuous curve than arcs
function squircle(w, h, r, seg = 18) {
  const s = new THREE.Shape(), pts = [];
  const corner = (cx, cy, a0) => {
    for (let i = 0; i <= seg; i++) {
      const a = a0 + (i / seg) * Math.PI / 2, c = Math.cos(a), sn = Math.sin(a);
      const k = 0.62; // superellipse exponent factor
      pts.push(new THREE.Vector2(cx + r * Math.sign(c) * Math.pow(Math.abs(c), k), cy + r * Math.sign(sn) * Math.pow(Math.abs(sn), k)));
    }
  };
  corner(w / 2 - r, h / 2 - r, 0); corner(-w / 2 + r, h / 2 - r, Math.PI / 2);
  corner(-w / 2 + r, -h / 2 + r, Math.PI); corner(w / 2 - r, -h / 2 + r, Math.PI * 1.5);
  s.setFromPoints(pts); return s;
}
function planarUV(geo, w, h) {
  const p = geo.attributes.position, uv = new Float32Array(p.count * 2);
  for (let i = 0; i < p.count; i++) { uv[i * 2] = p.getX(i) / w + 0.5; uv[i * 2 + 1] = p.getY(i) / h + 0.5; }
  geo.setAttribute('uv', new THREE.BufferAttribute(uv, 2)); return geo;
}

// Studio lighting as an equirect canvas: soft grey dome, bright overhead + side softboxes, so the
// titanium rim picks up long clean highlights (the "Rotato" look) instead of a dark room.
function studioEnv() {
  const w = 1024, h = 512, c = document.createElement('canvas'); c.width = w; c.height = h;
  const g = c.getContext('2d');
  const sky = g.createLinearGradient(0, 0, 0, h);
  sky.addColorStop(0, '#d8d8e0'); sky.addColorStop(0.3, '#6a6a74'); sky.addColorStop(0.5, '#34343c'); sky.addColorStop(0.62, '#8a8a94'); sky.addColorStop(1, '#1a1a20');
  g.fillStyle = sky; g.fillRect(0, 0, w, h);
  const box = (x, y, bw, bh, a) => { const r = g.createLinearGradient(x, 0, x + bw, 0); r.addColorStop(0, `rgba(255,255,255,0)`); r.addColorStop(.5, `rgba(255,255,255,${a})`); r.addColorStop(1, `rgba(255,255,255,0)`); g.fillStyle = r; g.fillRect(x, y, bw, bh); };
  box(80, 60, 200, 330, 1); box(560, 80, 160, 300, .9); box(330, 20, 260, 70, 1); box(850, 120, 120, 260, .6);
  const t = new THREE.CanvasTexture(c); t.mapping = THREE.EquirectangularReflectionMapping; t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

let shared = null;
function buildShared(renderer) {
  const bodyGeo = new THREE.ExtrudeGeometry(squircle(W - EB * 2, H - EB * 2, R - EB), { depth: D - ET * 2, bevelEnabled: true, bevelThickness: ET, bevelSize: EB, bevelSegments: 14, curveSegments: 6 });
  bodyGeo.translate(0, 0, -(D - ET * 2) / 2);
  const frontGeo = new THREE.ShapeGeometry(squircle(W - RIM * 2, H - RIM * 2, R - RIM));
  const sw = W - IN * 2, sh = H - IN * 2;
  const screenGeo = planarUV(new THREE.ShapeGeometry(squircle(sw, sh, SR)), sw, sh);
  const islandGeo = new THREE.ShapeGeometry(rrect(0.124, 0.036, 0.018));
  const backPlate = new THREE.ShapeGeometry(squircle(W - RIM * 2, H - RIM * 2, R - RIM));
  const bumpGeo = new THREE.ExtrudeGeometry(squircle(0.2, 0.2, 0.055), { depth: 0.006, bevelEnabled: true, bevelThickness: 0.003, bevelSize: 0.003, bevelSegments: 4 });
  const lensGeo = new THREE.CylinderGeometry(0.036, 0.038, 0.012, 40); lensGeo.rotateX(Math.PI / 2);
  const glassGeo = new THREE.CircleGeometry(0.031, 40);
  const btnGeo = new THREE.CapsuleGeometry(0.004, 1, 4, 8);

  const pmrem = new THREE.PMREMGenerator(renderer);
  const env = pmrem.fromEquirectangular(studioEnv()).texture;

  const mats = {
    body: new THREE.MeshPhysicalMaterial({ color: 0xd8d8de, metalness: 1, roughness: 0.16, clearcoat: 0.5, clearcoatRoughness: 0.1, envMap: env, envMapIntensity: 1.1 }),
    front: new THREE.MeshPhysicalMaterial({ color: 0x020203, metalness: 0, roughness: 0.08, clearcoat: 1, envMap: env, envMapIntensity: 0.6 }),
    back: new THREE.MeshPhysicalMaterial({ color: 0x4a4a52, metalness: 0.25, roughness: 0.42, envMap: env, envMapIntensity: 0.9 }),
    island: new THREE.MeshBasicMaterial({ color: 0x000000 }),
    lens: new THREE.MeshPhysicalMaterial({ color: 0x0b0b10, metalness: 0.9, roughness: 0.2, envMap: env }),
    lensGlass: new THREE.MeshPhysicalMaterial({ color: 0x101830, metalness: 0.3, roughness: 0.05, clearcoat: 1, envMap: env }),
    glare: new THREE.MeshPhysicalMaterial({ color: 0xffffff, metalness: 0, roughness: 0.06, transparent: true, opacity: 0.1, envMap: env, envMapIntensity: 1.4, depthWrite: false }),
  };
  // soft contact shadow texture
  const c = document.createElement('canvas'); c.width = c.height = 256;
  const g = c.getContext('2d'), grd = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  grd.addColorStop(0, 'rgba(10,8,40,0.32)'); grd.addColorStop(0.55, 'rgba(10,8,40,0.12)'); grd.addColorStop(1, 'rgba(10,8,40,0)');
  g.fillStyle = grd; g.fillRect(0, 0, 256, 256);
  const shadowTex = new THREE.CanvasTexture(c);
  mats.shadow = new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false });
  shared = { bodyGeo, frontGeo, screenGeo, islandGeo, backPlate, bumpGeo, lensGeo, glassGeo, btnGeo, mats, sw, sh, shadowGeo: new THREE.PlaneGeometry(1, 1) };
  return shared;
}

export class Phone {
  constructor(stage, tex) {
    const S = shared, g = new THREE.Group();
    this.group = g; this.stage = stage;
    const body = new THREE.Mesh(S.bodyGeo, S.mats.body); g.add(body);
    const front = new THREE.Mesh(S.frontGeo, S.mats.front); front.position.z = D / 2 + 0.0005; g.add(front);
    this.screenMat = new THREE.MeshBasicMaterial({ map: tex || null, color: tex ? 0xffffff : 0x111111, toneMapped: false, transparent: true });
    const screen = new THREE.Mesh(S.screenGeo, this.screenMat); screen.position.z = D / 2 + 0.0012; g.add(screen);
    const island = new THREE.Mesh(S.islandGeo, S.mats.island); island.position.set(0, H / 2 - IN - 0.03, D / 2 + 0.0018); g.add(island);
    // no glass/glare layer over the display: the designs must show their true colours
    const back = new THREE.Mesh(S.backPlate, S.mats.back); back.position.z = -D / 2 - 0.0005; back.rotation.y = Math.PI; g.add(back);
    const bump = new THREE.Mesh(S.bumpGeo, S.mats.back); bump.rotation.y = Math.PI; bump.position.set(W / 2 - 0.13, H / 2 - 0.13, -D / 2 - 0.001); g.add(bump);
    [[0.044, 0.044], [0.044, -0.044], [-0.044, 0]].forEach(([dx, dy]) => {
      const l = new THREE.Mesh(S.lensGeo, S.mats.body); l.position.set(W / 2 - 0.13 - dx, H / 2 - 0.13 + dy, -D / 2 - 0.016); g.add(l);
      const gl = new THREE.Mesh(S.glassGeo, S.mats.lensGlass); gl.rotation.y = Math.PI; gl.position.set(l.position.x, l.position.y, -D / 2 - 0.0225); g.add(gl);
    });
    // side buttons
    [[-1, 0.29, 0.035], [-1, 0.19, 0.075], [-1, 0.095, 0.075], [1, 0.15, 0.12], [1, -0.08, 0.06]].forEach(([side, y, len]) => {
      const b = new THREE.Mesh(S.btnGeo, S.mats.body); b.scale.y = len; b.position.set(side * (W / 2 + 0.0005), y, 0); g.add(b);
    });
    const sh = new THREE.Mesh(S.shadowGeo, S.mats.shadow.clone());
    sh.scale.set(W * 1.5, H * 1.12, 1); sh.position.set(0.02, -0.03, -D * 2); g.add(sh);
    this.shadow = sh;
    // state (CSS px / degrees)
    this.sh = 1; this.x = 0; this.y = 0; this.z = 0; this.h = 600; this.rx = 0; this.ry = 0; this.rz = 0; this.o = 1;
    stage.scene.add(g);
  }
  setTexture(tex) { this.screenMat.map = tex; this.screenMat.color.set(0xffffff); this.screenMat.needsUpdate = true; }
  apply() {
    const g = this.group, d2r = Math.PI / 180;
    g.position.set(this.x, this.y, this.z);
    g.scale.setScalar(this.h);
    g.rotation.set(this.rx * d2r, this.ry * d2r, this.rz * d2r, 'YXZ');
    g.visible = this.o > 0.01;
    // fade: only the screen & shadow can fade cleanly; body pops via scale when o<1
    this.screenMat.opacity = this.o;
    this.shadow.material.opacity = this.o * this.sh * (1 - Math.min(1, Math.abs(this.rx) / 50));
    this.shadow.visible = this.shadow.material.opacity > 0.01;
  }
}

export class Stage {
  constructor(canvas) {
    this.canvas = canvas;
    const r = this.renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
    r.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    r.outputColorSpace = THREE.SRGBColorSpace;
    r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = 1.05;
    this.scene = new THREE.Scene();
    if (!shared) buildShared(r);
    const key = new THREE.DirectionalLight(0xffffff, 1.4); key.position.set(-1, 2, 3); this.scene.add(key);
    this.scene.add(new THREE.AmbientLight(0xffffff, 0.35));
    this.fov = 22;
    this.camera = new THREE.PerspectiveCamera(this.fov, 1, 10, 20000);
    this.loader = new THREE.TextureLoader();
    this.phones = [];
    this.resize();
    // keep the drawing buffer + camera aspect locked to the canvas's real on-screen size,
    // so phones never stretch when the window (or the pinned stage) changes width
    if ('ResizeObserver' in window) new ResizeObserver(() => { this.resize(); this.render(); }).observe(canvas);
  }
  resize() {
    const w = this.canvas.clientWidth || window.innerWidth, h = this.canvas.clientHeight || window.innerHeight;
    if (w === this.w && h === this.h) return;
    this.w = w; this.h = h;
    this.renderer.setSize(w, h, false);
    const dist = (h / 2) / Math.tan((this.fov / 2) * Math.PI / 180);
    this.camera.aspect = w / h; this.camera.position.set(0, 0, dist); this.camera.near = dist * 0.1; this.camera.far = dist * 4;
    this.camera.updateProjectionMatrix();
  }
  load(url) {
    return new Promise(res => this.loader.load(url, t => {
      t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = this.renderer.capabilities.getMaxAnisotropy();
      // no mipmaps: they soften UI text; plain linear filtering stays crisp at the sizes the phones appear
      t.generateMipmaps = false; t.minFilter = THREE.LinearFilter; t.magFilter = THREE.LinearFilter; res(t);
    }, undefined, () => res(null)));
  }
  add(tex) { const p = new Phone(this, tex); this.phones.push(p); return p; }
  render() { this.phones.forEach(p => p.apply()); this.renderer.render(this.scene, this.camera); }
  // on-screen bounding box (CSS px, relative to the canvas) of a phone's front face
  screenRect(p) {
    p.apply(); p.group.updateMatrixWorld();
    const v = new THREE.Vector3(); let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    for (const [x, y] of [[-W / 2, -H / 2], [W / 2, -H / 2], [-W / 2, H / 2], [W / 2, H / 2]]) {
      v.set(x, y, 0).applyMatrix4(p.group.matrixWorld).project(this.camera);
      const sx = (v.x + 1) / 2 * this.w, sy = (1 - v.y) / 2 * this.h;
      x0 = Math.min(x0, sx); x1 = Math.max(x1, sx); y0 = Math.min(y0, sy); y1 = Math.max(y1, sy);
    }
    return { x: x0, y: y0, w: x1 - x0, h: y1 - y0 };
  }
}
