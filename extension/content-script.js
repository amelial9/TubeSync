console.log("👋 TubeSync content script loaded!");

const video = document.querySelector("video");

if (video) {
  console.log("🎬 video element found");
  console.log("⏱️ currentTime:", video.currentTime);
  console.log("▶️ paused?", video.paused);

  video.addEventListener("play", () => {
    console.log("🎥 Video started playing");
  });

  video.addEventListener("pause", () => {
    console.log("⏸️ Video paused");
  });

  video.addEventListener("timeupdate", () => {
    console.log("⏰ Updated time:", video.currentTime);
  });
} else {
  console.log("❌ no video element found");
}