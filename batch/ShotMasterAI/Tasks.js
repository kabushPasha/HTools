


 // ------------------------------------------------------------------
// loadTasksFromDisk (unchanged)
// ------------------------------------------------------------------
async function loadTasksFromDisk(folder_handle) {
    window.tasks = [];
  try {
    const fileHandle = await folder_handle.getFileHandle('tasks.json', { create: false });
    const file = await fileHandle.getFile();
    const text = await file.text();
    const tasks = JSON.parse(text);

    window.tasks = tasks; 
    } catch {
    }
}

async function updateTasksUI() {
    window.tasksContainer.innerHTML = '';   
    for (const task of window.tasks) {
      await AddTaskToUI(task);
    }
}


async function AddTaskToUI(task) {
    //console.log('Loaded task:', task);

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
        const res = await window.checkTaskResults(task.taskId, msg => {});     
        console.log('Task check results:', res);   
        if (res && res.ok && res.resultUrls && res.resultUrls.length > 0) {
          statusIndicator.style.backgroundColor = '#44ff44'; // green = downloaded
          statusIndicator.title = 'Downloaded';          
          task.status = 'downloaded';
          saveTasks(window.currentFolderHandle);
        }        
      } catch (err) {
        console.error('Task check failed', err);
      }

      console.log(window.tasks);
    });
    taskEl.appendChild(chkBtn);
    // prepend latest task
    window.tasksContainer.prepend(taskEl);

  /*
    // Format timestamp with dashes (YYYY-MM-DD HH:MM:SS)
    const now = new Date();
    const timestamp = now.toISOString().slice(0, 19).replace('T', ' ');
    */
}


// ------------------------------------------------------------------
// Helper: save/update tasks.json
// ------------------------------------------------------------------
async function saveTasks(dirHandle) {
  // Save back to tasks.json
  try {
    const fileHandle = await dirHandle.getFileHandle('tasks.json', { create: true });
    const writable = await fileHandle.createWritable();
    await writable.write(JSON.stringify(window.tasks, null, 2));
    await writable.close();
  } catch (err) {
    console.error('Failed to write tasks.json', err);
  }
}
