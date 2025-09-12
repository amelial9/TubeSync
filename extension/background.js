console.log("TubeSync background script loaded");

chrome.runtime.onInstalled.addListener((details) => {
  console.log("TubeSync extension installed/updated", details);
  
  chrome.storage.sync.set({
    enabled: true
  });
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log("Background received message:", request);
  
  if (request.action === "getStatus") {
    chrome.storage.sync.get("enabled", (result) => {
      sendResponse({ enabled: result.enabled || false });
    });
    return true;
  }
});
