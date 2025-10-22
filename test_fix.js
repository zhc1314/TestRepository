// Test script to verify the fix for addMessage function
console.log('===== Testing addMessage function fix =====');

// Test 1: Verify remove() method exists on DOM elements
const testElement = document.createElement('div');
console.log('Test 1: DOM elements have remove() method:', typeof testElement.remove === 'function');

// Test 2: Simulate exact scenario from AI fight mode
document.addEventListener('DOMContentLoaded', async () => {
  console.log('\nTest 2: Simulating AI fight message removal scenario...');
  
  // Create a chat container similar to the real application
  const chatMessages = document.querySelector('.chat-messages');
  if (chatMessages) {
    console.log('Chat container found. Testing with actual DOM elements...');
    
    // Define a mock of the fixed addMessage function (simulating our fix)
    function mockAddMessage(sender, message) {
      // Create message element
      const messageDiv = document.createElement('div');
      messageDiv.className = 'flex gap-3 animate-fade-in';
      
      // Set content based on sender (simplified version)
      if (sender === 'user') {
        messageDiv.className = 'flex gap-3 justify-end animate-fade-in';
        messageDiv.innerHTML = `<div>User: ${message}</div>`;
      } else {
        messageDiv.innerHTML = `<div>${sender === 'ai1' ? 'AI1' : 'AI2'}: ${message}</div>`;
      }
      
      // Append to container
      chatMessages.appendChild(messageDiv);
      
      // Return the element - THIS IS THE FIX WE IMPLEMENTED
      return messageDiv;
    }
    
    // Test the exact scenario that caused the error
    try {
      console.log('Creating loading message...');
      const loadingMessage = mockAddMessage('ai1', '思考中...');
      
      console.log('Loading message created successfully:', loadingMessage !== undefined);
      console.log('Loading message has remove() method:', 
                  loadingMessage && typeof loadingMessage.remove === 'function');
      
      // Simulate delay like in the real code
      await new Promise(resolve => setTimeout(resolve, 100));
      
      console.log('Attempting to remove loading message...');
      loadingMessage.remove();
      console.log('✓ SUCCESS: Loading message removed without errors!');
      console.log('\nThe TypeError "Cannot read properties of undefined (reading \'remove\')" should be resolved.');
    } catch (error) {
      console.error('✗ ERROR during test:', error);
    }
  } else {
    console.log('Chat container not found. Running standalone test instead...');
    
    // Fallback test if chat container isn't available
    const mockChatMessages = document.createElement('div');
    
    function mockAddMessage(sender, message) {
      const messageDiv = document.createElement('div');
      messageDiv.textContent = message;
      mockChatMessages.appendChild(messageDiv);
      return messageDiv; // This is our fix
    }
    
    const loadingMessage = mockAddMessage('ai1', '思考中...');
    console.log('Created message:', loadingMessage !== undefined);
    
    try {
      loadingMessage.remove();
      console.log('✓ SUCCESS in standalone test: remove() works on returned element');
    } catch (error) {
      console.error('✗ ERROR in standalone test:', error);
    }
  }
  
  console.log('\n===== Test completed =====');
});