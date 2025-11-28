// Event bus to notify shot status updates
//const updateShotStatusBus = new EventTarget();


async function LoadShot(shotName, shotHandle,scene){
  default_shotinfo = {
    finished: false 
  }
  shotinfo = await loadBoundJson(shotHandle, 'shotinfo.json',default_shotinfo);  
  taskinfo = await loadBoundJson(shotHandle, 'tasks.json',{tasks:[]});  

  const shot = { 
        name: shotName,
        handle: shotHandle, 
        shotinfo: shotinfo,
        taskinfo:taskinfo,
        scene:scene,
        // Functions
        async saveShotInfo() {
            await saveBoundJson(this.shotinfo);
        },
        async saveTaskInfo() {
            await saveBoundJson(this.taskinfo);
        },
        async addKieTask(_task) {     
          const task = CreateTask(this).fromTask(_task);
          this.taskinfo.tasks.push(task);
          this.taskinfo.save();
          task.checkResults();
          return task;          
        },
        initializeTasks() {
          const shot = this;  
          const _tasks = []
          for(const task of this.taskinfo.tasks) {
            _tasks.push({...CreateTask(shot),...task});
          }
          this.taskinfo.tasks = _tasks;
        }, 
        async getSrcImageHandle() {
          try{
              if (this.shotinfo.srcImage == null) return null;
              const resultsDir = await this.handle.getDirectoryHandle("results", { create: false });
              const fileHandle = await resultsDir.getFileHandle(this.shotinfo.srcImage, { create: false });
              return fileHandle;
          }
          catch (err){
            
          }
          return null
        },
        async updateEvent() {    
          await this.onUpdateEvent();      
          // Dispatch Shot Update
          const shotUpdateEvent = new CustomEvent("shotupdate", { detail: { shot: this } });
          document.dispatchEvent(shotUpdateEvent);
        },
        async addUpdateCallback(onUpdate){
          // EVENT LISTENERS
          document.addEventListener("shotupdate", (e) => {
              if (e.detail.shot == this){
                onUpdate(e.detail);
              }
          });
        }, 
        // Shot self check update
        async onUpdateEvent() {
          // Check if we have first image
          if (!this.shotinfo.srcImage){
            try {
              dirHandle = await this.handle.getDirectoryHandle("results", { create: false });
              for await (const [name, fileHandle] of dirHandle.entries()) {
                if (fileHandle.kind !== "file") continue;
                if (/\.(png|jpe?g|gif|webp)$/i.test(name)) {
                  this.shotinfo.srcImage = name;
                  await shot.saveShotInfo();
                  return;
                }
              }
            } catch (err) {
              // no folder/images
            }
          }
          // Do other things
        },


    }
    


  shot.initializeTasks();
  return shot;
}

async function LoadScene(sceneName, sceneHandle){
  default_sceneinfo = {
    finished: false,
    description: "",
    location: "",
    shotsjson: "",
    script:"",
    tags: [],
  }          

  sceneinfo = await loadBoundJson(sceneHandle, 'sceneinfo.json',default_sceneinfo);

  const scene = {
    name: sceneName ,
    handle: sceneHandle, 
    shots: [],    
    sceneinfo:sceneinfo,
    // Functions
    async LoadShots() {
      this.shots = []
      for await (const [shotName, shotHandle] of this.handle.entries()) {
        if (shotHandle.kind === 'directory') {
          this.shots.push(await LoadShot(shotName,shotHandle,this));
        }
      } 
    },
    // Add Tag
    async addTag(img) {
      if (!this?.sceneinfo?.tags?.includes(img.path)) { this.sceneinfo.tags.push(img.path); }
      console.log("Scene",this);
      this.sceneinfo.save();
    },
    // Remove Tag
    async removeTag(img) {
    if (!this?.sceneinfo?.tags) return;

    const index = this.sceneinfo.tags.indexOf(img.path);
    if (index !== -1) {
        this.sceneinfo.tags.splice(index, 1); // remove the tag
        console.log("Removed tag:", img.path, "Scene:", this);
        this.sceneinfo.save();
      }
    },
    // Get All Tags
    async getTags(){
      const tags = []
      for(const tag_path of this.sceneinfo.tags) {      
        tags.push(await artbookUI.path2img(tag_path));
      }
      return tags
    },

  }

  await scene.LoadShots()
  return scene
}

async function updateTreeDict() {
  window.treeDict = [];
  window.scenesDirHandle = await rootDirHandle.getDirectoryHandle("Scenes", { create: true } );
  
  for await (const [sceneName, sceneHandle] of window.scenesDirHandle.entries()) {
    if (sceneHandle.kind === 'directory') {
      scene = await LoadScene(sceneName, sceneHandle);
      window.treeDict.push( scene );
    }
  }
  //console.log('Updated treeDict:', window.treeDict);
}

async function updateTreeUI() {
    // Clear existing UI
    foldersEl.innerHTML = ''; 
    // Create Scene elements
    for (const scene of window.treeDict) {        
        sceneLi = await createSceneLI(scene);
        foldersEl.appendChild(sceneLi);
    }
}

async function createShotLI(shot) {
    // ---- Build shot <li> ----
    const shotLi = document.createElement('li');
    shotLi.textContent = shot.name;
    shotLi.style.cursor = 'pointer';
    shotLi.style.display = 'flex';
    shotLi.style.alignItems = 'center';
    shotLi.style.justifyContent = 'space-between';

    const statusIcon = document.createElement('span');
    statusIcon.style.marginLeft = '4px';
    shotLi.appendChild(statusIcon);

    shotLi.addEventListener('click', (e) => {
        e.stopPropagation();
        selectShot(shot);
    });    

    shot.liElement = shotLi;

    shot.updateUI = function(){
        const isCompleted = shot.shotinfo.finished;
        statusIcon.textContent = isCompleted ? '●' : '○';
        statusIcon.style.color = isCompleted ? 'green' : 'grey';

        shot.scene.updateUI?.();
    }

    shot.updateUI();
    return shotLi;
}

async function createShotElements(scene) {
    const shotElements = [];
    for (const shot of scene.shots) {
        shotLi = await createShotLI(shot);
        shotElements.push(shotLi);
    }
    return shotElements;
}

function getFinishedShotCount(scene) {
    return scene.shots.filter(s => s.shotinfo.finished).length;
}

function getTotalShotCount(scene) {
    return scene.shots.length;
}

async function createSceneLI(scene) {
    shotElements = await createShotElements(scene);
    
    // ---- Build scene <li> ----
    const sceneLi = document.createElement('li');
    sceneLi.style.cursor = 'pointer';
    sceneLi.style.display = 'flex';
    sceneLi.style.flexDirection = 'column'; // stack children vertically
    sceneLi.style.alignItems = 'stretch';

    // Header container (scene name + counter)
    const headerDiv = document.createElement('div');
    headerDiv.style.display = 'flex';
    headerDiv.style.justifyContent = 'space-between';
    headerDiv.style.alignItems = 'center';

    const sceneNameSpan = document.createElement('span');
    sceneNameSpan.textContent = scene.name;
    headerDiv.appendChild(sceneNameSpan);

    const counterSpan = document.createElement('span');
    counterSpan.style.color = 'grey';
    headerDiv.appendChild(counterSpan);

    // Subfolders container
    const subfolderUl = document.createElement('ul');
    subfolderUl.style.display = 'none'; // Initially collapsed
    //console.log("shotElements:", shotElements);    
    shotElements.forEach(el => subfolderUl.appendChild(el));

    // Toggle show/hide on scene click + call selection
    headerDiv.addEventListener('click', () => {
        selectSceneFolder(scene);
        // Disabled showing shots - might return later
        //const isCollapsed = subfolderUl.style.display === 'none';
        //subfolderUl.style.display = isCollapsed ? 'block' : 'none';
    });

    // Append header and shot list
    sceneLi.appendChild(headerDiv);    
    sceneLi.appendChild(subfolderUl);
    scene.liElement = sceneLi;

    scene.updateUI = function(){
        finishedShots = getFinishedShotCount(scene);
        totalShots = getTotalShotCount(scene);  
        counterSpan.textContent = `${finishedShots}/${totalShots}`;
    }
    scene.updateUI();

    return sceneLi;
}

// LIST FOLDERS
async function listFolders() {  
  await updateTreeDict();
  await updateTreeUI(); 
  await readArtbookData();
  //console.log(window.treeDict);
}

// Status bar helper
function updateStatus(message) {
  if (statusBar) {
    statusBar.textContent = message;
  }
  console.log(message);
}

window.updateStatus = updateStatus;

async function updateShotStatus(shot,status) {
    if (status != shot.shotinfo.finished){
        shot.shotinfo.finished  = status;
        shot.updateUI();        
        saveBoundJson(shot.shotinfo);
    }
}





