
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
  //const PromptTextArea = await createPromptUI(handle);
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

  //await createPromptUI(scene.handle, "script",parent = sceneSettingsContainer);
  await editableJsonField(scene.sceneinfo, "script", sceneSettingsContainer);

  buttonContainer = CreateButtonsContainer(parent = sceneSettingsContainer);
  SplitIntoShotsBtn = addSimpleButton('split-into-shots-btn', 'Split Into Shots',buttonContainer);

  // Currently not used button
  //ImportShotsBtn = addSimpleButton(buttonContainer, 'import-shots-btn', 'Import Shots Clipboard');
  //ImportShotsBtn.addEventListener('click', async () => { await importShotsFromClipboard(); });

  generateSplitIntoShotsPromptBtn = addSimpleButton('generate-split-into-shots-prompt-btn', 'Generate Split Prompt',buttonContainer);
  generateSplitIntoShotsPromptBtn.addEventListener('click', async () => { 
      base_text = `разбей эту сцену из моего сценария на шоты, сгенерируй промпты для нейросети для генерации видео и предоставь в виде json, в ответе предоставь толкьо json в следующем формате:
      {"SHOT_010" : 
        {"prompt" : "подробный промпт для нейросети генератора видео", 
        "camera" : "focal length, shot type", 
        "action_description" : "описания действия которое происходит для аниматора", } 
        } 
      }

      ${scene.sceneinfo.script}
      `;
      navigator.clipboard.writeText(base_text)
    });

  generateShotsFromJsonBtn = addSimpleButton('generate-shots-from-json-btn', 'Generate Shots from JSON',buttonContainer);
  generateShotsFromJsonBtn.addEventListener('click', async () => {    
    shotdict = JSON.parse(scene.sceneinfo.shotsjson);
    for (const key in shotdict) {
      console.log('Generating shot:', key);
      console.log('Shot data:', shotdict[key]);

      shothandle = await scene.handle.getDirectoryHandle(key, { create: true } );
      shotinfohandle = await shothandle.getFileHandle('shotinfo.json', { create: true } );
      shotinfo = { ...default_shotinfo, ...shotdict[key] ,...{____handle: shotinfohandle} };

      scene.shots.push( {
        name: key,
        handle: shothandle,
        shotinfo: shotinfo
      });

      await saveBoundJson(shotinfo);
    }
  });  

  await editableJsonField(scene.sceneinfo, "shotsjson", sceneSettingsContainer);

  shotPreviewStrip = await createShotPreviewStrip(scene);

  const tabs1 = createTabContainer(contentsPanel);
  tabs1.addTab({ title: 'Scene', content: sceneSettingsContainer });
  tabs1.addTab({ title: 'Shots', content: shotPreviewStrip }); 
}

// Shot INFO CARD 
async function CreateShotInfoCard(shot,parent = null) {
  const container = document.createElement('div');
  container.classList.add('shot-info'); 

  // --- Shot name ---
  const title = document.createElement('div');
  title.textContent = shot.name;
  title.classList.add('shot-info-title');  // optional CSS class
  container.appendChild(title);

  // --- Prompt TextArea ---
  //PromptTextArea = await createPromptUI(shot.handle, "prompt", container);
  await editableJsonField(shot.shotinfo, "prompt", container);
  await editableJsonField(shot.shotinfo, "camera", container);
  await editableJsonField(shot.shotinfo, "action_description", container);
  
  CreateShotInfoCardButtons(shot,container); 

  container.taskContainer = await createTaskContainer(shot,container);

  // Create Images Preview Folder
  await createMediaFolderPreview(shot,"results",container)
  await createMediaFolderPreview(shot,"resultVods",container)

  // Append to parent
  if (parent) parent.appendChild(container);
  return container;
}
// Shot Preview Strip
async function createShotPreviewStrip(scene) {
  const container = document.createElement('div');

  resizableArea = createResizableContainer(parent = container);
  shotsStrip = createHorizontalContainer(resizableArea)

  // --- Create and append each shot preview ---
  for (const shot of scene.shots) {
    const shotElement = await CreateShotPreview(shot);
    shotsStrip.appendChild(shotElement);
    const shot_info = await CreateShotInfoCard(shot, parent = container);
    shot_info.style.display = 'none';

    // --- Add click event to show corresponding info ---
    shotElement.addEventListener('click', () => {
      document.querySelectorAll('.shot-info').forEach(el => el.style.display = 'none');
      shot_info.style.display = 'block';
    });
  }
  return container;
}
// Shot Preview Icon
async function CreateShotPreview(shot) {
  // Container for the shot
  const container = document.createElement("div");
  container.classList.add("shot-preview");

  // Image element
  const img = document.createElement("img");
  img.src = "https://picsum.photos/id/237/200/300";

  if (shot.shotinfo.srcImage){
    const resultsDir = await shot.handle.getDirectoryHandle("results", { create: false });
    const fileHandle = await resultsDir.getFileHandle(shot.shotinfo.srcImage, { create: false });

    const file = await fileHandle.getFile();
    const url = URL.createObjectURL(file);
    img.src = url;
  }

  container.appendChild(img);

  // Label
  const label = document.createElement("div");
  label.textContent = shot.name;
  label.classList.add("shot-preview-label");
  container.appendChild(label);

  return container;
}
// Simple Button
function addSimpleButton(btn, text, parent = null)
{
  simpleBtn = document.createElement('button');
  simpleBtn.id = btn;
  simpleBtn.textContent = text;
  if (parent) {parent.appendChild(simpleBtn);}
  return simpleBtn;
}
// Shot Info Card Buttons
async function CreateShotInfoCardButtons(shot,parent = null)
{
  buttonContainer = CreateButtonsContainer(parent);
  
  // --- TEST button ---
  testBtn = addSimpleButton('testBtn', 'Log shot', buttonContainer);
  testBtn.addEventListener('click', async () => { console.log(shot); });

  // --- Shot Status button ---
  changeShotStatusBtn = await createShotStatusButton(shot,buttonContainer);  

  // --- Send Image button (KIE.ai) ---  
  /*
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
  */

  // --- Create Resolve FCPXML button ---
  createResolveXMLButton = addSimpleButton('create-resolve-xml-btn', 'Generate Resolve FCPXML',buttonContainer);
  createResolveXMLButton.addEventListener('click', async () => {    
      const resultsFolder = await window.currentFolderHandle.getDirectoryHandle("results", { create: false });
      await generateFCPXMLFromFolder(resultsFolder);
  });


  txt2ImageBtn = addSimpleButton('txt2imgBtn',"txt2img", buttonContainer);
  txt2ImageBtn.addEventListener('click', async () => {   
    console.log("Clicked txt2img:",shot); 
    try {
        const _task = await kieGenerate_txt2img(shot.shotinfo.prompt);
        const task = await shot.addKieTask(_task);  
        parent?.taskContainer?.addTask(task);

    } catch (error) {
      console.error(error);
    }
  });

  img2videoBtn = addSimpleButton('img2videoBtn',"img2video", buttonContainer);
  img2videoBtn.addEventListener('click', async () => {   
    console.log("Clicked img2video:",shot); 
    try {
      const srcImageHandle = await shot.getSrcImageHandle();
      console.log("SRC_IMAGE",srcImageHandle)

      if (srcImageHandle) {
        img_upload_data = await kieUploadFile(srcImageHandle);
        console.log('Image upload data:', img_upload_data.downloadUrl);
        if (img_upload_data && img_upload_data.success)
        {
          const _task = await kieGenerate_RunwayImg2Video(shot.shotinfo.prompt, img_upload_data.downloadUrl);      
          const task = await shot.addKieTask(_task);  
          parent?.taskContainer?.addTask(task);
        }
      }
    } catch (error) {
      console.error(error);
    }
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

// Load Media Folder -- rewrite
async function createMediaFolderPreview(shot, folderName, parent = null) {
  try {
    container = await createCollapsibleContainer(folderName,parent);
    const srcImagesHandle = await shot.handle.getDirectoryHandle(folderName, { create: false });

    const imagesContainer = document.createElement('div');
    imagesContainer.className = "media-container";

  for await (const [name, fileHandle] of srcImagesHandle.entries()) {
    if (fileHandle.kind === 'file') {
      const file = await fileHandle.getFile();
      const url = URL.createObjectURL(file);      

      if (/\.(png|jpe?g|gif|webp)$/i.test(name)) {
        const wrapper = document.createElement('div');
        wrapper.className = 'img-wrapper';
   
        if (name === shot.shotinfo.srcImage) wrapper.classList.add('highlighted'); 

        const img = document.createElement('img');
        img.src = url;
        img.className = 'media-img';
        img.title = name;

        const btn = document.createElement('button');
        btn.className = 'media-hover-btn';
        btn.textContent = 'Pick';

        // SET SRC IMAGE ON CLICK
        btn.addEventListener('click', (event) => {
          event.stopPropagation();
          console.log(url);
          shot.shotinfo.srcImage = name;          
          shot.saveShotInfo();

          imagesContainer.querySelectorAll('.img-wrapper.highlighted').forEach(el => el.classList.remove('highlighted'));
          wrapper.classList.add('highlighted');
        });

        wrapper.append(img, btn);
        imagesContainer.appendChild(wrapper);
      }

      if (/\.(mp4|webm|ogg|mov|mkv)$/i.test(name)) {
        const video = document.createElement('video');
        video.src = url;
        video.style.width = 'auto';          // Ensures visibility
        video.style.maxHeight = '300px';
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
    container.appendChild(imagesContainer);
    return container
  } catch {
    // no SrcImages folder
  }
}
