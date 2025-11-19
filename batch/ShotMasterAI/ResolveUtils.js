
// Temp Function - replace later with proper module import/export
async function collectVideoFiles(folderHandle) {
  // Collect video files
  const videoFiles = [];
  for await (const entry of folderHandle.values()) {
    if (entry.kind === "file" && entry.name.match(/\.(mp4|mov|m4v)$/i)) {
      videoFiles.push(entry);
    }
  }

  if (videoFiles.length === 0) throw new Error("No video files found in folder.");
  return videoFiles;  
}

  // Duration helper
  async function getVideoDuration(fileHandle) {
    const file = await fileHandle.getFile();
    const url = URL.createObjectURL(file);
    return new Promise((resolve, reject) => {
      const video = document.createElement("video");
      video.preload = "metadata";
      video.src = url;
      video.onloadedmetadata = () => {
        URL.revokeObjectURL(url);
        resolve(video.duration);
      };
      video.onerror = reject;
    });
  }

  function prettyPrintXml(xmlString) {
  const PADDING = "  "; // 2 spaces
  const reg = /(>)(<)(\/*)/g;
  let xml = xmlString.replace(reg, "$1\r\n$2$3");
  let pad = 0;
  return xml
    .split("\r\n")
    .map((node) => {
      let indent = "";
      if (node.match(/<\/\w/)) pad -= 1;
      for (let i = 0; i < pad; i++) indent += PADDING;
      if (node.match(/<[^!?].*>[^<]*$/)) pad += 1;
      return indent + node;
    })
    .join("\r\n");
}

async function generateFCPXMLFromFolder(folderHandle) {
  videoFiles = await collectVideoFiles(folderHandle);
  const xmlString = await generateFCPXMLFromClips(videoFiles);
  saveLocalTextFile(folderHandle, "timeline.fcpxml", xmlString);
}

async function generateFCPXMLFromClips(videoFiles) {
  const baseRoot = "S:/Temp/!AI_Video/SCENE_010/SH040/results/";

  // Build clip metadata
  const clips = [];
  for (const handle of videoFiles) {
    const file = await handle.getFile();
    const durationSec = await getVideoDuration(handle);
    const frames = Math.round(durationSec * 30); // 30 fps integer frames

    clips.push({
      id: "r" + (clips.length + 2), // start after r0/r1
      name: file.name,
      durationFrames: frames,
      path: baseRoot + file.name
    });
  }

  const totalFrames = clips.reduce((sum, c) => sum + c.durationFrames, 0);

  // DOM XML builder
  const doc = document.implementation.createDocument("", "", null);

  const fcpxml = doc.createElement("fcpxml");
  fcpxml.setAttribute("version", "1.10");
  doc.appendChild(fcpxml);

  // Resources
  const resources = doc.createElement("resources");
  fcpxml.appendChild(resources);

  const format = doc.createElement("format");
  format.setAttribute("id", "r1");
  format.setAttribute("name", "FFVideoFormat1080p30");
  format.setAttribute("frameDuration", "1/30s");
  format.setAttribute("width", "1920");
  format.setAttribute("height", "1080");
  resources.appendChild(format);

  // Assets with <media-rep>
  for (const clip of clips) {
    const asset = doc.createElement("asset");
    asset.setAttribute("name", clip.name);
    asset.setAttribute("id", clip.id);
    asset.setAttribute("duration", `${clip.durationFrames}/30s`);
    asset.setAttribute("start", "0/1s");
    asset.setAttribute("format", "r1");
    asset.setAttribute("hasVideo", "1");

    const mediaRep = doc.createElement("media-rep");
    mediaRep.setAttribute("kind", "original-media");
    mediaRep.setAttribute("src", `file://localhost/${clip.path.replace(/\\/g, "/")}`);

    asset.appendChild(mediaRep);
    resources.appendChild(asset);
  }

  // Library / event / project
  const library = doc.createElement("library");
  fcpxml.appendChild(library);

  const event = doc.createElement("event");
  event.setAttribute("name", "Auto Import");
  library.appendChild(event);

  const project = doc.createElement("project");
  project.setAttribute("name", "Auto Timeline");
  event.appendChild(project);

  // Sequence
  const sequence = doc.createElement("sequence");
  sequence.setAttribute("format", "r1");
  sequence.setAttribute("duration", `${totalFrames}/30s`);
  sequence.setAttribute("tcStart", "0/1s");
  sequence.setAttribute("tcFormat", "NDF");
  project.appendChild(sequence);

  const spine = doc.createElement("spine");
  sequence.appendChild(spine);

  // Asset-clips
  let offsetFrames = 0;
  for (const clip of clips) {
    const clipEl = doc.createElement("asset-clip");
    clipEl.setAttribute("name", clip.name);
    clipEl.setAttribute("ref", clip.id);
    clipEl.setAttribute("enabled", "1");
    clipEl.setAttribute("duration", `${clip.durationFrames}/30s`);
    clipEl.setAttribute("start", "0/1s");
    clipEl.setAttribute("format", "r1");
    clipEl.setAttribute("offset", `${offsetFrames}/30s`);

    const adjust = doc.createElement("adjust-transform");
    adjust.setAttribute("anchor", "0 0");
    adjust.setAttribute("scale", "1 1");
    adjust.setAttribute("position", "0 0");
    clipEl.appendChild(adjust);

    spine.appendChild(clipEl);
    offsetFrames += clip.durationFrames;
  }

  // Serialize
  const serializer = new XMLSerializer();
  let xmlString = serializer.serializeToString(doc);
  xmlString = `<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n` + xmlString;

  // Save
  console.log("Created Resolve-compatible FCPXML with asset-clips and media-rep.");
  console.log(prettyPrintXml(xmlString));

  return xmlString;
}
