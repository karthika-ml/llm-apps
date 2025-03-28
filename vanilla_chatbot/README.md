# chatbotprojects
# OpenAI Chatbot Vanilla

This is a simple chatbot application that demonstrates how to use the OpenAI API with Streamlit. It provides a basic interface for interacting with a GPT model (like `gpt-3.5-turbo` or `gpt-4`).

## Features

*   **Simple and clean interface:**  A straightforward Streamlit app for easy interaction.
*   **OpenAI integration:** Uses the `openai` library to communicate with OpenAI's models.
*   **Basic chat functionality:** Allows you to send messages and receive responses from the chatbot.

## Getting Started

1.  **Installation:**
    ```bash
    pip install streamlit openai
    ```

2.  **Set your OpenAI API key:**
    *   Create a `.env` file in the project directory.
    *   Add your API key to the `.env` file:
        ```
        OPENAI_API_KEY=your_actual_api_key_here
        OPENAI_MODEL=your_openai_model_here
        ```

3.  **Run the app:**
    ```bash
    streamlit run openai_chatbot_vanilla.py 
    ```

## Usage

*   Type your message in the text input area.
*   Click the "Send" button to send your message to the chatbot.
*   The chatbot's response will be displayed below.

## Customization

*   You can modify the `openai_chatbot_vanilla.py` file to:
    *   Change the GPT model being used (e.g., `gpt-3.5-turbo`, `gpt-4`).
    *   Adjust parameters like `temperature` and `max_tokens` to control the chatbot's behavior.
    *   Add more features to the Streamlit interface.

## Contributing

Contributions are welcome! Feel free to open issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.