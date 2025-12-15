import * as THREE from 'three';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';
import * as dat from 'dat.gui'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import * as targets from "./targets.js";
import { playSound } from "./sounds.js";
import Stats from "three/addons/libs/stats.module.js";

const stats = new Stats();
document.body.appendChild(stats.dom);

// Loading Managar
const loadingManager = new THREE.LoadingManager()

// IMPORTING IMAGES
const textureLoader = new THREE.TextureLoader(loadingManager)


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
    stats.update();
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
    const geometry = new THREE.SphereGeometry( 1,36 , 18 );
    const material = new THREE.MeshBasicMaterial( { color: 'grey',map:colorTexture} );
    material.map = colorTexture;
    const cube = new THREE.Mesh( geometry, material );
    if (scene) scene.add( cube );

    cube.tick = function(dt){
      const time = performance.now() / 1000;
      this.position.y = Math.sin(time); 
    }

    cube.onHit = function(){

      this.position.add(new THREE.Vector3().randomDirection().multiplyScalar(3));
      this.position.normalize().multiplyScalar(3);
      //this.position.set(this.position.normalize().multiplyScalar(5));

    }

    cube.scale.setScalar(0.2);

    Loop.add(cube);
    return cube;
}

// Create Controls
function createFPSControls(){
  const controls = new PointerLockControls(camera, document.body);
  // --- 2. Click to lock the pointer ---
  document.addEventListener('click', () => { 
    if (!controls.isLocked) controls.lock();
  });

  controls.pointerSpeed = 0.2;

  // --- 3. Movement flags ---
  const keys = {};
  document.addEventListener('keydown', e => (keys[e.code] = true));
  document.addEventListener('keyup', e => (keys[e.code] = false));
  const velocity = new THREE.Vector3();
  const speed = 5;

  /*
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
  */
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

// ------------------ MAIN ------------------- 
const scene = new THREE.Scene();

// Create Camera
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
camera.position.y = 1;

Loop.renderer = createRender({camera, scene});

const controls = createFPSControls();
Loop.add(controls);

//const cube = createCube(scene);

Loop.tick()

createCrosshair();



// ---------- RAYCASTER ----------
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
window.addEventListener('click', raycastAgainstTarget, false);

function raycastAgainstTarget() {
    // Raycast straight from the camera forward
    raycaster.set(camera.getWorldPosition(new THREE.Vector3()), camera.getWorldDirection(new THREE.Vector3()));

    // Intersect with objects
    const intersects = raycaster.intersectObjects(scene.children, true);

    playSound("SphereShooter/sfx/awp-shoot-sound-effect-cs_go.mp3");
    if (intersects.length > 0) {
        const hit = intersects[0].object;
        hit.onHit?.();
    }
    else{
      playSound("SphereShooter/sfx/bullet_miss.mp3",0.2)
    }
}

/*
const lazer = {
  tick() {
    raycastAgainstTarget();
  }
}
Loop.add(lazer);
*/

// ----------------- Other Functions ----------------
// Create Axes Helper
/*
const axesHelper = new THREE.AxesHelper()
scene.add(axesHelper)
//Create Group
const group = new THREE.Group();
//group.add()
scene.add(group)
*/



// Load Pighead
/*
const loader = new GLTFLoader();
const gltf = await loader.loadAsync( '/SphereShooter/models/pig/pig.gltf');
console.log("IMPORTED",gltf.scene);
gltf.scene.scale.setScalar(1);
scene.add( gltf.scene );
*/

//  -------------------  Lights -----------------
// Ambient light (soft global light)
//const ambientLight = new THREE.AmbientLight(0xffffff, 0.4); 
//scene.add(ambientLight);

// Directional light (like sunlight)
//const dirLight = new THREE.DirectionalLight(0xffffff, 1);
//dirLight.position.set(5, 10, 5);  // position the light
//scene.add(dirLight);



// HDRI
textureLoader.load("SphereShooter/textures/hdri/clouds.jpg", function(texture) {
    texture.mapping = THREE.EquirectangularReflectionMapping;
    scene.background = texture;
    scene.environment = texture;
});


// Scene Building
targets.createGridBoard({
  scene,
  position:new THREE.Vector3(0,1,-5),
  size :new THREE.Vector3(4,4,0.05),
}).createGeo().createTargets(3);





// --------Debug Control Panel -------------------
const gui = new dat.GUI()
gui.add(controls,"pointerSpeed",0.0001,1).step(0.01).name("Sensetivity")



//gui.add( cube.position , 'x' , -3,3).step(0.01).name("Cube_X");
//gui.add(cube,"visible")
//gui.add(cube.material,"wireframe").onChange( () => {console.log("callback")})
//const debug_functions = { test_log() { console.log("test"); }};
//gui.add(debug_functions,"test_log")

/*
const moves = {};
document.addEventListener('mousemove', (event) => {
    const moveSquared = event.movementX ** 2 + event.movementY ** 2;

    if (moveSquared in moves) {
        moves[moveSquared] += 1;
    } else {
        moves[moveSquared] = 1;
    }

    console.log(moves);
});


*/