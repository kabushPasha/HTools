import * as THREE from 'three';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';

// Create LOOP
const Loop = {
  objects : [],
  renderer : null,
  clock: new THREE.Clock(),
  add(obj) {
    this.objects.push(obj);
  },  
  tick() {
    requestAnimationFrame(() => this.tick());     
    const dt = this.clock.getDelta();
    this.objects.forEach(obj => obj?.tick?.(dt));
    this.renderer?.draw?.();
  }
}
//Create Render
function createRender({ camera = null , scene = null}){
  // Create Renderer
  const renderer = new THREE.WebGLRenderer();
  document.body.appendChild( renderer.domElement );

  renderer.camera = camera;
  renderer.scene = scene;

  renderer.draw = function() { this.render(this.scene, this.camera);}

  renderer.updateSize = function() {
    this.setSize(window.innerWidth, window.innerHeight);
    this.setPixelRatio(Math.min(window.devicePixelRatio,2));
    if (this.camera){
      this.camera.aspect = window.innerWidth / window.innerHeight;
      this.camera.updateProjectionMatrix();
    }
  } 

  // Handlers
  // Handle window resize
  window.addEventListener('resize', () => {  renderer.updateSize()  });

  // Init Funcitons
  renderer.updateSize();

  return renderer
}
// Create Cube
function createCube(scene = null){
    const geometry = new THREE.BoxGeometry( 1, 1, 1 );
    const material = new THREE.MeshBasicMaterial( { color: 'red' } );
    const cube = new THREE.Mesh( geometry, material );
    if (scene) scene.add( cube );

    cube.tick = function(dt){
      const time = performance.now() / 1000;
      this.position.y = Math.sin(time); 
    }

    Loop.add(cube);
    return cube;
}
// Create Controls
function createFPSControls(){
  const controls = new PointerLockControls(camera, document.body);
  // --- 2. Click to lock the pointer ---
  document.addEventListener('click', () => { controls.lock();});

  // --- 3. Movement flags ---
  const keys = {};
  document.addEventListener('keydown', e => (keys[e.code] = true));
  document.addEventListener('keyup', e => (keys[e.code] = false));
  const velocity = new THREE.Vector3();
  const speed = 5;

  controls.tick = (dt) => {
      if (controls.isLocked) {
      velocity.set(0, 0, 0);
      if (keys['KeyW']) velocity.z -= speed * dt;
      if (keys['KeyS']) velocity.z += speed * dt;
      if (keys['KeyA']) velocity.x -= speed * dt;
      if (keys['KeyD']) velocity.x += speed * dt;

      controls.moveRight(velocity.x);
      controls.moveForward(-velocity.z);
    }
  }
  return controls
}
// Create a crosshair div
function createCrosshair(){
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
}


// Create scene
const scene = new THREE.Scene();

// Create Camera
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
camera.position.z = 5;
camera.position.y = 1;

Loop.renderer = createRender({camera, scene});

const controls = createFPSControls();
Loop.add(controls);

const cube = createCube(scene);

Loop.tick()

createCrosshair();





// ----------------- Other Functions ----------------
// Create Axes Helper
const axesHelper = new THREE.AxesHelper()
scene.add(axesHelper)
//Create Group
const group = new THREE.Group();
//group.add()
scene.add(group)


// Lesson 8