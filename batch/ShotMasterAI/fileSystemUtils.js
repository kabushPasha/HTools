
async function loadLocalTextFile(handle,filename) {
  try {
    fileHandle = await handle.getFileHandle(filename, { create: false });
    file = await fileHandle.getFile();
    text = await file.text();
    return text
  } catch {
    return ""
  }
}

async function saveLocalTextFile(handle,filename,text) {
    try {
        const fileHandle = await handle.getFileHandle(filename, { create: true });
        const writable = await fileHandle.createWritable();
        await writable.write(text);
        await writable.close();
    } catch (err) {
        console.error('Failed to save prompt.txt', err);
    }
}

async function loadLocalJsonFile(handle,filename) {
    try {  
        text = await loadLocalTextFile(handle,filename);
        return  JSON.parse(text);
    } catch {
        return null;
    }
}

async function saveLocalJsonFile(handle,filename,json) {
    try {
        const text = JSON.stringify(json, null, 2); 
        await saveLocalTextFile(handle,filename,text);
    } catch (err) {
        console.error('Failed to save json file', err);
    }       
}

async function clipboardToJson() {
  try {
        window.updateStatus('Importing json from clipboard...');
        const text = await navigator.clipboard.readText();    
        json = JSON.parse(text);
        return json;
    }
    catch (err) {
      console.error('Failed to read clipboard contents: ', err);
    }
    return null;
}

async function importShotsFromClipboard() {
    try {
        shot_dict = await clipboardToJson();
        for (const key in shot_dict) {
        if (shot_dict.hasOwnProperty(key)) {
            importSceneDict(key, shot_dict[key]);
            }
        }
    }
    catch (err) {
        console.error('Failed to read clipboard contents: ', err);
    }
}

async function importSceneDict(scene_name, scene_dict){
  window.updateStatus(`Importing scene: ${scene_name}`);
  sceneFolderHandle = await rootDirHandle.getDirectoryHandle(scene_name, { create: true } );

  for (const key in scene_dict) {
    if (scene_dict.hasOwnProperty(key)) {          
        importShotDict(key, scene_dict[key],sceneFolderHandle);
      }
  }
}

async function importShotDict(shot_name,shot_dict,sceneFolderHandle) {
  window.updateStatus(`Importing shot: ${shot_name} `);    
  //console.log('Importing shot:', shot_dict);
  shotFolderHandle = await sceneFolderHandle.getDirectoryHandle(shot_name, { create: true } );

    try {
        const fileHandle = await shotFolderHandle.getFileHandle('prompt.txt', { create: true });
        const writable = await fileHandle.createWritable();
        await writable.write(shot_dict.prompt);
        await writable.close();
    } catch (err) {
    console.error('Failed to save prompt.txt', err);
    }
}



