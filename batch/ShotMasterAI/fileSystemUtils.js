
// BOUND JSON
async function loadBoundJson(handle,filename,defaultValue={}) {
    fileHandle = await handle.getFileHandle(filename, { create: true });
    file = await fileHandle.getFile();
    text = await file.text() || "{}";      
    data = JSON.parse(text);
    data = { ...defaultValue, ...data };
    data.____handle = fileHandle; // bind handle

    data.save = async function() {saveBoundJson(this);}
    return data;
}

async function saveBoundJson(data) {
    try {
        //console.log("DATA:",data)
        const text = JSON.stringify(data, null, 2); 
        const fileHandle = data.____handle; 
        const writable = await fileHandle.createWritable();
        await writable.write(text);
        await writable.close();
        console.log(`Saved bound json`);
    } catch (err) {
        console.error(`Failed to save`, err);
    }   
}

async function loadLocalTextFile(handle,filename) {
  try {
    fileHandle = await handle.getFileHandle(filename, { create: false });
    file = await fileHandle.getFile();
    text = await file.text();
    return text
  } catch {
    console.log(`Failed to load local text file: ${filename}`);
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
  sceneFolderHandle = await window.scenesDirHandle.getDirectoryHandle(scene_name, { create: true } );

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

// Splits Script into scenes and shots
async function importScenesFromScript() {
    function splitScenes(text) {
    return text
        .split(/(?=SC_\d{3})/)        // split at scene markers
        .filter(s => /^SC_\d{3}/.test(s.trim()))   // keep only real scenes
        .map(s => ({
        id: s.match(/^SC_\d{3}/)[0],
        content: s.replace(/^SC_\d{3}/, "").trim()
        }));
    }

    try {
        script_text = await loadLocalTextFile(rootDirHandle,'script.txt');
        scenes = splitScenes(text);

        for (scene in scenes) {
            scene_name = scenes[scene].id;
            scene_content = scenes[scene].content;
            sceneFolderHandle = await window.scenesDirHandle.getDirectoryHandle(scene_name, { create: true } );
            //saveLocalTextFile(sceneFolderHandle,'script.txt',scene_content);
            saveLocalJsonFile(sceneFolderHandle,"sceneinfo.json",{script:scene_content});
        }
    }
    catch (err) {
        console.error('Failed to read script.txt: ', err);
    }
}

async function getRelativePath(fileHandle, dirHandle, path = '') {
    for await (const [name, handle] of dirHandle.entries()) {
        if (handle === fileHandle) return path + name;
        if (handle.kind === 'directory') {
            const result = await getRelativePath(fileHandle, handle, path + name + '/');
            if (result) return result;
        }
    }
    return null;
}
