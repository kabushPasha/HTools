

(() => {
  // INIT
  let saved = JSON.parse(localStorage.getItem('videoSegmentData') || '{}');

  let videoFileURL = null;
  let videoFileName = "input.mp4"; // default fallback name for ffmpeg command
  let keyframeTimes = [];
  let segments = [];
  let currentPage = 1;
  let perPage = 6;
  let videoScale = 1; // 1 = normal size
  const baseWidth = 320; // base width of each video container

  let showFavoritesOnly = false;
  //const favorites = new Set(); // store segment indices

  const videoGrid = document.getElementById('videoGrid');
  const pagination = document.getElementById('pagination');
  const videoFileInput = document.getElementById('videoFileInput');
  const keyframeFileInput = document.getElementById('keyframeFileInput');
  const zoomInBtn = document.getElementById('zoomInBtn');
  const zoomOutBtn = document.getElementById('zoomOutBtn');
  const showFavoritesToggle = document.getElementById('showFavoritesToggle');
  const generateFFmpegBtn = document.getElementById('generateFFmpegBtn');

  // UTIL FUNCTIONS
  function parseKeyframes(text) {
    return text
      .split(',')
      .map(s => parseFloat(s.trim()))
      .filter(n => !isNaN(n))
      .sort((a, b) => a - b);
  }

  function generateSegments(times) {
    const segs = [];
    for (let i = 0; i < times.length - 1; i++) {
      segs.push({ start: times[i] + 0.01, end: times[i + 1], index: i, favorite: false });
    }
    return segs;
  }

  function clearOldVideo() {
    if (videoFileURL) {
      URL.revokeObjectURL(videoFileURL);
      videoFileURL = null;
    }
    keyframeTimes = [];
    segments = [];
    currentPage = 1;
    videoGrid.innerHTML = '';
    pagination.innerHTML = '';
    updateFavoritesToggle();
    updateGenerateButton();
  }

  function renderPage() {
    Array.from(videoGrid.children).forEach(container => {
      const video = container.querySelector('video');
      if (video) {
        video.pause();
        video.src = '';
        video.load();
      }
    });

    videoGrid.innerHTML = '';
    if (!videoFileURL || segments.length === 0) {
      pagination.innerHTML = '';
      return;
    }

    let displaySegments = showFavoritesOnly
      ? segments.filter(s => s.favorite)
      : segments;

    if (displaySegments.length === 0) {
      videoGrid.innerHTML = '<p style="width: 100%; text-align:center; color: #888;">No segments to display.</p>';
      pagination.innerHTML = '';
      return;
    }

    const totalPages = Math.ceil(displaySegments.length / perPage);
    updatePageTitle(totalPages);
    if (currentPage > totalPages) currentPage = totalPages || 1;

    const startIndex = (currentPage - 1) * perPage;
    const pageSegments = displaySegments.slice(startIndex, startIndex + perPage);
    pageSegments.forEach((seg, idx) => {
      const container = document.createElement('div');
      container.className = 'video-container';
      container.style.width = (baseWidth * videoScale) + 'px';
      container.style.position = 'relative';
      container.style.overflow = 'hidden';

      const video = document.createElement('video');
      video.src = videoFileURL;
      video.muted = true;
      video.controls = false;
      video.loop = false;
      video.preload = "auto";
      video.style.width = '100%';
      video.setAttribute('tabindex', '-1');

      video.addEventListener('loadedmetadata', () => {
        if (video.currentTime < seg.start || video.currentTime > seg.end) {
          video.currentTime = seg.start;
        }
        video.play();
      });

      video.addEventListener('timeupdate', () => {
        if (video.currentTime >= seg.end) {
          video.currentTime = seg.start;
          video.play();
        }
      });

      container.appendChild(video);

      // ⏱ Duration overlay (bottom-left)
      const durationOverlay = document.createElement('div');
      durationOverlay.className = 'duration-overlay';
      durationOverlay.style.position = 'absolute';
      durationOverlay.style.left = '8px';
      durationOverlay.style.bottom = '6px';
      durationOverlay.style.fontSize = '12px';
      durationOverlay.style.color = '#fff';
      durationOverlay.style.background = 'rgba(0, 0, 0, 0.5)';
      durationOverlay.style.padding = '2px 6px';
      durationOverlay.style.borderRadius = '4px';
      durationOverlay.style.pointerEvents = 'none';
      const duration = seg.end - seg.start;
      durationOverlay.textContent = `⏱ ${secondsToHHMMSS(duration)}`;
      container.appendChild(durationOverlay);

      // ➡ Join button (bottom-right)
      if (seg.index < segments.length - 1 && !showFavoritesOnly) {
        const joinArrow = document.createElement('button');
        joinArrow.textContent = '➡';
        joinArrow.title = 'Join with next segment';
        joinArrow.classList.add('overlay-button');
        joinArrow.style.position = 'absolute';
        joinArrow.style.bottom = '6px';
        joinArrow.style.right = '8px';
        joinArrow.style.fontSize = '14px';
        joinArrow.style.padding = '2px 6px';
        joinArrow.style.background = 'rgba(255, 255, 255, 0.1)';
        joinArrow.style.color = '#fff';
        joinArrow.style.border = 'none';
        joinArrow.style.borderRadius = '4px';
        joinArrow.style.cursor = 'pointer';
        // When joining segments:
        joinArrow.addEventListener('click', () => {
          const nextSeg = segments[seg.index + 1];
          if (!nextSeg) return;

          // Extend current segment
          seg.end = nextSeg.end;

          // If next segment was favorited, keep current segment as favorite
          //seg.favorite = seg.favorite || nextSeg.favorite;
          seg.favorite = true;

          // Remove next segment and reindex
          segments.splice(seg.index + 1, 1);
          segments = segments.map((s, i) => ({ ...s, index: i }));

          renderPage();
          updateFavoritesToggle();
        updateGenerateButton();        
          saveToLocalStorage();
        });
        container.appendChild(joinArrow);
      }

      // ★ Favorite star (top-right)
      const favBtn = document.createElement('button');
      favBtn.className = 'fav-btn star-icon-button';
      favBtn.innerHTML = seg.favorite ? '★' : '☆';
      if (seg.favorite) {
        favBtn.classList.add('favorited');
      }
      favBtn.title = 'Toggle favorite for this segment';
      favBtn.addEventListener('click', e => {
        e.stopPropagation();
        seg.favorite = !seg.favorite;
        favBtn.innerHTML = seg.favorite ? '★' : '☆';
        favBtn.classList.toggle('favorited', seg.favorite);
        updateFavoritesToggle();
        updateGenerateButton();
        saveToLocalStorage();
      });
      container.appendChild(favBtn);

      videoGrid.appendChild(container);
    });

    renderPagination(displaySegments.length);
  }

  // Save Favorites to local Storage
  function saveToLocalStorage() {
    if (!videoFileName) return;
    saved[videoFileName] = {
      segments,
      currentPage,
      perPage,
    };
    localStorage.setItem('videoSegmentData', JSON.stringify(saved));
  }

  function loadFromLocalStorage() {
    if (saved[videoFileName]) {
      const data = saved[videoFileName];
      if (data.segments) segments = data.segments;
      if (data.currentPage) currentPage = data.currentPage;
      if (data.perPage) {
        perPage = data.perPage;
        if (perPageInput) perPageInput.value = perPage;
      }
      renderPage();
      updateFavoritesToggle();
      updateGenerateButton();
    }
  }

  function updatePageTitle(totalPages) {
    const favCount = segments.filter(s => s.favorite).length;
    document.title = `Page ${currentPage}/${totalPages} | ★ ${favCount}`;
  }

  function renderPagination(totalSegments) {
    pagination.innerHTML = '';
    const totalPages = Math.ceil(totalSegments / perPage);
    if (totalPages <= 1) return;

    for (let i = 1; i <= totalPages; i++) {
      const btn = document.createElement('button');
      btn.className = 'page-btn';
      btn.textContent = i;
      btn.disabled = (i === currentPage);
      if (i === currentPage) {
        btn.classList.add('active');
      }
      btn.addEventListener('click', () => {
        if (i !== currentPage) {
          currentPage = i;
          saveToLocalStorage();
          renderPage();
        }
      });
      pagination.appendChild(btn);
    }
  }

  function zoom(delta) {
    videoScale = Math.min(3, Math.max(0.3, videoScale + delta));
    renderPage();
  }

  function updateFavoritesToggle() {
    const favCount = segments.filter(s => s.favorite).length;
    showFavoritesToggle.disabled = favCount === 0;
    if (!showFavoritesOnly) {
      showFavoritesToggle.textContent = "Show Favorites Only: OFF";
      showFavoritesToggle.classList.remove('active');
    } else {
      showFavoritesToggle.textContent = "Show Favorites Only: ON";
      showFavoritesToggle.classList.add('active');
    }
  }

  function updateGenerateButton() {
    const favCount = segments.filter(s => s.favorite).length;
    generateFFmpegBtn.disabled = favCount === 0;
  }

  function secondsToHHMMSS(sec) {
    const h = Math.floor(sec / 3600);
    const m = Math.floor((sec % 3600) / 60);
    const s = (sec % 60).toFixed(3);
    return (h > 0 ? h.toString().padStart(2, '0') + ':' : '') +
      m.toString().padStart(2, '0') + ':' +
      s.toString().padStart(6, '0');
  }
  // Update ffmpeg command generation
  function generateFFmpegCommand() {
    if (!videoFileURL) {
      alert("Please load a video file first.");
      return;
    }
    const favoriteSegments = segments.filter(s => s.favorite);
    if (favoriteSegments.length === 0) {
      alert("No favorite segments selected.");
      return;
    }

    let inputFileName = videoFileName;
    if (/\s/.test(inputFileName)) {
      inputFileName = `"${inputFileName}"`;
    }

    const baseName = videoFileName.replace(/\.[^/.]+$/, '');

    const outputDir = `CUTS/${baseName}`;
    const cmdLines = [`mkdir "${outputDir}" -Force`];

    //const cmdLines = ['mkdir .\CUTS -Force'];

    favoriteSegments.forEach((seg, i) => {
      const start = seg.start + 0.1;
      const end = seg.end;
      //const outputFile = `"CUTS/CUT_${baseName}_segment${i + 1}.mp4"`;
      const outputFile = `"${outputDir}/CUT_${baseName}_segment${i + 1}.mp4"`;
      //const line = `ffmpeg -n -ss ${start.toFixed(3)} -to ${end.toFixed(3)} -i ${inputFileName} -c copy -avoid_negative_ts make_zero ${outputFile}`;
      const line = `ffmpeg -v error -n -ss ${start.toFixed(3)} -to ${end.toFixed(3)} -i ${inputFileName} -c copy -avoid_negative_ts make_zero ${outputFile}`;
      cmdLines.push(line);
    });

    cmdLines.push("");
    return cmdLines.join('\r\n');
  }
  videoFileInput.addEventListener('change', e => {
    clearOldVideo();
    const file = e.target.files[0];
    if (!file) return;
    videoFileName = file.name;
    videoFileURL = URL.createObjectURL(file);
    renderPage();
    showFavoritesToggle.disabled = false;
    generateFFmpegBtn.disabled = true;
  });

  keyframeFileInput.addEventListener('change', e => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      keyframeTimes = parseKeyframes(reader.result);
      segments = generateSegments(keyframeTimes);
      currentPage = 1;
      renderPage();
      updateFavoritesToggle();
      updateGenerateButton();
    };
    reader.readAsText(file);
  });

  zoomInBtn.addEventListener('click', () => zoom(0.2));
  zoomOutBtn.addEventListener('click', () => zoom(-0.2));

  showFavoritesToggle.addEventListener('click', () => {
    showFavoritesOnly = !showFavoritesOnly;
    updateFavoritesToggle();
    renderPage();
  });

  generateFFmpegBtn.addEventListener('click', async () => {
    const cmdText = generateFFmpegCommand();
    if (cmdText) {
      try {
        await navigator.clipboard.writeText(cmdText);
        alert('ffmpeg CMD script copied to clipboard!');
      } catch (err) {
        alert('Failed to copy to clipboard. Please try again.');
      }
    }
  });


  // Drag & Drop Cue + Handling
  const dropOverlay = document.getElementById('dropOverlay');
  let dragCounter = 0;

  function handleFileDrop(file) {
    console.log('📦 Dropped file:', file.name, file.type);

    if (file.type.startsWith('video/')) {
      console.log('🎞️ Treating as video file');
      clearOldVideo();
      videoFileName = file.name;
      videoFileURL = URL.createObjectURL(file);
      renderPage();
      showFavoritesToggle.disabled = false;
      generateFFmpegBtn.disabled = true;
    } else if (file.name.endsWith('.txt')) {
      console.log('📄 Treating as keyframe text file');
      const reader = new FileReader();
      reader.onload = () => {
        console.log('✅ Keyframe file loaded');
        keyframeTimes = parseKeyframes(reader.result);
        segments = generateSegments(keyframeTimes);
        currentPage = 1;
        renderPage();
        updateFavoritesToggle();
        updateGenerateButton();
        loadFromLocalStorage();
      };
      reader.onerror = (err) => {
        console.error('❌ Error reading file:', err);
      };
      reader.readAsText(file);
    } else {
      console.warn('❓ Unsupported file type:', file.name);
    }


  }

  window.addEventListener('drop', (e) => {
    e.preventDefault();
    dropOverlay.style.display = 'none';
    dragCounter = 0;

    const files = Array.from(e.dataTransfer.files);
    console.log('📥 Files dropped:', files.map(f => f.name));
    if (files.length === 0) return;

    files.forEach(handleFileDrop);
  });


  window.addEventListener('dragenter', (e) => {
    e.preventDefault();
    dragCounter++;
    dropOverlay.style.display = 'flex';
  });

  window.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dragCounter--;
    if (dragCounter <= 0) {
      dropOverlay.style.display = 'none';
      dragCounter = 0;
    }
  });

  window.addEventListener('dragover', (e) => {
    e.preventDefault();
  });

  // Add keyboard navigation for pagination
  window.addEventListener('keydown', (e) => {
    const isInputFocused = document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA';
    if (isInputFocused) return;

    const totalSegments = showFavoritesOnly
      ? segments.filter(s => s.favorite).length
      : segments.length;
    const totalPages = Math.ceil(totalSegments / perPage);

    if (e.key === 'ArrowRight') {
      if (currentPage < totalPages) {
        currentPage++;
        renderPage();
      }
    } else if (e.key === 'ArrowLeft') {
      if (currentPage > 1) {
        currentPage--;
        renderPage();
      }
    }
  });


  // Add mouse wheel navigation for pagination
  let wheelTimeout = null;

  window.addEventListener('wheel', (e) => {
    const isInputFocused = document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA';
    if (isInputFocused) return;

    const totalSegments = showFavoritesOnly
      ? segments.filter(s => s.favorite).length
      : segments.length;
    const totalPages = Math.ceil(totalSegments / perPage);

    // Debounce scrolling to prevent rapid switching
    if (wheelTimeout) return;
    wheelTimeout = setTimeout(() => wheelTimeout = null, 150); // adjust as needed

    if (e.deltaY > 0 && currentPage < totalPages) {
      currentPage++;
      renderPage();
      saveToLocalStorage();
    } else if (e.deltaY < 0 && currentPage > 1) {
      currentPage--;
      renderPage();
      saveToLocalStorage();
    }
  });

  // reload on Middle mouse
  document.addEventListener('mousedown', (e) => {
    if (e.button === 1) { // 1 = middle mouse button
      e.preventDefault(); // Prevent opening links in new tab (default behavior)
      location.reload();  // Reload the page
    }
  });


  // Clear Saved Videos BTN
  document.getElementById('clearLocalStorageBtn').addEventListener('click', () => {
    if (confirm("Are you sure you want to clear all saved favorites and page history?")) {
      localStorage.removeItem('videoSegmentData');
      saved = {};
      alert("Saved data cleared.");
    }
  });

  // Change Per page number
  const perPageInput = document.getElementById('perPageInput');

  perPageInput.addEventListener('change', (e) => {
    const value = parseInt(e.target.value, 10);
    if (!isNaN(value) && value > 0) {
      perPage = value;
      currentPage = 1;
      renderPage();
      saveToLocalStorage();
    } else {
      e.target.value = perPage; // restore previous value
    }
  });




})();




