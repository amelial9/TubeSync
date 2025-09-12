console.log("👋 TubeSync content script loaded!");

// const video = document.querySelector("video");

// if (video) {
//   console.log("🎬 video element found");
//   console.log("⏱️ currentTime:", video.currentTime);
//   console.log("▶️ paused?", video.paused);

//   video.addEventListener("play", () => {
//     console.log("🎥 Video started playing");
//   });

//   video.addEventListener("pause", () => {
//     console.log("⏸️ Video paused");
//   });

//   video.addEventListener("timeupdate", () => {
//     console.log("⏰ Updated time:", video.currentTime);
//   });
// } else {
//   console.log("❌ no video element found");
// }


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

  const title = document.title;
  const channel = document.querySelector('#text-container yt-formatted-string')?.innerText || "Unknown";

  // console.log("[TubeSync debug]", {
  //   title,
  //   author: channel,
  //   playing: !video.paused,
  //   time: Math.floor(video.currentTime),
  //   duration: Math.floor(video.duration),
  // });

  return {
    title,
    author: channel,
    playing: !video.paused,
    time: Math.floor(video.currentTime),
    duration: Math.floor(video.duration),
  };
}

setInterval(() => {
  chrome.storage.sync.get("enabled", ({ enabled }) => {
    if (enabled && socket.readyState === WebSocket.OPEN) {
      const payload = getPlaybackData();
      if (payload) {
        socket.send(JSON.stringify(payload));
        // console.log("[TubeSync]", payload);
      }
    }
  });
}, 500);
