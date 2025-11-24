
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

// Save folder handle and maintain latest 10 folders
async function savePickedFolder(handle) {
  const db = await getDB();
  const tx = db.transaction('folders', 'readwrite');
  const store = tx.objectStore('folders');

  // Save as lastFolder
  store.put(handle, 'lastFolder');

  // Get recentFolders array
  const recentReq = store.get('recentFolders');
  recentReq.onsuccess = (event) => {
    let recent = event.target.result || [];

    // Only add handle if it doesn't already exist (by reference)
    if (!recent.includes(handle)) {
      recent.unshift(handle);          // add to start
      if (recent.length > 10) recent = recent.slice(0, 10); // limit to 10
      store.put(recent, 'recentFolders');
    }
  };

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

// Load recent folders array
async function loadRecentFolders() {
  const db = await getDB();
  const tx = db.transaction('folders', 'readonly');
  const store = tx.objectStore('folders');
  return new Promise((resolve) => {
    const req = store.get('recentFolders');
    req.onsuccess = () => resolve(req.result || []);
    req.onerror = () => resolve([]);
  });
}
// USER FATA
async function loadUserData() {
  const db = await getDB();
  const tx = db.transaction('folders', 'readonly');
  const store = tx.objectStore('folders');

  const data = await new Promise(resolve => {
    const req = store.get('user_settings');
    req.onsuccess = () => resolve(req.result || {});
    req.onerror = () => resolve({});
  });

  // Add save method directly to the data object
  data.save = async function () {    
    const { save, ...dataToSave } = this;
    const tx = db.transaction('folders', 'readwrite');
    const store = tx.objectStore('folders');
    store.put(dataToSave, 'user_settings');
    
    // Wait for transaction to complete
    await new Promise((resolve, reject) => {
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
      tx.onabort = () => reject(tx.error);
    });
  };

  return data;
}


// CREATE Singleton
const db = {};
db.getDB = getDB;
db.savePickedFolder = savePickedFolder;
db.loadPickedFolder = loadPickedFolder;
db.loadRecentFolders = loadRecentFolders;
db.loadUserData = loadUserData;
window.db = db;



