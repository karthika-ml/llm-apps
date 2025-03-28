<<<<<<< HEAD
# Blog Writer Agent using Crew AI Framework

This project leverages the Crew AI framework to create a blog writer agent. It automates the process of generating blog content based on specified topics.

## Prerequisites

Before running the application, ensure you have the following installed:

* **Python 3.7+**
* **pip** (Python package installer)

## Setup

1.  **Create a new virtual environment (recommended):**

    ```bash
    python -m venv venv
    ```

    * **On Windows:**

        ```bash
        venv\Scripts\activate
        ```

    * **On macOS and Linux:**

        ```bash
        source venv/bin/activate
        ```

2.  **Install required packages:**

    ```bash
    pip install -r requirements.txt
    ```

    * Make sure you have a `requirements.txt` file in your project directory containing the necessary dependencies, including `crewAI`.

3.  **Install Streamlit:**

    ```bash
    pip install streamlit
    ```

4.  **Configure OpenAI API Key:**

    * Obtain your OpenAI API key from the OpenAI website.
    * Set the API key as an environment variable named `OPENAI_API_KEY`.

        * **On macOS and Linux:**

            ```bash
            export OPENAI_API_KEY="your_api_key_here"
            ```

        * **On Windows:**

            ```bash
            set OPENAI_API_KEY=your_api_key_here
            ```

        * Alternatively, you can configure your API key through the python code directly. However, using environment variables is the most secure method.

## Running the Application

To run the Streamlit application, execute the following command:

```bash
streamlit run app.py
=======
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
>>>>>>> c116f1361bd275a2599bf7e44140fabe9418cabf
