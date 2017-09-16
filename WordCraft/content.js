document.addEventListener("mouseup", async (event) => {
  // Get the currently selected text
  const selectedText = window.getSelection().toString().trim();

  // Check if there's selected text and it's not empty
  if (selectedText && selectedText.length > 0) {
    try {
      // Improved error handling and validation
      if (selectedText.length > 500) {
        console.warn("Text selection too long. Please select a shorter text.");
        return;
      }

      // Call Grammar API (using After the Deadline API)
      const response = await fetch(
        "https://api.afterthedeadline.com/checkDocument",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            Accept: "application/xml", // Specify XML response
          },
          body: new URLSearchParams({
            key: process.env.GRAMMAR_API_KEY || "your-api-key-here", // Use environment variable
            data: selectedText,
          }),
        }
      );

      // Check if the response is successful
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.text();

      // Parse XML response
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(data, "text/xml");

      // Extract error details with more comprehensive parsing
      const errors = xmlDoc.getElementsByTagName("error");
      const errorList = [];

      for (let error of errors) {
        const errorObj = {
          type: error.getAttribute("type") || "Unknown Error",
          string: error.getAttribute("string") || selectedText,
          suggestions: Array.from(error.getElementsByTagName("suggestion"))
            .map((suggestion) => suggestion.textContent)
            .filter((suggestion) => suggestion.trim() !== ""), // Remove empty suggestions
          context: error.getAttribute("context") || "",
        };

        // Only add if suggestions exist
        if (errorObj.suggestions.length > 0) {
          errorList.push(errorObj);
        }
      }

      // Create a popup or notification with grammar suggestions
      if (errorList.length > 0) {
        chrome.runtime.sendMessage(
          {
            action: "showGrammarErrors",
            errors: errorList,
            originalText: selectedText,
          },
          (response) => {
            if (chrome.runtime.lastError) {
              console.error("Error sending message:", chrome.runtime.lastError);
            }
          }
        );
      } else {
        // No errors found
        chrome.runtime.sendMessage({
          action: "noErrorsFound",
          text: selectedText,
        });
      }
    } catch (error) {
      console.error("Comprehensive error checking failed:", error);

      // Send error information back to extension
      chrome.runtime.sendMessage({
        action: "grammarCheckError",
        errorMessage: error.toString(),
        originalText: selectedText,
      });
    }
  }
});

// Enhanced message listener with more robust correction application
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "applyCorrection") {
    try {
      // Get current selection
      const selection = window.getSelection();

      // Validate selection
      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        const selectedText = range.toString();

        // Additional validation
        if (selectedText === request.originalText) {
          // Replace the selected text with the suggested correction
          range.deleteContents();

          // Create a new text node with the correction
          const correctionNode = document.createTextNode(request.correction);
          range.insertNode(correctionNode);

          // Select the newly inserted text
          const newRange = document.createRange();
          newRange.selectNodeContents(correctionNode);
          selection.removeAllRanges();
          selection.addRange(newRange);

          // Provide feedback about successful correction
          sendResponse({
            status: "success",
            message: "Correction applied successfully",
          });
        } else {
          // Mismatched text - prevent incorrect correction
          sendResponse({
            status: "error",
            message: "Selected text does not match original text",
          });
        }
      }
    } catch (error) {
      console.error("Error applying correction:", error);
      sendResponse({
        status: "error",
        message: error.toString(),
      });
    }

    // Return true to indicate we wish to send a response asynchronously
    return true;
  }
});

// Utility function to highlight text with grammar issues
function highlightGrammarIssues(errors) {
  const selection = window.getSelection();
  if (selection.rangeCount > 0) {
    const range = selection.getRangeAt(0);
    const span = document.createElement("span");
    span.style.backgroundColor = "yellow";
    span.style.color = "red";
    span.title = errors
      .map((e) => `${e.type}: ${e.suggestions.join(", ")}`)
      .join("\n");

    range.surroundContents(span);
  }
}
