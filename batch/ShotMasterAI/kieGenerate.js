// Main function: validate prompt, generate image, save to folder, update UI
async function generateAndSaveImage(promptText,genBtn) {
  // fall back to globals
  dirHandle = window.dirHandle;
  statusEl = window.statusEl;

  // Validate inputs
  if (!validatePrompt(promptText, statusEl)) return;
  if (!validateApiKey(statusEl)) return;

  genBtn.disabled = true;
  statusEl.textContent = 'Generating...';
  statusEl.style.opacity = 1;

  try {
    // Generate image and get URLs
    await kieGenerate(promptText);
  } catch (err) {
    console.error('Generate failed', err);
    statusEl.textContent = 'Generate failed';
    statusEl.style.opacity = 1;
    setTimeout(() => statusEl.style.opacity = 0, 2000);
  } finally {
    genBtn.disabled = false;
    setTimeout(() => statusEl.style.opacity = 0, 1000);
  }
}

// Validate prompt text
function validatePrompt(promptText, statusEl) {
  if (!promptText) {
    statusEl.textContent = 'Enter a prompt first';
    statusEl.style.opacity = 1;
    setTimeout(() => statusEl.style.opacity = 0, 1500);
    return false;
  }
  return true;
}

// Validate API key
function validateApiKey(statusEl) {
  const KIE_API_KEY = window.KIE_API_KEY;
  if (!KIE_API_KEY) {
    statusEl.textContent = 'Set KIE_API_KEY in ShotasterAI.js';
    statusEl.style.opacity = 1;
    return false;
  }
  return true;
}

// KIE generation + polling moved here. Reads API key from window.KIE_API_KEY at call time.
async function kieGenerate(prompt) {
  const generateUrl = 'https://api.kie.ai/api/v1/gpt4o-image/generate';
  const payload = {
    prompt,
    size: '1:1',
    nVariants: 1,
    isEnhance: false,
    uploadCn: false,
    enableFallback: false,
    fallbackModel: 'FLUX_MAX'
  };
  
  console.log('KIE generate payload:', payload);  

  const postRes = await fetch(generateUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${window.KIE_API_KEY}`
    },
    body: JSON.stringify(payload)
  });

  const postText = await postRes.text();
  let postJson;
  try { postJson = JSON.parse(postText); } catch { postJson = postText; }
  console.debug('KIE generate response:', postJson);

  if (!postRes.ok) {
    throw new Error(`KIE generate error ${postRes.status}: ${postText}`);
  }

  taskId = postJson.data.taskId;  
  try { window.addKieTask(taskId, prompt); } catch (e) { console.warn('addKieTask failed', e); }
}


// Generate Video - split into post and recieve task ID
async function kieGenerate_RunwayImg2Video(prompt, initImageUrl){
  const url = 'https://api.kie.ai/api/v1/runway/generate';
  
  const payload = {
    prompt : prompt,
    duration : "5",
    quality : "720p",
    imageUrl: initImageUrl,
    aspectRation: "9:16", 
    model: "runway-duration-5-generate",
    waterMark: "",
  };

  const options = {
    method: 'POST',
    headers: {Authorization: `Bearer ${window.KIE_API_KEY}`, 'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  };

  console.log('KIE Runway Img2Video options:', options);

  try {
    const response = await fetch(url, options);
    const data = await response.json();
    console.log(data);
    
    taskId = data.data.taskId;  
    try { window.addKieTask(taskId, prompt); } catch (e) { console.warn('addKieTask failed', e); }

  } catch (error) {
    console.error(error);
  } 
}

async function kieUploadFile(img_fileHandle) {
  img_data = await fileToBase64(img_fileHandle);
  console.log('Uploading image to KIE.ai:', img_data);

  const url = 'https://kieai.redpandaai.co/api/file-base64-upload';
  const options = {
    method: 'POST',
    headers: {Authorization: `Bearer ${window.KIE_API_KEY}`,
             'Content-Type': 'application/json'},
    body: `{"base64Data":"${img_data.rawBase64}",
           "fileName":"${img_fileHandle.name}",
           "uploadPath":"images/test"}`
  };

  console.log('KIE upload options:', options);

  try {
    const response = await fetch(url, options);
    const data = await response.json();    
    console.log('Image uploaded to KIE.ai with fileId:', data);
    return data.data;
  } catch (error) {
    console.error('kieUploadFile failed', error);
  }
}

// New: check task results (separate function)
async function checkTaskResults(taskId) {
  const KIE_API_KEY = window.KIE_API_KEY || '';
  if (!taskId) throw new Error('No taskId provided');

  // EACH API HAS DIFFERENT ENDPOINT FOR THIS, 
  //const url = `https://api.kie.ai/api/v1/gpt4o-image/record-info?taskId=${taskId}`;
  const url = `https://api.kie.ai/api/v1/runway/record-detail?taskId=${taskId}`;

  const options = { 
    method: 'GET', 
    headers: { Authorization: `Bearer ${KIE_API_KEY}` }
  };

  try {
    console.log('Checking task results with options:', options);
    const response = await fetch(url, options);
    console.log('checkTaskResults RESPONSE :', response);
    if (!response.ok) {
      const txt = await response.text();
      throw new Error(`Record-info error ${response.status}: ${txt}`);
    }
    const data = await response.json();
    console.log('record-info  DATA:', data);
    const ok = data?.msg === 'success';

    console.log('Saving results for task:', taskId);

    // Save Result Images
    const resultUrls = ok ? (data?.data?.response?.resultUrls || [data?.data?.videoInfo?.videoUrl] || []) : [];   
    if (ok && resultUrls.length > 0) {      
      await saveResults(resultUrls);
    }

    return { ok, resultUrls, raw: data };
  } catch (error) {
    console.error('checkTaskResults failed', error);
    return { ok: false, error };
  }
}


// Save result images to results folder (accept optional args)
async function saveResults(resultUrls) {
  console.log('Saving result images:', resultUrls);
  dirHandle = window.currentFolderHandle; 

  if (!resultUrls || resultUrls.length === 0) return;

  if (!dirHandle) throw new Error('No directory handle available to save results');

  const resultsHandle = await dirHandle.getDirectoryHandle('results', { create: true });
  
  for (let i = 0; i < resultUrls.length; i++) {
    const imageUrl = resultUrls[i];
    
    try {
      // Extract filename from URL or generate one
      let fileName = `image_${Date.now()}_${i}.png`;
      try {
        const urlObj = new URL(imageUrl);
        const urlPath = urlObj.pathname;
        const urlFileName = urlPath.split('/').pop();
        if (urlFileName && urlFileName.length > 0) {
          fileName = urlFileName;
        }
      } catch (e) {
        console.warn('Could not extract filename from URL, using default', e);
      }

      // Check if file already exists
      let fileExists = false;
      try {
        await resultsHandle.getFileHandle(fileName);
        fileExists = true;
      } catch (e) {
        // File does not exist, which is expected
      }

      if (fileExists) {
        console.log(`File already exists, skipping: ${fileName}`);
        continue;
      }

      // File doesn't exist, download and save it
      const response = await fetch(imageUrl);
      const blob = await response.blob();

      const fileHandle = await resultsHandle.getFileHandle(fileName, { create: true });
      const writable = await fileHandle.createWritable();
      await writable.write(blob);
      await writable.close();

    } catch (imgErr) {
      console.error(`Failed to save image ${i}`, imgErr);
    }
  }  
}



async function fileToBase64(fileHandle) {
  const file = await fileHandle.getFile();
  const arrayBuffer = await file.arrayBuffer();

  // Convert bytes → Base64
  let binary = "";
  const bytes = new Uint8Array(arrayBuffer);
  const len = bytes.byteLength;

  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }

  const base64 = btoa(binary);
  return {
    dataUrl: `data:${file.type};base64,${base64}`,
    rawBase64: base64
  };
}


// Attach to global
window.generateAndSaveImage = generateAndSaveImage;
window.kieGenerate = kieGenerate;
window.saveResults = saveResults;
window.checkTaskResults = checkTaskResults;
window.kieUploadFile = kieUploadFile;
window.kieGenerate_RunwayImg2Video = kieGenerate_RunwayImg2Video

