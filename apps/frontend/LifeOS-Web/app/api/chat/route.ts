// app/api/chat/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const { message } = await req.json();

    // WARNING: THIS IS A MOCK RESPONSE FOR DEVELOPMENT
    // The actual API call to Claude should be implemented here.
    // The CLAUDE_API_KEY should be accessed securely from environment variables.
    if (!process.env.CLAUDE_API_KEY) {
      console.warn("CLAUDE_API_KEY is not set. Using mock response.");
      // In a real scenario, you would likely return an error here.
      // For this example, we'll proceed with a mock response.
    }

    // MOCK API CALL (replace with actual Claude API call)
    // const claudeResponse = await someClaudeApiClient.post({
    //   apiKey: process.env.CLAUDE_API_KEY,
    //   prompt: message,
    // });

    // Simulate a delay to mimic a real API call
    await new Promise(resolve => setTimeout(resolve, 500));

    const mockResponse = {
        text: `This is a mocked response to your message: "${message}". The Claude API is not yet connected, but this confirms the secure backend endpoint is working.`
    };

    return NextResponse.json({ reply: mockResponse.text });

  } catch (error) {
    console.error('Error in chat API route:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
