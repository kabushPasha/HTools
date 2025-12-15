import * as THREE from 'three';
import { playSound } from "./sounds.js";

// Move this part
export function createSpawnGrid(sizex = 3, sizey = 3) {
    const grid = {
      positions:[],
      init(sizex,sizey) {
        this.positions = [];
        const stepX = 1 / sizex;
        const stepY = 1 / sizey;
        const halfX = 1 / 2;
        const halfY = 1 / 2;
        for (let i = 0; i < sizex; i++) {
            for (let j = 0; j < sizey; j++) {
                const posX = -halfX + stepX / 2 + i * stepX;
                const posY = -halfY + stepY / 2 + j * stepY;
                const posZ = 1 * 0.5;
                this.positions.push({pos : new THREE.Vector3(posX, posY, posZ), item : null});
            }
        }
      },
      getFreeCell() {
          const freePositions = this.positions.filter(p => p.item === null);          
          if (freePositions.length === 0) return null; // no free positions
          const index = Math.floor(Math.random() * freePositions.length);
          return freePositions[index];
      },
    }         
    grid.init(sizex, sizey)
    return grid
};

export function createSimpleBoard(data = null){
  const simpleBoard = {
    scene : null,
    position : new THREE.Vector3(0,0,0),
    size : new THREE.Vector3(1,1,0.05),
    Loop : null, 
    targets: [],
    createGeo(){
      const geometry = new THREE.BoxGeometry( this.size.x,this.size.y,this.size.z);    
      const material = new THREE.MeshBasicMaterial( { color: 'grey'} );
      const board = new THREE.Mesh( geometry, material );

      if (this.scene) this.scene.add(board);
      if (this.Loop) this.Loop.add(board);

      board.position.copy(this.position);

      board.onHit = function(){
        playSound("SphereShooter/sfx/bullet-board.mp3",0.4)
      }      
      this.mesh = board;
      return this
    },
    getRandomPosition(){
      return new THREE.Vector3((Math.random() - 0.5) * (this.size.x),(Math.random() - 0.5) * (this.size.y),this.size.z*0.5)
    },
    createTarget(){
      const board = this;
      const target = createTarget({
        parent :this.mesh, 
        position: this.getRandomPosition(),
        onHit : function() {
          this.position.copy( board.getRandomPosition());
        },
        Loop : this.Loop,
      });
      board.targets.push(target);  
    },
    createTargets(n){
      for( let i =0;i<n;i++)    {
        this.createTarget();
      }
    },
    init(data){
      Object.assign(this, data);
      return this;
    }
  }  

  if (data) simpleBoard.init(data);
  return simpleBoard;
}

export function createGridBoard(data){
    const GridBoard = {
      gridx : 3,
      gridy : 3,
      spawnGrid : createSpawnGrid(3,3),
      createTarget()
      {
        const board = this;
        const freeGridCell = board.spawnGrid.getFreeCell()    

        const target = createTarget({
          parent : board.mesh, 
          position: freeGridCell.pos.clone().multiply( board.size ),        
          onHit : function() {
            const freeCell =  board.spawnGrid.getFreeCell();
            this.position.copy(freeCell.pos.clone().multiply(board.size));  
            this.cell.item = null
            this.cell = freeCell
            freeCell.item = this
            playSound("SphereShooter/sfx/bullet-metal-hit.mp3",0.2)
          }
        },data.Loop);
        target.cell = freeGridCell
        freeGridCell.item = target
      },    
      createTargets(n){
        for( let i =0;i<n;i++)    {
          this.createTarget();
        }
      },      
    }    

    const board = createSimpleBoard().init(GridBoard);   
    if (data) board.init(data);
    return board;
}




export function createTarget( {parent = null,position = new THREE.Vector3(0,0,0), onHit = () => {}, Loop = null} = {}){    

    const geometry = new THREE.SphereGeometry( 1,36 , 18 );
    const material = new THREE.MeshBasicMaterial( { color: 'green'} );
    const target = new THREE.Mesh( geometry, material );
    if (parent) parent.add( target );
    target.position.copy(position);

    target.tick = function(dt){
    }

    target.onHit = function(){
      onHit.call(this);
    }

    target.scale.setScalar(0.5);

    if (Loop) Loop.add(target);
    return target;
}
// move end
