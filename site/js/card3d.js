// 3D Trovy card (Trovy case study, Context slide). Loads the GLB into .tv-card3d over a CSS gradient tile.
// Floats gently and leans toward the pointer; a tap/click (or Enter/Space) spins it a full turn so the back shows.
// Renders only while its slide is on screen. Until the model is ready (or without WebGL) the flat PNG shows.
import * as THREE from 'three';
import { GLTFLoader } from './vendor/GLTFLoader.js';
import { RoomEnvironment } from './vendor/RoomEnvironment.js';

const slot = document.querySelector('.tv-card3d');
if (slot) init(slot);

function init(slot) {
  const canvas = slot.querySelector('canvas');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true }); } catch (e) { return; }
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  // no filmic tone mapping: it washes the gold out to cream
  renderer.toneMapping = THREE.NoToneMapping;
  const ENV = 0.55, KEY = 1.2;                              // tuned against the card render
  renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(renderer), 0.04).texture;
  const key = new THREE.DirectionalLight(0xfff4e0, KEY); key.position.set(-4, 6, 8); scene.add(key);

  const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);
  camera.position.set(0, 0, 23);

  // pivot: spin (y) and pointer lean live on separate groups so they add up
  const lean = new THREE.Group(), spin = new THREE.Group();
  lean.add(spin); scene.add(lean);
  const REST = { x: -0.32, y: 0.38, z: 0.2 };               // the tilt of the original PNG
  lean.rotation.set(REST.x, REST.y, REST.z);

  const base = document.body.dataset.base || '';
  new GLTFLoader().load(base + slot.dataset.glb, gltf => {
    const card = gltf.scene;
    card.traverse(o => { if (o.isMesh) { o.material.envMapIntensity = ENV; } });
    spin.add(card);
    slot.classList.add('is-3d');
    dirty = true;
  });

  // sizing: the slot sits inside a scaled art board, so measure its real pixels
  let dirty = true;
  function size() {
    const r = slot.getBoundingClientRect();
    if (!r.width) return;
    const dpr = Math.min(2, devicePixelRatio || 1);
    renderer.setPixelRatio(dpr);
    renderer.setSize(r.width, r.height, false);
    camera.aspect = r.width / r.height; camera.updateProjectionMatrix();
    dirty = true;
  }
  new ResizeObserver(size).observe(slot);
  addEventListener('resize', size);

  // pointer lean
  const target = { x: 0, y: 0 }, cur = { x: 0, y: 0 };
  slot.addEventListener('pointermove', e => {
    const r = slot.getBoundingClientRect();
    target.x = ((e.clientY - r.top) / r.height - 0.5) * 0.35;
    target.y = ((e.clientX - r.left) / r.width - 0.5) * 0.5;
  });
  slot.addEventListener('pointerleave', () => { target.x = 0; target.y = 0; });

  // tap to spin: one full turn, eased; taps during a spin queue another turn
  let spinning = null;
  function spinOnce() {
    slot.classList.add('spun');
    const to = (spinning ? spinning.vars.y : spin.rotation.y) + Math.PI * 2;
    if (spinning) spinning.kill();
    spinning = gsap.to(spin.rotation, { y: to, duration: reduced ? 0.01 : 1.6, ease: 'power3.inOut',
      onUpdate: () => { dirty = true; }, onComplete: () => { spin.rotation.y %= Math.PI * 2; spinning = null; } });
  }
  slot.addEventListener('click', spinOnce);

  const slide = slot.closest('.cs-slide');
  const visible = () => document.body.classList.contains('is-stack')
    ? slot.getBoundingClientRect().bottom > 0 && slot.getBoundingClientRect().top < innerHeight
    : slide && slide.classList.contains('on');
  const t0 = performance.now();
  gsap.ticker.add(() => {
    if (!visible()) return;
    if (!canvas.width) size();
    const t = (performance.now() - t0) / 1000;
    cur.x += (target.x - cur.x) * 0.08; cur.y += (target.y - cur.y) * 0.08;
    const bob = reduced ? 0 : Math.sin(t * 1.1) * 0.12;
    lean.rotation.set(REST.x + cur.x + (reduced ? 0 : Math.sin(t * 0.7) * 0.03), REST.y + cur.y, REST.z);
    lean.position.y = bob;
    renderer.render(scene, camera);
    dirty = false;
  });
}
