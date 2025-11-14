let rootDirHandle = null;
let selectedDirHandle = null;
const foldersEl = document.getElementById('folders');
const contentsEl = document.getElementById('contents');

// Add your KIE.ai API key here
window.KIE_API_KEY = '19d558c94447da4ea0f5bb14328fb9d4';

// --- IndexedDB helper functions ---
function getDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('folderDB', 1);
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains('folders')) {
        db.createObjectStore('folders');
      }
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

async function savePickedFolder(handle) {
  const db = await getDB();
  const tx = db.transaction('folders', 'readwrite');
  tx.objectStore('folders').put(handle, 'lastFolder');
  await tx.complete;
}

async function loadPickedFolder() {
  const db = await getDB();
  const tx = db.transaction('folders', 'readonly');
  const store = tx.objectStore('folders');
  return new Promise((resolve) => {
    const req = store.get('lastFolder');
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => resolve(null);
  });
}

// --- Pick folder button ---
document.getElementById('pick').addEventListener('click', async () => {
  try {
    rootDirHandle = await window.showDirectoryPicker({ mode: 'readwrite' });
    await savePickedFolder(rootDirHandle);
    await listFolders();
    contentsEl.innerHTML = '';
  } catch (err) {
    console.error('Folder pick canceled or failed', err);
  }
});

// --- Load last picked folder on page load ---
window.addEventListener('DOMContentLoaded', async () => {
  const handle = await loadPickedFolder();;
  if (handle) {
    let permission = await handle.queryPermission({ mode: 'readwrite' });
    if (permission !== 'granted') {
      permission = await handle.requestPermission({ mode: 'readwrite' });
    }
    if (permission === 'granted') {
      rootDirHandle = handle;
      await listFolders();
    }
  }
});

// --- List immediate subfolders ---
async function listFolders() {
  foldersEl.innerHTML = '';
  for await (const [name, handle] of rootDirHandle.entries()) {
    if (handle.kind === 'directory') {
      const li = document.createElement('li');
      li.textContent = name;
      li.addEventListener('click', () => selectFolder(handle, li));
      foldersEl.appendChild(li);
    }
  }
}

