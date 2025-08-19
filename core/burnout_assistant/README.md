# Burnout Recovery Assistant

The Burnout Recovery Assistant is an AI-powered tool designed to help users create personalized wellness plans to prevent and recover from burnout. It uses different prompting techniques to generate tailored advice based on the user's input.

## Features

- **Multiple Prompting Styles**: Choose from various AI prompting techniques
- **Personalized Wellness Plans**: Get customized advice based on your routine
- **PDF Export**: Download your wellness plan as a PDF
- **Interactive Interface**: User-friendly Streamlit interface

## Available Prompting Styles

1. **Zero-shot**: Direct advice based on your input
2. **One-shot**: Advice based on a similar example
3. **Few-shot**: Advice based on multiple examples
4. **Role-based**: Structured advice from a counselor's perspective
5. **Chain-of-thought**: Detailed, step-by-step analysis

## Usage

1. **Access the Assistant**:
   - Navigate to the "Burnout Assistant" section in the dashboard
   - The assistant will display a text area for your input

2. **Describe Your Routine**:
   - Enter details about your daily routine, work schedule, or specific symptoms
   - Example: "I work 10 hours a day, have a long commute, and feel exhausted all the time"

3. **Choose a Prompting Style**:
   - Select a prompting style from the dropdown menu
   - Each style provides a different approach to generating advice

4. **Generate Your Plan**:
   - Click "Generate Recovery Plan"
   - The assistant will analyze your input and create a personalized plan

5. **Download Options**:
   - View the generated plan in the chat interface
   - Click "Download as PDF" to save a copy

## Configuration

The assistant requires the following environment variable to be set in your `.env` file:

```env
# Gemini API Configuration
API_KEY=your_gemini_api_key
```

## Dependencies

- google-generativeai
- streamlit
- python-dotenv
- fpdf (for PDF generation)

## Integration

The Burnout Recovery Assistant is integrated into the main dashboard and can be accessed from the sidebar. It's designed to work seamlessly with the rest of the Automation Suite.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
