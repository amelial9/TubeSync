console.log("TubeSync content script loaded");

let socket = new WebSocket("ws://localhost:3000");

socket.onopen = () => {
  console.log("TubeSync WebSocket connected");
};

socket.onerror = (e) => {
  console.error("TubeSync WebSocket error", e);
};

socket.onclose = () => {
  console.log("TubeSync WebSocket closed");
};

function getPlaybackData() {
  const video = document.querySelector("video");
  if (!video) return null;

  let title = document.title;
  if (title.endsWith(" - YouTube")) {
    title = title.replace(" - YouTube", "");
  }

  const channel =
    document.querySelector("#text-container yt-formatted-string")?.innerText ||
    "Unknown";

  const clipButton = document.querySelector(".ytp-clip-watch-full-video-button");
  const isLive =
    clipButton && clipButton.innerText.toLowerCase().includes("live stream");

  return {
    title,
    author: channel,
    time: Math.floor(video.currentTime),
    duration: Math.floor(video.duration),
    isLive,
  };
}

setInterval(() => {
  try {
    chrome.storage.sync.get("enabled", ({ enabled }) => {
      if (enabled && socket.readyState === WebSocket.OPEN) {
        const payload = getPlaybackData();
        if (payload) {
          socket.send(JSON.stringify(payload));
          console.log("[TubeSync sending]", payload);
        }
      }
    });
  } catch (err) {
    console.warn("[TubeSync] Extension context invalidated, stopping.");
  }
}, 500);
