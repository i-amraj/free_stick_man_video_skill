/**
 * Procedural 3D Room Builder — GrowKaz Stickman Studio
 * Generates stylized 3D rooms (Mystery Noir, Tech Server, Minimal Studio) using Three.js
 */

export class RoomBuilder {
  constructor(container, width = 1080, height = 1920) {
    this.container = typeof container === 'string' ? document.querySelector(container) : container;
    this.width = width;
    this.height = height;
  }

  buildMysteryRoom(THREE) {
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0a0e1a, 0.045);

    const camera = new THREE.PerspectiveCamera(40, this.width / this.height, 0.1, 100);
    camera.position.set(0, 3.2, 8.5);
    camera.lookAt(0, 1.2, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    renderer.setSize(this.width, this.height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.container.appendChild(renderer.domElement);

    // Floor
    const floor = new THREE.Mesh(
      new THREE.PlaneGeometry(24, 24),
      new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.6, metalness: 0.2 })
    );
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    scene.add(floor);

    // Walls
    const wallMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.8 });
    const backWall = new THREE.Mesh(new THREE.PlaneGeometry(24, 14), wallMat);
    backWall.position.set(0, 7, -6);
    backWall.receiveShadow = true;
    scene.add(backWall);

    // Desk
    const desk = new THREE.Mesh(
      new THREE.BoxGeometry(4.2, 0.16, 2.2),
      new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.5 })
    );
    desk.position.set(0, 1.4, 0);
    desk.castShadow = true;
    desk.receiveShadow = true;
    scene.add(desk);

    // Dramatic Lights
    const keyLight = new THREE.SpotLight(0x38bdf8, 3.5, 20, Math.PI / 3, 0.4);
    keyLight.position.set(-2, 7, 3);
    keyLight.castShadow = true;
    scene.add(keyLight);

    const rimLight = new THREE.DirectionalLight(0xec4899, 1.2);
    rimLight.position.set(4, 5, -3);
    scene.add(rimLight);

    scene.add(new THREE.AmbientLight(0x0a0f1d, 1.0));

    return { scene, camera, renderer };
  }
}

