import * as THREE from 'three';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
camera.position.z = 5;
camera.position.y = 1;

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );

document.body.appendChild( renderer.domElement );


function createCube(scene = null){
    const geometry = new THREE.BoxGeometry( 1, 1, 1 );
    const material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
    const cube = new THREE.Mesh( geometry, material );
    if (scene) scene.add( cube );
    return cube;
}

const cube = createCube(scene);

/*
function animate() {
  renderer.render( scene, camera );

  const delta = clock.getDelta();
  controls.update(delta);

  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
}
renderer.setAnimationLoop( animate );
*/


// Handle window resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();

  renderer.setSize(window.innerWidth, window.innerHeight);
  controls.handleResize();
});





// --- 1. Create controls ---
const controls = new PointerLockControls(camera, document.body);

// --- 2. Click to lock the pointer ---
document.addEventListener('click', () => {
  controls.lock();
});


// --- 3. Movement flags ---
const keys = {};
document.addEventListener('keydown', e => (keys[e.code] = true));
document.addEventListener('keyup', e => (keys[e.code] = false));

const velocity = new THREE.Vector3();
const speed = 5;

const clock = new THREE.Clock();

// --- 4. Render loop ---
function animate() {
  requestAnimationFrame(animate);

  const dt = clock.getDelta();

  if (controls.isLocked) {
    velocity.set(0, 0, 0);

    if (keys['KeyW']) velocity.z -= speed * dt;
    if (keys['KeyS']) velocity.z += speed * dt;
    if (keys['KeyA']) velocity.x -= speed * dt;
    if (keys['KeyD']) velocity.x += speed * dt;

    controls.moveRight(velocity.x);
    controls.moveForward(-velocity.z);
  }

  renderer.render(scene, camera);
}

animate();

// Create a crosshair div
const crosshair = document.createElement('div');
crosshair.style.position = 'fixed';
crosshair.style.top = '50%';
crosshair.style.left = '50%';
crosshair.style.width = '6px';
crosshair.style.height = '6px';
crosshair.style.background = 'white';
crosshair.style.borderRadius = '50%';
crosshair.style.transform = 'translate(-50%, -50%)';
crosshair.style.pointerEvents = 'none'; // so it won't block clicks
crosshair.style.zIndex = '9999';

// Add it to the body
document.body.appendChild(crosshair);



function createInfiniteFloor({
  size = 1000,          // overall plane size
  textureUrl = null,    // optional texture
  color = 0x808080,     // fallback color
  repeat = 100          // how many times the texture repeats
} = {}) {
  let material;

  if (textureUrl) {
    const textureLoader = new THREE.TextureLoader();
    const texture = textureLoader.load(textureUrl);
    texture.wrapS = THREE.RepeatWrapping;
    texture.wrapT = THREE.RepeatWrapping;
    texture.repeat.set(repeat, repeat);
    material = new THREE.MeshStandardMaterial({ map: texture });
  } else {
    material = new THREE.MeshStandardMaterial({ color });
  }

  const geometry = new THREE.PlaneGeometry(size, size);
  const floor = new THREE.Mesh(geometry, material);
  floor.rotation.x = -Math.PI / 2;  // rotate to lie flat
  floor.receiveShadow = true;

  return floor;
}

// Assuming scene is already created
const floor = createInfiniteFloor({
  size: 2000,
  color: 0x808080,// grey color
  repeat: 200
});
scene.add(floor);