# Agentic AI Assistant

The Agentic AI Assistant is a powerful tool that integrates with the Gemini AI model to provide interactive assistance with various tasks. It's designed to be modular and extensible, allowing for easy integration of new tools and capabilities.

## Features

- **Interactive Chat Interface**: Natural language interaction with the AI assistant
- **Tool Integration**: Can use various tools to perform tasks
- **Context Awareness**: Maintains conversation history for coherent interactions
- **Streamlit Integration**: Seamless integration with the main dashboard

## Usage

1. **Accessing the Assistant**:
   - Navigate to the "Agentic AI Assistant" section in the dashboard
   - The assistant will greet you with a welcome message

2. **Making Queries**:
   - Type your question or request in the chat input
   - The assistant will process your request and provide a response

3. **Example Queries**:
   - "What can you help me with?"
   - "Scan my project folder and summarize the README files"
   - "Help me debug this Python code"

## Configuration

The assistant requires the following environment variables to be set in your `.env` file:

```env
# Gemini API Configuration
API_KEY=your_gemini_api_key
```

## Dependencies

- google-generativeai
- streamlit
- python-dotenv

## Integration

The assistant is integrated into the main dashboard and can be extended by adding new tools to the `tools` directory. Each tool should implement a standard interface for the assistant to interact with it.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
