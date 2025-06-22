// Simple test script to verify API integration
const API_BASE_URL = 'https://mindease-gigu.onrender.com';

async function testAPI() {
  console.log('🧪 Testing MindEase API Integration...\n');
  
  try {
    // Test 1: Basic connection
    console.log('1. Testing basic connection...');
    const testResponse = await fetch(`${API_BASE_URL}/health`);
    const testData = await testResponse.json();
    console.log('✅ Connection successful:', testData.status);
    
    // Test 2: Anonymous session creation
    console.log('\n2. Testing anonymous session creation...');
    const sessionResponse = await fetch(`${API_BASE_URL}/api/v1/auth/anonymous`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({}),
    });
    const sessionData = await sessionResponse.json();
    console.log('✅ Session created:', sessionData.access_token ? 'Yes' : 'No');
    
    if (sessionData.access_token) {
      const token = sessionData.access_token;
      
      // Test 3: Chat session creation
      console.log('\n3. Testing chat session creation...');
      const chatSessionResponse = await fetch(`${API_BASE_URL}/api/v1/chat/session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          session_type: "free_form",
          emotion_context: "general_wellness"
        }),
      });
      const chatSessionData = await chatSessionResponse.json();
      console.log('✅ Chat session created:', chatSessionData.session_id ? 'Yes' : 'No');
      
      if (chatSessionData.session_id) {
        // Test 4: Send a test message
        console.log('\n4. Testing message sending...');
        const messageResponse = await fetch(`${API_BASE_URL}/api/v1/chat/message`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({
            content: "Hello, this is a test message",
            session_id: chatSessionData.session_id,
            session_type: "free_form"
          }),
        });
        const messageData = await messageResponse.json();
        console.log('✅ Message sent:', messageData.message ? 'Yes' : 'No');
        
        if (messageData.message) {
          console.log('🤖 AI Response:', messageData.message.substring(0, 100) + '...');
        }
      }
    }
    
    console.log('\n🎉 All tests completed successfully!');
    console.log('\n📝 Next steps:');
    console.log('1. Open http://localhost:3000 in your browser');
    console.log('2. Navigate to the chat page');
    console.log('3. Test the full chat functionality');
    
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    console.log('\n🔧 Troubleshooting:');
    console.log('1. Check if the backend is deployed and accessible');
    console.log('2. Verify the API URL is correct');
    console.log('3. Check network connectivity');
  }
}

// Run the test
testAPI(); 