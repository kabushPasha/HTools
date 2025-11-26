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
            if (tab.id === id)  tab.onShown();
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
        
        tabs.push({ id, button, content: contentDiv ,
          onShown : async function(){
            
            const walkChildren = (element) => {
                for (const child of element.children) {
                    // If the child has an onShown function, call it
                    if (typeof child.onShown === 'function') {
                        child.onShown();
                    }
                    // Recursively check its children
                    walkChildren(child);
                }
            };

            walkChildren(contentDiv);
          }
        });

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

function createCollapsibleContainer(name, parent = null) {
    // Create main container
    //console.log("collapsible container:",parent);
    const container = document.createElement('div');
    container.classList.add('collapsible-container');

    // Create header (label + button)
    const header = document.createElement('div');
    header.classList.add('collapsible-header');

    const label = document.createElement('span');
    label.textContent = name;
    label.classList.add('collapsible-label');

    const button = document.createElement('button');
    button.textContent = 'Collapse';
    button.classList.add('collapsible-button');

    header.appendChild(label);
    header.appendChild(button);

    // Create inner content container
    const contentContainer = document.createElement('div');
    contentContainer.classList.add('collapsible-content');
    contentContainer.style.marginTop = '10px';

    // Toggle functionality
    let isCollapsed = false;
    button.addEventListener('click', () => {
        isCollapsed = !isCollapsed;
        contentContainer.style.display = isCollapsed ? 'none' : 'block';
        button.textContent = isCollapsed ? 'Expand' : 'Collapse';
    });

    // Assemble container
    container.appendChild(header);
    container.appendChild(contentContainer);

    container.appendChild = function(el) {
        contentContainer.appendChild(el);
    }

    if (parent) parent.appendChild(container);
    return container;
}

function CreateButtonsContainer(parent = null) {
  const container = document.createElement('div');
  container.classList.add('buttons-container'); // CSS handles all styling
  if (parent) parent.appendChild(container);
  return container;
}