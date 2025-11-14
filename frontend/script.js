class ChatBot {
  constructor() {
      this.apiUrl = 'http://localhost:5001/chat';
      this.initializeElements();
      this.setupEventListeners();
      this.setupSuggestionButtons();
  }

  initializeElements() {
      this.chatContainer = document.getElementById('chatContainer');
      this.messageInput = document.getElementById('messageInput');
      this.sendButton = document.getElementById('sendButton');
      this.clearButton = document.getElementById('clearChat');
      this.typingIndicator = document.getElementById('typingIndicator');
      this.charCount = document.getElementById('charCount');
      this.responseModal = document.getElementById('responseModal');
      this.closeModal = document.getElementById('closeModal');
  }

  setupEventListeners() {
      this.sendButton.addEventListener('click', () => this.sendMessage());
      this.messageInput.addEventListener('keypress', (e) => {
          if (e.key === 'Enter') {
              this.sendMessage();
          }
      });

      this.messageInput.addEventListener('input', () => this.updateCharCount());
      this.clearButton.addEventListener('click', () => this.clearChat());
      this.closeModal.addEventListener('click', () => this.closeResponseModal());

      // Close modal when clicking outside
      this.responseModal.addEventListener('click', (e) => {
          if (e.target === this.responseModal) {
              this.closeResponseModal();
          }
      });
  }

  setupSuggestionButtons() {
      const suggestionButtons = document.querySelectorAll('.suggestion-btn');
      suggestionButtons.forEach(button => {
          button.addEventListener('click', (e) => {
              const message = e.target.getAttribute('data-message');
              this.messageInput.value = message;
              this.sendMessage();
          });
      });
  }

  updateCharCount() {
      const length = this.messageInput.value.length;
      this.charCount.textContent = `${length}/500`;
      
      if (length > 450) {
          this.charCount.style.color = '#ef4444';
      } else if (length > 400) {
          this.charCount.style.color = '#f59e0b';
      } else {
          this.charCount.style.color = '#9ca3af';
      }
  }

  async sendMessage() {
      const message = this.messageInput.value.trim();
      if (!message) return;

      // Add user message to chat
      this.addMessage(message, 'user');
      this.messageInput.value = '';
      this.updateCharCount();

      // Show typing indicator
      this.showTypingIndicator();

      try {
          const response = await this.getBotResponse(message);
          
          // Check if it's a problem solution response and use appropriate method
          if (response.response_type && response.response_type.startsWith('problem_solution_')) {
              this.addProblemSolution(response);
          } else {
              this.addBotMessage(response);
          }
      } catch (error) {
          console.error('Error:', error);
          this.addBotMessage({
              bot_response: "I'm having trouble connecting right now. Please try again later.",
              response_type: "error",
              sentiment: "NEUTRAL",
              confidence: 0
          });
      } finally {
          this.hideTypingIndicator();
      }
  }

  async getBotResponse(message) {
      const response = await fetch(this.apiUrl, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: message })
      });

      if (!response.ok) {
          throw new Error('Network response was not ok');
      }

      return await response.json();
  }

  addMessage(message, sender) {
      const messageDiv = document.createElement('div');
      messageDiv.className = `message ${sender}`;
      
      const messageContent = document.createElement('div');
      messageContent.className = 'message-content';
      messageContent.textContent = message;

      messageDiv.appendChild(messageContent);
      this.chatContainer.appendChild(messageDiv);
      
      // Scroll to bottom
      this.scrollToBottom();
  }

  addBotMessage(responseData) {
      const messageDiv = document.createElement('div');
      messageDiv.className = 'message bot';
      
      const messageContent = document.createElement('div');
      messageContent.className = 'message-content';
      
      // Add message text
      const messageText = document.createElement('div');
      messageText.textContent = responseData.bot_response;
      messageContent.appendChild(messageText);

      // Add message info
      const messageInfo = document.createElement('div');
      messageInfo.className = 'message-info';
      
      const timestamp = document.createElement('span');
      timestamp.textContent = new Date().toLocaleTimeString();
      
      const messageType = document.createElement('span');
      messageType.className = 'message-type';
      messageType.textContent = responseData.response_type;
      
      messageInfo.appendChild(timestamp);
      messageInfo.appendChild(messageType);
      messageContent.appendChild(messageInfo);

      // Add click event to show response details
      messageContent.addEventListener('click', () => {
          this.showResponseModal(responseData);
      });

      messageDiv.appendChild(messageContent);
      this.chatContainer.appendChild(messageDiv);
      
      this.scrollToBottom();
  }

  // Add problem solution method
  addProblemSolution(responseData) {
      const messageDiv = document.createElement('div');
      messageDiv.className = 'message bot';
      
      const messageContent = document.createElement('div');
      messageContent.className = 'message-content problem-solution';
      
      // Add solution with better formatting
      const solutionText = document.createElement('div');
      solutionText.innerHTML = responseData.bot_response.replace(/\n/g, '<br>');
      messageContent.appendChild(solutionText);

      // Add solution details if available
      if (responseData.solution_details) {
          const details = document.createElement('div');
          details.className = 'solution-details';
          details.innerHTML = `
              <div class="detail-item">
                  <strong>Type:</strong> ${responseData.solution_details.type}
              </div>
          `;
          messageContent.appendChild(details);
      }

      // Add message info
      const messageInfo = document.createElement('div');
      messageInfo.className = 'message-info';
      
      const timestamp = document.createElement('span');
      timestamp.textContent = new Date().toLocaleTimeString();
      
      const messageType = document.createElement('span');
      messageType.className = 'message-type';
      messageType.textContent = responseData.response_type;
      
      messageInfo.appendChild(timestamp);
      messageInfo.appendChild(messageType);
      messageContent.appendChild(messageInfo);

      // Add click event to show response details
      messageContent.addEventListener('click', () => {
          this.showResponseModal(responseData);
      });

      messageDiv.appendChild(messageContent);
      this.chatContainer.appendChild(messageDiv);
      
      this.scrollToBottom();
  }

  showResponseModal(responseData) {
      document.getElementById('modalType').textContent = responseData.response_type;
      document.getElementById('modalSentiment').textContent = responseData.sentiment;
      document.getElementById('modalConfidence').textContent = responseData.confidence;
      
      this.responseModal.style.display = 'flex';
  }

  closeResponseModal() {
      this.responseModal.style.display = 'none';
  }

  showTypingIndicator() {
      this.typingIndicator.style.display = 'flex';
      this.scrollToBottom();
  }

  hideTypingIndicator() {
      this.typingIndicator.style.display = 'none';
  }

  scrollToBottom() {
      setTimeout(() => {
          this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
      }, 100);
  }

  clearChat() {
      // Keep only the welcome message
      const welcomeMessage = document.querySelector('.welcome-message');
      this.chatContainer.innerHTML = '';
      this.chatContainer.appendChild(welcomeMessage);
      
      // Add a confirmation message
      this.addBotMessage({
          bot_response: "Chat history has been cleared! How can I help you?",
          response_type: "system",
          sentiment: "POSITIVE",
          confidence: 1
      });
  }
}

// Initialize the chatbot when the page loads
document.addEventListener('DOMContentLoaded', () => {
  new ChatBot();
});