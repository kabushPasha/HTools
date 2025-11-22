





// KIE Post Task
async function postKieTask(url,payload){
  console.log("postKieTask",url,payload);
  const options = {
    method: 'POST',
    headers: {Authorization: `Bearer ${window.KIE_API_KEY}`, 'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  };

  try {
    const response = await fetch(url, options);

    return response;
  } catch (error) {
    console.error(error);
    return null;
  } 
}

// KIE_txt2Img
async function kieGenerate_txt2img(prompt){
  console.log("kieGenerate_txt2img",prompt)
  const url = 'https://api.kie.ai/api/v1/gpt4o-image/generate';
  const payload = {
    prompt,
    size: '1:1',
    nVariants: 1,
    isEnhance: false,
    uploadCn: false,
    enableFallback: false,
    fallbackModel: 'FLUX_MAX'
  };

  response = await postKieTask(url,payload);
  return response;
}

// KIE Runway Img2Vide - REWRITE to use Post task?
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

// Upload File - REWRITE to use Post task?
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

// CHECK RESULTS
async function checkTaskResults(task) {
  const KIE_API_KEY = window.KIE_API_KEY || '';  

  // EACH API HAS DIFFERENT ENDPOINT FOR THIS, 
  const url = `https://api.kie.ai/api/v1/gpt4o-image/record-info?taskId=${task.taskId}`;
  //const url = `https://api.kie.ai/api/v1/runway/record-detail?taskId=${taskId}`;

  const options = { 
    method: 'GET', 
    headers: { Authorization: `Bearer ${KIE_API_KEY}` }
  };

  try {
    //console.log('Checking task results with options:', options);
    const response = await fetch(url, options);
    //console.log('checkTaskResults RESPONSE :', response);
    
    if (!response.ok) {
      const txt = await response.text();
      throw new Error(`Record-info error ${response.status}: ${txt}`);
    }

    const data = await response.json();
    console.log('record-info  DATA:', data);
    if (data?.msg === 'success')
    {
      const resultUrls = data?.data?.response?.resultUrls || [data?.data?.videoInfo?.videoUrl] || [];       
      task.resultUrls = resultUrls;
    }
  } catch (error) {
    console.error('checkTaskResults failed', error);    
  }
}

// File2Base64
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



