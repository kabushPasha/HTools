let rootDirHandle = null;
let selectedDirHandle = null;
const foldersEl = document.getElementById('folders');
const contentsPanel = document.getElementById('contents');
const statusBar = document.getElementById('status-bar');

// Add your KIE.ai API key here
window.KIE_API_KEY = '19d558c94447da4ea0f5bb14328fb9d4';

// -- BUTTON CALLBACKS ---
// --- Pick folder button ---
document.getElementById('pick').addEventListener('click', async () => {
  try {
    rootDirHandle = await window.showDirectoryPicker({ mode: 'readwrite' });
    await window.db.savePickedFolder(rootDirHandle);
    await listFolders();
    contentsPanel.innerHTML = '';
  } catch (err) {
    console.error('Folder pick canceled or failed', err);
  }
});

// --- Import From Scenes from Clipboard ---
document.getElementById('import_shots_from_clipboard_btn').addEventListener('click', async () => {
    await importShotsFromClipboard();  
});

// --- Import From Scenes from Clipboard ---
document.getElementById('import_scenes_from_script_btn').addEventListener('click', async () => {
    await importScenesFromScript();  
});


// --- Load last picked folder on page load ---
window.addEventListener('DOMContentLoaded', async () => {
  const handle = await window.db.loadPickedFolder();
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


const recentMenu = document.getElementById('recent-folders-menu');
// Load recent folders from IndexedDB and populate submenu
async function populateRecentFolders() {
  const recent = await window.db.loadRecentFolders();
  recentMenu.innerHTML = ''; 
  
  recent.forEach((handle, index) => {
    const li = document.createElement('li');
    li.textContent = handle.name;
    li.addEventListener('click', async () => {
      // Request permission and open folder
      let permission = await handle.queryPermission({ mode: 'readwrite' });
      if (permission !== 'granted') {
        permission = await handle.requestPermission({ mode: 'readwrite' });
      }
      if (permission === 'granted') {
        rootDirHandle = handle;
        await listFolders();
        contentsPanel.innerHTML = '';
      }
    });
    recentMenu.appendChild(li);
  });
}
// Populate on hover
document.getElementById('open-recent').addEventListener('mouseenter', populateRecentFolders);
