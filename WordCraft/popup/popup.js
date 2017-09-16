document.addEventListener('DOMContentLoaded', () => {
  const textInput = document.getElementById('textInput');
  const checkGrammarBtn = document.getElementById('checkGrammarBtn');
  const errorsContainer = document.getElementById('errorsContainer');
  const clearBtn = document.getElementById('clearBtn');

  // Check Grammar Button Click Handler
  checkGrammarBtn.addEventListener('click', () => {
      const text = textInput.value.trim();
      if (!text) {
          alert('Please enter some text to check.');
          return;
      }

      // Send message to content script to check grammar
      chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
          chrome.tabs.sendMessage(tabs[0].id, {
              action: 'checkGrammar',
              text: text
          }, handleGrammarResponse);
      });
  });

  // Clear Button Click Handler
  clearBtn.addEventListener('click', () => {
      textInput.value = '';
      errorsContainer.innerHTML = '';
  });

  // Handle Grammar Check Response
  function handleGrammarResponse(response) {
      if (!response || !response.errors) {
          errorsContainer.innerHTML = '<p class="text-gray-500">No grammar errors found.</p>';
          return;
      }

      // Clear previous errors
      errorsContainer.innerHTML = '';

      // Display Errors
      response.errors.forEach((error, index) => {
          const errorElement = document.createElement('div');
          errorElement.classList.add(
              'error-item', 
              'p-3', 
              'bg-white', 
              'rounded', 
              'shadow-sm', 
              'border', 
              'flex', 
              'justify-between', 
              'items-center'
          );

          errorElement.innerHTML = `
              <div>
                  <p class="font-semibold text-red-600">${error.type}</p>
                  <p class="text-gray-700">Original: "${error.string}"</p>
                  <p class="text-green-600">Suggestions: ${error.suggestions.join(', ')}</p>
              </div>
              <button 
                  data-suggestion="${error.suggestions[0]}" 
                  class="apply-suggestion btn-animate bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600"
              >
                  Apply
              </button>
          `;

          // Add event listener to apply suggestion
          errorElement.querySelector('.apply-suggestion').addEventListener('click', (e) => {
              const suggestion = e.target.getAttribute('data-suggestion');
              chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
                  chrome.tabs.sendMessage(tabs[0].id, {
                      action: 'applySuggestion',
                      suggestion: suggestion
                  });
              });
          });

          errorsContainer.appendChild(errorElement);
      });
  }
});