
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
  await CreateShotInfoCardButtons(shot,parent = contentsPanel);
  // --- Tasks collapsible (holds per-task entries) ---
  window.tasksContainer = createTaskContainer(contentsPanel);
  await loadTasksFromDisk(handle, tasksContainer);
  await updateTasksUI();
  //await loadSrcImages(handle, contentsEl);
  await loadMediaFolder(handle, contentsPanel, 'SrcImages');
  await loadMediaFolder(handle, contentsPanel, 'results');
}
// SELECT SCENE FOLDER
async function selectSceneFolder(scene) {
  window.currentFolderHandle = scene.handle;
  document.querySelectorAll('#folders li').forEach(el => el.classList.remove('selected'));
  contentsPanel.innerHTML = '';

  // Create scene elements in contents panel
  // Create the prompt UI and get references to the textarea and status

  const sceneSettingsContainer = document.createElement('div');

  await createPromptUI(scene.handle, "script",parent = sceneSettingsContainer);

  buttonContainer = CreateButtonsContainer(parent = sceneSettingsContainer);
  SplitIntoShotsBtn = addSimpleButton('split-into-shots-btn', 'Split Into Shots',buttonContainer);

  // Currently not used button
  //ImportShotsBtn = addSimpleButton(buttonContainer, 'import-shots-btn', 'Import Shots Clipboard');
  //ImportShotsBtn.addEventListener('click', async () => { await importShotsFromClipboard(); });

  shotPreviewStrip = await createShotPreviews(scene);

  const tabs1 = createTabContainer(contentsPanel);
  tabs1.addTab({ title: 'Scene', content: sceneSettingsContainer });
  tabs1.addTab({ title: 'Shots', content: shotPreviewStrip }); 
}

// Create Shot Info Element (Prompt etc)
async function CreateShotInfoElement(shot,parent = null) {
  container = document.createElement('div');
  container.classList.add('shot-info'); 

  // --- Shot name ---
  const title = document.createElement('div');
  title.textContent = shot.name;
  title.classList.add('shot-info-title');  // optional CSS class
  container.appendChild(title);

  // --- Prompt TextArea ---
  PromptTextArea = await createPromptUI(shot.handle, "prompt", container);
  
  CreateShotInfoCardButtons(shot,container);

  // Append to parent
  if (parent) parent.appendChild(container);
  return container;
}

// Create Shot Previews with horizontal scroll and stretched shot boxes
async function createShotPreviews(scene) {
  const container = document.createElement('div');

  resizableArea = createResizableContainer(parent = container);
  shotsStrip = createHorizontalContainer(resizableArea)

  // --- Create and append each shot preview ---
  for (const shot of scene.shots) {
    const shotElement = await CreateShotPreview(shot);
    shotsStrip.appendChild(shotElement);
    const shot_info = await CreateShotInfoElement(shot, parent = container);
    shot_info.style.display = 'none';

    // --- Add click event to show corresponding info ---
    shotElement.addEventListener('click', () => {
      document.querySelectorAll('.shot-info').forEach(el => el.style.display = 'none');
      shot_info.style.display = 'block';
    });
  }
  return container;
}

async function CreateShotPreview(shot) {
  // Container for the shot
  const container = document.createElement("div");
  container.classList.add("shot-preview");

  // Image element
  const img = document.createElement("img");
  img.src = shot.image || "https://picsum.photos/id/237/200/300";
  container.appendChild(img);

  // Label
  const label = document.createElement("div");
  label.textContent = shot.name;
  label.classList.add("shot-preview-label");
  container.appendChild(label);

  return container;
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

function CreateButtonsContainer(parent = null) {
  const buttonContainer = document.createElement('div');
  buttonContainer.classList.add('buttons-container'); // CSS handles all styling
  if (parent) parent.appendChild(buttonContainer);
  return buttonContainer;
}
function addSimpleButton(btn, text, parent = null)
{
  simpleBtn = document.createElement('button');
  simpleBtn.id = btn;
  simpleBtn.textContent = text;
  if (parent) {parent.appendChild(simpleBtn);}
  return simpleBtn;
}

async function CreateShotInfoCardButtons(shot,parent = null)
{
  buttonContainer = CreateButtonsContainer(parent);
  
  /*
  // --- Generate button (KIE.ai) ---
  const genBtn = document.createElement('button');
  genBtn.id = 'generate-btn';
  genBtn.textContent = 'Text2Img KIE.ai';
  buttonContainer.appendChild(genBtn);
  genBtn.addEventListener('click', async () => {
    const promptText = window.PromptTextArea.value.trim();
    await generateAndSaveImage(promptText,  genBtn);
  });
  */

  // --- TEST button ---
  testBtn = addSimpleButton('testBtn', 'TEST Button', buttonContainer);
  testBtn.addEventListener('click', async () => {    
      console.log('TEST Button clicked',shot.name);
  });

  // --- Shot Status button ---
  changeShotStatusBtn = await createShotStatusButton(shot,buttonContainer);  

  // --- Send Image button (KIE.ai) ---  
  sendImageBtn = addSimpleButton('sendimage-btn', 'Send Image to KIE.ai', buttonContainer);
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

  // --- Create Resolve FCPXML button ---
  createResolveXMLButton = addSimpleButton('create-resolve-xml-btn', 'Generate Resolve FCPXML',buttonContainer);
  createResolveXMLButton.addEventListener('click', async () => {    
      const resultsFolder = await window.currentFolderHandle.getDirectoryHandle("results", { create: false });
      await generateFCPXMLFromFolder(resultsFolder);
  });


  return buttonContainer
}

// SHOT STATUS TOGGLE
async function createShotStatusButton(shot,parent = null)
{
  const shotToggleBtn = addSimpleButton('shot-toggle-btn', 'Finished',parent);

  function updateShotStatusButton(shotToggleBtn)  {
      shotToggleBtn.style.backgroundColor = shot.shotinfo.finished ? 'lightgreen' : 'lightgrey';
  }

  updateShotStatusButton(shotToggleBtn);
  shotToggleBtn.addEventListener('click', () => {
    updateShotStatus( shot, !shot.shotinfo.finished);
    updateShotStatusButton(shotToggleBtn);
  });
  return shotToggleBtn;
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

async function createPromptUI(handle, name = "prompt", parent = contentsPanel) { 
  // Create label
  const PromptLabel = document.createElement('label');
  PromptLabel.htmlFor = 'prompt-area';
  PromptLabel.textContent = name;
  PromptLabel.classList.add("prompt-label");

  // Create textarea
  const PromptTextArea = document.createElement('textarea');
  PromptTextArea.id = `prompt-area`;
  PromptTextArea.placeholder = 'Enter your prompt here...';
  PromptTextArea.rows = 3;

  // Load prompt.txt if exists
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
      console.log(`${name}.txt saved.`);
    }, 500);
  });

  // Create wrapper
  const wrapper = document.createElement('div');
  wrapper.classList.add('prompt-wrapper');
  wrapper.appendChild(PromptLabel);
  wrapper.appendChild(PromptTextArea);
  parent.appendChild(wrapper);

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

