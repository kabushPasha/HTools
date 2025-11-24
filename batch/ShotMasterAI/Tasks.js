

// Task Container
async function createTaskContainer(shot,parent = null){
  const container = createCollapsibleContainer("tasks",parent);

  container.addTask = function(task){
    // create task UI element
    const taskEl = document.createElement('div');
    taskEl.className = 'kie-task';
    taskEl.style.display = 'flex';
    taskEl.style.alignItems = 'center';
    taskEl.style.gap = '8px';

    // Create timestamp label
    const label = document.createElement('div');
    label.style.flex = '1';
    label.textContent = `${task.createdAt}`;
    taskEl.appendChild(label);    


    // NEW: status text before icon
    const statusText = document.createElement('div');
    statusText.style.minWidth = '180px';
    statusText.textContent = 'Idle';
    statusText.style.color = "#888";     // light grey text
    statusText.style.fontSize = "12px";  // optional: smaller
    taskEl.appendChild(statusText);
    
    // Create status indicator
    const statusIndicator = document.createElement('div');
    statusIndicator.style.width = '12px';
    statusIndicator.style.height = '12px';
    statusIndicator.style.borderRadius = '50%';
    statusIndicator.style.backgroundColor = task.status == 'downloaded' ? '#44ff44' : '#ff4444' ;
    statusIndicator.title = 'Not downloaded';
    taskEl.appendChild(statusIndicator);

    // Create Button to check results
    const chkBtn = document.createElement('button');
    chkBtn.textContent = 'Check Results';
    chkBtn.addEventListener('click', async () => {
      try {
        await task.checkResults();
      } catch (err) {
        console.error('Task check failed', err);
      }
    });
    taskEl.appendChild(chkBtn);

    taskEl.update = async function(){
      statusIndicator.style.backgroundColor = task.status == EnumShotStatus.finished ? '#44ff44' : '#ff4444' ;
      statusText.textContent = task.status;
    }
    taskEl.update();
    task.addUpdateCallback( (data) => { taskEl.update();})

    // Test Button
    const testBtn = document.createElement('button');
    testBtn.textContent = 'LOG';
    testBtn.addEventListener('click', async () => {
      console.log("TASK: ",task);
      console.log("SHOT: ",task.getShot());
    });
    taskEl.appendChild(testBtn);


    // prepend latest task
    container.appendChild(taskEl);
  }

  container.init = function() {
    //console.log("Initialize TASK container");
    for (const task of shot.taskinfo.tasks) {
      //console.log("TASK:",task);
      container.addTask(task);
    }
  }
  
  container.init()
  return container;
}

const EnumShotStatus = {
  idle : "idle",
  checking : "checking",
  downloading : "downloading",
  finished : "finished",
}

function CreateTask(shot) {
  task = {
    //example_field : "update",    
    // Functions 
    resultUrls : [],
    status : "idle",

    getShot() {return shot},

    fromTask(_task) {
      Object.assign(this, _task);
      return this;
    },
    // Save Results To Disk
    async saveResults() {
      const task = this;
      const shot = task.getShot()
      console.log('Saving result images:', task.resultUrls);      

      const resultsHandle = await shot.handle.getDirectoryHandle(task.outputFolder, { create: true });

      if (task.resultUrls == null) {
        console.log("RESULT URLS IS EMPTY")
        return
      }

      this.setStatus(EnumShotStatus.downloading)      
      for (const url of task.resultUrls) {        
          const urlObj = new URL(url);
          const urlPath = urlObj.pathname;
          const fileName = urlPath.split('/').pop();
        
          try {
            await resultsHandle.getFileHandle(fileName);
            console.log("File alreay exists", fileName)
            continue
          } catch (e) {
            // File does not exist, which is expected
          }

          const response = await fetch(url);
          const blob = await response.blob();

          const fileHandle = await resultsHandle.getFileHandle(fileName, { create: true });
          const writable = await fileHandle.createWritable();
          await writable.write(blob);
          await writable.close();
      }

      //task.status = "downloaded";
      task.setStatus(EnumShotStatus.finished)
      task.finished = true;
      // Update Status
      await shot.taskinfo.save();
      await shot.updateEvent(); 
    }, 

    async checkResults(timeout = 5000, maxRetries = 100) {
        this.setStatus(EnumShotStatus.checking)
        let retries = 0;

        while (retries < maxRetries) {
          await checkTaskResults(this);
          if (this.resultUrls.length > 0) {
            await this.saveResults();
            break;
          }

          // Retry
          await new Promise(resolve => setTimeout(resolve, timeout));
          retries++;
          console.log(`Waiting for results... attempt ${retries}`);
        }
        
    },

    async setStatus(status) {
      this.status = status;
      this.updateEvent();
    },

    // Event Functions
    async updateEvent() {          
      // Dispatch Shot Update
      const taskUpdateEvent = new CustomEvent("taskupdate", { detail: { task: this } });
      document.dispatchEvent(taskUpdateEvent);
    },
    async addUpdateCallback(onUpdate){
      // EVENT LISTENERS
      document.addEventListener("taskupdate", (e) => {
          if (e.detail.task.taskId == this.taskId){
            onUpdate(e.detail);
          }
      });
    },

  }
  return task;
}
