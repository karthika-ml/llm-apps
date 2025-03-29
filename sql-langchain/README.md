# 🤖 Chat with SQL Database using Streamlit, Azure OpenAI, and LangChain

This app lets you query your SQL Database using natural language. It leverages **Azure OpenAI's GPT-3.5 Turbo**, **LangChain**, and a simple interactive UI built with **Streamlit** to generate SQL queries, execute them, and return conversational answers.

---

## 🚀 Features

- ✅ **Natural Language Queries**: Ask questions without writing SQL.
- ✅ **Interactive UI**: Chat-like interface powered by Streamlit.
- ✅ **Azure OpenAI Integration**: Accurate SQL query and response generation with GPT-3.5 Turbo.
- ✅ **Secure Database Connections**: Connect securely to your SQL databases.

---

## 📁 Project Structure

. ├── app.py ├── requirements.txt └── .env (Not included in GitHub for security)

yaml
Copy
Edit

---

## 📦 Installation & Setup

### Step 1: Clone this Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Step 2: Create Python Environment
Create and activate a virtual environment:

bash
Copy
Edit
python -m venv venv
Activate it:

Windows:

bash
Copy
Edit
venv\Scripts\activate
macOS/Linux:

bash
Copy
Edit
source venv/bin/activate
Step 3: Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
🔑 Configure Environment Variables
Create a .env file at the root of the project containing your Azure OpenAI credentials:

env
Copy
Edit
OPENAI_API_TYPE=azure
OPENAI_API_BASE=https://your-azure-openai-endpoint.azure.com/
OPENAI_API_VERSION=2023-05-15
OPENAI_API_KEY=your-azure-openai-api-key
OPENAI_MODEL=gpt-35-turbo
⚠️ Important:

Add .env to your .gitignore file.

Do not share .env publicly or commit it to GitHub.

▶️ Run the Application
Start the Streamlit application locally:

bash
Copy
Edit
streamlit run app.py
Your browser will open at http://localhost:8501.

🛠️ Database Connection
In the Streamlit sidebar, enter your SQL Database credentials:

Field	Example value
Host	xxxxxxxxxx.database.windows.net
Port	(Leave empty or default)
Username	intelli
Password	YourSecurePassword
Database	intelli_db
Click "Connect" to establish your connection.

