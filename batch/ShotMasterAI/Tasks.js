

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
        //console.log("Checking results",shot,task);
        // First check if we have generated urls
        // also update the status based on status from response
        await task.checkResults();

        // Update Status  change to a function??
        statusIndicator.style.backgroundColor = task.status == 'downloaded' ? '#44ff44' : '#ff4444' ;
      } catch (err) {
        console.error('Task check failed', err);
      }
    });
    taskEl.appendChild(chkBtn);

    // Test Button
    const testBtn = document.createElement('button');
    testBtn.textContent = 'LOG TASK';
    testBtn.addEventListener('click', async () => {
      console.log(task);
      console.log(task.getShot());
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

function CreateTask(shot) {
  task = {
    //example_field : "update",    
    // Functions 
    resultUrls : [],
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

      task.status = "downloaded";
      task.finished = true;
      // Update Status
      await saveBoundJson(shot.taskinfo);
    }, 

  async checkResults(timeout = 1000, maxRetries = 2) {
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
  }
  return task;
}
