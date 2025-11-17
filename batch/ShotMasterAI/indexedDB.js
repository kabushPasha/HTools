
// Open IndexedDB and ensure object store exists
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

// Save folder handle
async function savePickedFolder(handle) {
  const db = await getDB();
  const tx = db.transaction('folders', 'readwrite');
  tx.objectStore('folders').put(handle, 'lastFolder');
  await tx.complete;
}

// Load last picked folder
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


// CREATE Singleton
const db = {};
db.getDB = getDB;
db.savePickedFolder = savePickedFolder;
db.loadPickedFolder = loadPickedFolder;
window.db = db;

