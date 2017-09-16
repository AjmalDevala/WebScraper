chrome.runtime.onInstalled.addListener(() => {
  console.log("WordCraft installed!");
});

// Handle showing grammar errors
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "showGrammarErrors") {
    // Create a notification with grammar errors
    chrome.notifications.create({
      type: "basic",
      iconUrl: "assets/icon.png",
      title: "Grammar Suggestions",
      message: request.errors.map(error => 
        `Error in "${error.string}": Suggestions - ${error.suggestions.join(", ")}`
      ).join("\n")
    });
  }
});