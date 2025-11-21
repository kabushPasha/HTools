

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
        console.log("Checking results",shot,task);
        await checkTaskResults(task);       
        saveBoundJson(shot.taskinfo);
        // SAVE RESULTS MAYBE  ??
      } catch (err) {
        console.error('Task check failed', err);
      }
    });
    taskEl.appendChild(chkBtn);
    // prepend latest task
    container.appendChild(taskEl);
  }

  container.init = function() {
    console.log("Initialize TASK container");
    for (const task of shot.taskinfo.tasks) {
      console.log("TASK:",task);
      container.addTask(task);
    }
  }
  
  container.init()
  return container;
}

// ADD Task to shot
async function addKieTask(taskId, shot) {
  console.log('Adding KIE task:', taskId, shot);
  task = {
    createdAt: new Date().toISOString().slice(0, 19).replace('T', ' '),
    prompt: shot.shotinfo.prompt,
    taskId: taskId,
    status: 'pending'
  }

  shot.taskinfo.tasks.push(task);
  saveBoundJson(shot.taskinfo);
  return task;
};