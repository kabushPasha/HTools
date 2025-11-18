let rootDirHandle = null;
let selectedDirHandle = null;
const foldersEl = document.getElementById('folders');
const contentsPanel = document.getElementById('contents');
const statusBar = document.getElementById('status-bar');

// Add your KIE.ai API key here
window.KIE_API_KEY = '19d558c94447da4ea0f5bb14328fb9d4';

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


// List the loaded folders and subfolders
async function listFolders() {
  foldersEl.innerHTML = ''; // Clear existing UI

  for await (const [sceneName, sceneHandle] of rootDirHandle.entries()) {
    if (sceneHandle.kind === 'directory') {
      const sceneLi = document.createElement('li');
      sceneLi.textContent = sceneName;
      sceneLi.style.cursor = 'pointer';

      // Subfolders container
      const subfolderUl = document.createElement('ul');
      subfolderUl.style.display = 'none'; // Initially collapsed

      // Populate shot subfolders
      for await (const [shotName, shotHandle] of sceneHandle.entries()) {
        if (shotHandle.kind === 'directory') {
          const shotLi = document.createElement('li');
          shotLi.textContent = shotName;
          shotLi.style.cursor = 'pointer';

          shotLi.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent triggering scene click
            selectFolder(shotHandle, shotLi);
          });

          subfolderUl.appendChild(shotLi);
        }
      }

      // Toggle show/hide on scene click + call selection
      sceneLi.addEventListener('click', () => {
        selectSceneFolder(sceneHandle, sceneLi);
        const isCollapsed = subfolderUl.style.display === 'none';
        subfolderUl.style.display = isCollapsed ? 'block' : 'none';
      });

      // Append UI
      sceneLi.appendChild(subfolderUl);
      foldersEl.appendChild(sceneLi);
    }
  }
}

// Status bar helper
function updateStatus(message) {
  if (statusBar) {
    statusBar.textContent = message;
  }
  console.log(message);
}
window.updateStatus = updateStatus;
