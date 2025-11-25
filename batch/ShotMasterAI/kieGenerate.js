





// KIE Post Task
async function postKieTask(url,payload){
  console.log("postKieTask",url,payload);
  const options = {
    method: 'POST',
    headers: {Authorization: `Bearer ${window.userdata.KIE_API_KEY}`, 'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  };

  try {
    const response = await fetch(url, options);
    console.log("response",response);
    const data = await response.json(); 
    console.log("data",data);
    const taskId = data.data.taskId;  
    return taskId;
  } catch (error) {
    console.error(error);
    return null;
  } 
}

// KIE_txt2Img
async function kieGenerate_txt2img(prompt){
  console.log("kieGenerate_txt2img",prompt)
  const apiUrl = 'https://api.kie.ai/api/v1/gpt4o-image'
  const url = apiUrl + '/generate';
  const payload = {
    prompt,
    size: '1:1',
    nVariants: 1,
    isEnhance: false,
    uploadCn: false,
    enableFallback: false,
    fallbackModel: 'FLUX_MAX',
  };

  const taskId = await postKieTask(url,payload);

  const task = {
    createdAt: new Date().toISOString().slice(0, 19).replace("T", " "),
    prompt: prompt,
    taskId: taskId,
    status: "pending",
    outputFolder: "results",
    apiUrl : apiUrl,    
    resultsUrl : `${apiUrl}/record-info?taskId=${taskId}`, 
  };   

  return task;
}

// KIE Runway Img2Vide - REWRITE to use Post task?
async function kieGenerate_RunwayImg2Video(prompt, initImageUrl){
  const apiUrl = 'https://api.kie.ai/api/v1/runway';  
  const url = apiUrl + '/generate';
  const payload = {
    prompt : prompt,
    duration : "5",
    quality : "720p",
    imageUrl: initImageUrl,
    aspectRation: "9:16", 
    model: "runway-duration-5-generate",
    waterMark: "",
    type : "txt2img",
  };

  const taskId = await postKieTask(url,payload);

  const task = {
    createdAt: new Date().toISOString().slice(0, 19).replace("T", " "),
    prompt: prompt,
    taskId: taskId,
    status: "pending",
    outputFolder: "resultVods",
    apiUrl : apiUrl,
    type: "img2vid",
    resultsUrl : `${apiUrl}/record-detail?taskId=${taskId}`, 
  };  
  return task;
}

// Upload File - REWRITE to use Post task?
async function kieUploadFile(img_fileHandle) {
  img_data = await fileToBase64(img_fileHandle);
  console.log('Uploading image to KIE.ai:', img_data);

  const url = 'https://kieai.redpandaai.co/api/file-base64-upload';
  const options = {
    method: 'POST',
    headers: {Authorization: `Bearer ${window.userdata.KIE_API_KEY}`,
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

// CHECK RESULTS
async function checkTaskResults(task) {
  const url = task.resultsUrl;

  const options = { 
    method: 'GET', 
    headers: { Authorization: `Bearer ${ window.userdata.KIE_API_KEY}` }
  };

  try {
    console.log("GET RESULTS",url,options);
    const response = await fetch(url, options);

    if (!response.ok) {
      const txt = await response.text();
      throw new Error(`Record-info error ${response.status}: ${txt}`);
    }

    const data = await response.json();
    console.log('record-info  DATA:', data);
    if (data?.msg === 'success' && (data?.data?.status === "SUCCESS" || data?.data?.state === "success"))
    {
      console.log("images",data?.data?.response?.resultUrls)
      console.log("videos",data?.data?.videoInfo?.videoUrl )
      task.resultUrls = data?.data?.response?.resultUrls 
        ?? (data?.data?.videoInfo?.videoUrl ? [data.data.videoInfo.videoUrl] : []) 
        ?? [];
    }
  } catch (error) {
    console.error('checkTaskResults failed', error);    
  }
}


