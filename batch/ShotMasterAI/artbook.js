


async function readArtbookData(){
    window.artbook = [];
    window.artbookDirHandle = await rootDirHandle.getDirectoryHandle("REFS", { create: true } );

    for await (const [artTypeName, artTypeHandle] of window.artbookDirHandle.entries()) {
        if (artTypeHandle.kind === 'directory') {
            artTypeData = await LoadArtTypeFolder(artTypeName, artTypeHandle);
        window.artbook.push( artTypeData );
        }
    }
}

async function LoadArtTypeFolder(artTypeName, artTypeHandle){
  const artTypeData = {
    name: artTypeName ,
    handle: artTypeHandle, 
    items: [],
    path: artTypeName,
    async loadItems() {
        this.items = []
        for await (const [itemName, itemHandle] of this.handle.entries()) {
            if (itemHandle.kind === 'directory') {
                this.items.push(await LoadArtItem(itemName,itemHandle,this));
            }
        }
    },
    }

  await artTypeData.loadItems()
  return artTypeData
}

async function LoadArtItem(itemName, itemHandle,itemType){
  const artItem = { 
        name: itemName,
        handle: itemHandle, 
        images: [],
        path: itemType.path + "/" + itemName,
        async loadImages() {
            for await (const [name, fileHandle] of this.handle.entries()) {
                    if (fileHandle.kind !== "file") continue;
                    this.images.push( {
                        name:name,
                        handle:fileHandle,
                        path: this.path + "/" + name,
                        async createTagItem(parent = null,callback = null) {
                            const tagDiv = document.createElement("div");
                            tagDiv.className = "tag-item";
                            tagDiv.style.display = "flex";
                            tagDiv.style.alignItems = "center";
                            tagDiv.style.gap = "8px";
                            tagDiv.style.padding = "4px 6px";
                            tagDiv.style.border = "1px solid #888";
                            tagDiv.style.borderRadius = "6px";
                            tagDiv.style.background = "#222";
                            tagDiv.style.color = "#fff";
                            tagDiv.style.marginBottom = "4px";

                            // Thumbnail
                            const thumb = document.createElement("img");
                            thumb.className = "tag-item-thumb";
                            thumb.style.width = "32px";
                            thumb.style.height = "32px";
                            thumb.style.objectFit = "cover";
                            thumb.style.borderRadius = "4px";

                            const file = await this.handle.getFile();
                            thumb.src = URL.createObjectURL(file);

                            // Tag path
                            const path = document.createElement("span");
                            path.textContent = `${this.path}`;
                            path.style.flex = "1";
                            path.style.overflow = "hidden";
                            path.style.textOverflow = "ellipsis";
                            path.style.whiteSpace = "nowrap";

                            // Remove button
                            const removeBtn = document.createElement("button");
                            removeBtn.textContent = "×";
                            removeBtn.style.background = "#900";
                            removeBtn.style.border = "none";
                            removeBtn.style.color = "#fff";
                            removeBtn.style.cursor = "pointer";
                            removeBtn.style.fontWeight = "bold";
                            removeBtn.style.borderRadius = "4px";
                            removeBtn.style.padding = "0 6px";

                            // Add callback on click
                            if (callback && typeof callback === "function") {
                                removeBtn.addEventListener("click", (e) => {
                                    e.stopPropagation();
                                    callback(tagDiv,this);
                                });
                            }

                            tagDiv.append(thumb, path, removeBtn);
                            if (parent) parent.appendChild(tagDiv);
                            return tagDiv;
                        },


                     })
                }
        },
    }  
  await artItem.loadImages();
  return artItem;
}


artbookUI = {
    async createArtbookPanel(parent = null){
        const container = document.createElement('div');

        const tabs = createTabContainer(container);
        await readArtbookData()

        for (const artType of window.artbook) {       
            const artTypeContainer = document.createElement('div');
            artTypeContainer.className = "art-type-container";

            for (const artItem of artType.items) {

                const itemContainer = document.createElement("div");
                itemContainer.className = "art-item-container";

                const title = document.createElement("div");
                title.className = "art-item-title";
                title.textContent = artItem.name;

                const imagesContainer = document.createElement("div");
                imagesContainer.className = "art-images-container";

                for (const imgEntry of artItem.images) {
                    const file = await imgEntry.handle.getFile();
                    const url = URL.createObjectURL(file);
                    const name = imgEntry.name;

                    // --- IMAGE FILES ---
                    if (/\.(png|jpe?g|gif|webp)$/i.test(name)) {
                        const wrapper = document.createElement("div");
                        wrapper.className = "img-wrapper";

                        const img = document.createElement("img");
                        img.src = url;
                        img.className = "media-img";
                        img.title = name;

                        const label = document.createElement("div");
                        label.className = "img-label";
                        label.textContent = name;

                        wrapper.appendChild(img);
                        wrapper.appendChild(label);
                        imagesContainer.appendChild(wrapper);
                    }

                    // --- VIDEO FILES ---
                    /*
                    if (/\.(mp4|webm|ogg|mov|mkv)$/i.test(name)) {
                        const video = document.createElement("video");
                        video.src = url;
                        video.className = "media-video";
                        video.autoplay = true;
                        video.loop = true;
                        video.muted = true;
                        video.controls = true;

                        imagesContainer.appendChild(video);
                    }
                    */
                }

                itemContainer.append(title, imagesContainer);
                artTypeContainer.appendChild(itemContainer);
            }

            tabs.addTab({ title: artType.name, content: artTypeContainer });
        }

        console.log(window.artbook)

        if (parent) parent.appendChild(container);
    } ,  
    async createAddTagButton(parent = null, callback = null){
        const buttonWrapper = document.createElement("div");
        buttonWrapper.className = "add-tag-wrapper";

        const button = document.createElement("div");
        button.className = "add-tag-button";
        button.textContent = "Add Tag";

        const dropdown = document.createElement("div");
        dropdown.className = "tag-dropdown";

        // Build multi-level hover menu
        for (const artType of window.artbook) {
            const typeItem = document.createElement("div");
            typeItem.className = "dropdown-item";
            typeItem.textContent = artType.name;

            const itemMenu = document.createElement("div");
            itemMenu.className = "sub-dropdown";

            for (const artItem of artType.items) {
                const itemEntry = document.createElement("div");
                itemEntry.className = "dropdown-item";
                itemEntry.textContent = artItem.name;

                const imageMenu = document.createElement("div");
                imageMenu.className = "sub-dropdown";

                for (const img of artItem.images) {
                    const imgEntry = document.createElement("div");
                    imgEntry.className = "image-dropdown-item";

                    const label = document.createElement("span");
                    label.textContent = img.name;

                    const thumb = document.createElement("img");
                    thumb.className = "tag-img-thumb";

                    const file = await img.handle.getFile();
                    thumb.src = URL.createObjectURL(file);

                    // Add callback on click
                    if (callback && typeof callback === "function") {
                        imgEntry.addEventListener("click", (e) => {
                            e.stopPropagation(); // Prevent menu closing issues
                            callback(img);
                        });
                    }

                    imgEntry.appendChild(thumb);
                    imgEntry.appendChild(label);
                    imageMenu.appendChild(imgEntry);
                }

                itemEntry.appendChild(imageMenu);
                itemMenu.appendChild(itemEntry);
            }

            typeItem.appendChild(itemMenu);
            dropdown.appendChild(typeItem);
        }

        buttonWrapper.append(button, dropdown);
        if(parent) parent.appendChild(buttonWrapper);
    },
    async path2img(path) {
        for (const artType of window.artbook) {
            for (const artItem of artType.items) {
                for (const img of artItem.images) {
                    if (img.path === path) {
                        return img;
                    }
                }
            }
        }
        return null; 
    }

}


