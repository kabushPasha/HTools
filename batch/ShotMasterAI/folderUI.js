
// Select SHOT FOLDER
async function selectShot(shot) {
  handle = shot.handle;
  liElement = shot.liElement;  

  window.currentShot = shot;

  // Clear previous contents
  window.currentFolderHandle = handle;
  document.querySelectorAll('#folders li').forEach(el => el.classList.remove('selected'));
  liElement.classList.add('selected');
  contentsPanel.innerHTML = '';

  // Create the prompt UI and get references to the textarea and status
  const PromptTextArea = await createPromptUI(handle);
  window.PromptTextArea = PromptTextArea;

  await setFirstImage();
  await CreateButtons();
  // --- Tasks collapsible (holds per-task entries) ---
  window.tasksContainer = createTaskContainer(contentsPanel);
  await loadTasksFromDisk(handle, tasksContainer);
  await updateTasksUI();
  //await loadSrcImages(handle, contentsEl);
  await loadMediaFolder(handle, contentsPanel, 'SrcImages');
  await loadMediaFolder(handle, contentsPanel, 'results');
}

// SELECT SCENE FOLDER
async function selectSceneFolder(handle, liElement) {
  window.currentFolderHandle = handle;
  document.querySelectorAll('#folders li').forEach(el => el.classList.remove('selected'));
  contentsPanel.innerHTML = '';

  // Create the prompt UI and get references to the textarea and status
  PromptTextArea = await createPromptUI(handle, "script");
  window.PromptTextArea = PromptTextArea;

  buttonContainer = CreateButtonsContainer();
  SplitIntoShotsBtn = addSimpleButton(buttonContainer, 'split-into-shots-btn', 'Split Into Shots');

  //ImportShotsBtn = addSimpleButton(buttonContainer, 'import-shots-btn', 'Import Shots Clipboard');
  //ImportShotsBtn.addEventListener('click', async () => { await importShotsFromClipboard(); });
}

// ADD Task
window.addKieTask = async (taskId, promptText = '') => {
  console.log('Adding KIE task:', taskId, promptText);
  task = {
    createdAt: new Date().toISOString().slice(0, 19).replace('T', ' '),
    prompt: promptText,
    taskId: taskId,
    status: 'pending'
  }

  if (!Array.isArray(window.tasks)) window.tasks = [];
  window.tasks.push(task);
  saveTasks(window.currentFolderHandle);
  await updateTasksUI();
};

function CreateButtonsContainer()
{
  buttonContainer = document.createElement('div');
  buttonContainer.style.display = 'flex';
  buttonContainer.style.gap = '8px';
  buttonContainer.style.marginTop = '8px';
  contentsPanel.appendChild(buttonContainer);
  return buttonContainer;
}

function addSimpleButton(container, btn, text)
{
  simpleBtn = document.createElement('button');
  simpleBtn.id = btn;
  simpleBtn.textContent = text;
  container.appendChild(simpleBtn);
  return simpleBtn;
}

async function CreateButtons()
{
  buttonContainer = CreateButtonsContainer();
  
  // --- Generate button (KIE.ai) ---
  /*
  const genBtn = document.createElement('button');
  genBtn.id = 'generate-btn';
  genBtn.textContent = 'Text2Img KIE.ai';
  buttonContainer.appendChild(genBtn);
  genBtn.addEventListener('click', async () => {
    const promptText = window.PromptTextArea.value.trim();
    await generateAndSaveImage(promptText,  genBtn);
  });
  */

  // --- Shot Status button ---
  await createShotStatusButton();
  // --- Send Image button (KIE.ai) ---
  sendImageBtn = addSimpleButton(buttonContainer, 'sendimage-btn', 'Send Image to KIE.ai');
  sendImageBtn.addEventListener('click', async () => {
    console.log('Send Image button clicked');
    console.log('First Image Handle:', window.first_src_image_fileHandle);
    if (window.first_src_image_fileHandle) {
      const promptText = window.PromptTextArea.value.trim();
      img_upload_data = await kieUploadFile(window.first_src_image_fileHandle);
      console.log('Image upload data:', img_upload_data.downloadUrl);

      if (img_upload_data && img_upload_data.success)
      {
        kieGenerate_RunwayImg2Video(promptText, img_upload_data.downloadUrl);
      }

    } else {
      console.warn('No first_src_image found');
    }
  });



  createResolveXMLButton = addSimpleButton(buttonContainer, 'create-resolve-xml-btn', 'Generate Resolve FCPXML');
  createResolveXMLButton.addEventListener('click', async () => {    
    const resultsFolder = await window.currentFolderHandle.getDirectoryHandle("results", { create: false });
    await generateFCPXMLFromFolder(resultsFolder);
  }
  );



}

// SHOT STATUS TOGGLE
async function createShotStatusButton()
{
  shotToggleBtn = addSimpleButton(buttonContainer, 'shot-toggle-btn', 'Finished');

  function updateShotStatusButton(shotToggleBtn)
  {
      finished = window.currentShot.shotinfo.finished;
      //shotToggleBtn.textContent = finished ? 'Finished' : 'Progress';
      shotToggleBtn.style.backgroundColor = finished ? 'lightgreen' : 'lightgrey';
  }

  updateShotStatusButton(shotToggleBtn);
  shotToggleBtn.addEventListener('click', () => {
    updateShotStatus(window.currentShot, !window.currentShot.shotinfo.finished);
    updateShotStatusButton(shotToggleBtn);
  });
}

async function setFirstImage()
{
  window.first_src_image_fileHandle = null;
  try{
    const srcImagesHandle = await window.currentFolderHandle.getDirectoryHandle('SrcImages', { create: false });
    for await (const [name, fileHandle] of srcImagesHandle.entries()) {
      if (
        fileHandle.kind === 'file' &&
        /\.(png|jpe?g|gif|webp)$/i.test(name)
      ) {
        if (!window.first_src_image) {
          window.first_src_image_fileHandle = fileHandle;
        }
      }
    }
  } catch {
    //console.log('No SrcImages folder found');
  }
}

async function loadMediaFolder(handle, contentsEl, folderName) {
  try {
    const srcImagesHandle = await handle.getDirectoryHandle(folderName, { create: false });

    const details = document.createElement('details');
    const summary = document.createElement('summary');
    summary.textContent = folderName;
    details.appendChild(summary);
    details.open = true;

    const imagesContainer = document.createElement('div');
    imagesContainer.style.display = 'flex';
    imagesContainer.style.flexWrap = 'wrap';
    imagesContainer.style.gap = '8px';
    imagesContainer.style.marginTop = '8px';

for await (const [name, fileHandle] of srcImagesHandle.entries()) {
  if (fileHandle.kind === 'file') {
    const file = await fileHandle.getFile();
    const url = URL.createObjectURL(file);

    if (/\.(png|jpe?g|gif|webp)$/i.test(name)) {
      const img = document.createElement('img');
      img.src = url;
      img.style.maxWidth = '500px';
      img.style.maxHeight = '500px';
      img.style.objectFit = 'contain';
      img.title = name;
      imagesContainer.appendChild(img);
    }

    if (/\.(mp4|webm|ogg|mov|mkv)$/i.test(name)) {
      const video = document.createElement('video');
      video.src = url;
      video.style.width = 'auto';          // Ensures visibility
      video.style.maxHeight = '500px';
      video.style.objectFit = 'contain';
      video.controls = true;                // Shows play/pause UI
      video.title = name;
      video.autoplay = true;            // Automatically play video
      video.muted = true;               // Required by most browsers for autoplay
      video.controls = true;            // Optional: allow play/pause controls
      video.loop = true;                // Optional: loop video
      imagesContainer.appendChild(video);   // Or use videosContainer      
    }
  }
}

    details.appendChild(imagesContainer);
    contentsEl.appendChild(details);
  } catch {
    // no SrcImages folder
  }
}

async function createPromptUI(handle, name = "prompt") {
  // Create textarea
  const PromptTextArea = document.createElement('textarea');
  PromptTextArea.id = `prompt-area`;
  PromptTextArea.placeholder = 'Enter your prompt here...';
  PromptTextArea.rows = 3;
  contentsPanel.appendChild(PromptTextArea);

  // Load prompt.txt
  try {
    const fileHandle = await handle.getFileHandle(`${name}.txt`, { create: false });
    const file = await fileHandle.getFile();
    const text = await file.text();
    PromptTextArea.value = text;
  } catch {
    PromptTextArea.value = '';
  }

  // Auto-resize
  const autoResize = () => {
    PromptTextArea.style.height = 'auto';
    PromptTextArea.style.height = Math.max(PromptTextArea.scrollHeight, 3 * 16) + 'px';
  };
  PromptTextArea.addEventListener('input', autoResize);
  autoResize();

  // Auto-save (debounced)
  let saveTimeout;
  PromptTextArea.addEventListener('input', () => {
    autoResize();
    clearTimeout(saveTimeout);
    saveTimeout = setTimeout(async () => {
      saveLocalTextFile(handle, `${name}.txt`, PromptTextArea.value);
    }, 500);
  });
  return PromptTextArea;
}

function createTaskContainer(contentsEl) {
  const tasksDetails = document.createElement('details');
  tasksDetails.id = 'tasks-details';
  const tasksSummary = document.createElement('summary');
  tasksSummary.textContent = '🗂️ Tasks';
  tasksDetails.appendChild(tasksSummary);
  tasksDetails.open = true;

  const tasksContainer = document.createElement('div');
  tasksContainer.id = 'tasks-container';
  tasksContainer.style.display = 'flex';
  tasksContainer.style.flexDirection = 'column';
  tasksContainer.style.gap = '6px';
  tasksContainer.style.marginTop = '8px';

  tasksDetails.appendChild(tasksContainer);
  contentsEl.appendChild(tasksDetails);

  return tasksContainer;
}

