function createTabContainer(parent = null) {
    const container = document.createElement('div');
    container.classList.add('tab-container');

    const buttonsContainer = document.createElement('div');
    buttonsContainer.classList.add('tab-buttons');

    const contentContainer = document.createElement('div');
    contentContainer.classList.add('tab-contents');

    container.appendChild(buttonsContainer);
    container.appendChild(contentContainer);

    const tabs = [];

    function showTab(id) {
        tabs.forEach(tab => {
            tab.button.classList.toggle('active', tab.id === id);
            tab.content.style.display = tab.id === id ? 'block' : 'none';
        });
    }

    function addTab({ title, content }) {
        const id = 'tab-' + (tabs.length + 1);

        const button = document.createElement('button');
        button.classList.add('tab-button');
        button.textContent = title;
        button.addEventListener('click', () => showTab(id));

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('tab-content');

        if (typeof content === 'string') {
            contentDiv.innerHTML = content;
        } else if (content instanceof HTMLElement) {
            contentDiv.appendChild(content);
        }

        buttonsContainer.appendChild(button);
        contentContainer.appendChild(contentDiv);

        tabs.push({ id, button, content: contentDiv });

        if (tabs.length === 1) showTab(id);
    }

    if (parent) parent.appendChild(container);
    return { addTab, container };
}

function createResizableContainer(parent = null) {
  const container = document.createElement('div');
  container.id = "ShotPreviewsContainer";

  // --- Horizontal scroll wrapper ---
  const contentsWrapper = document.createElement('div');
  contentsWrapper.classList.add('contents-wrapper');
  container.appendChild(contentsWrapper);

  // --- Add resizer handle ---
  const resizer = document.createElement('div');
  resizer.classList.add('resizer');
  container.appendChild(resizer);

  let isResizing = false;

  resizer.addEventListener('mousedown', () => {
    isResizing = true;
    document.body.style.userSelect = 'none';
  });

  document.addEventListener('mousemove', (e) => {
    if (!isResizing) return;
    const newHeight = e.clientY - container.getBoundingClientRect().top;
    if (newHeight > 50) container.style.height = newHeight + 'px';
  });

  document.addEventListener('mouseup', () => {
    isResizing = false;
    document.body.style.userSelect = 'auto';
  });

  // Function to add a child to contents
  function appendChild(child) { contentsWrapper.appendChild(child); }
  if (parent) parent.appendChild(container);
  return { appendChild, container };
}

function createHorizontalContainer(parent = null) {
  const scrollWrapper = document.createElement('div');
  scrollWrapper.classList.add('horizontal-container');  // add CSS class
  if (parent) parent.appendChild(scrollWrapper);
  return scrollWrapper;
}



