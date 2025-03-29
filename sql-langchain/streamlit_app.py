import streamlit as st
import dotenv
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import openai
load_dotenv()

# Set OpenAI API configuration from environment variables
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set model separately
model = os.getenv("OPENAI_MODEL", "gpt-35-turbo")

def connectDatabase(username, port, host, password, database):
    # global db
    connection_string = 'mssql+pyodbc://xxxxxxx:Mar%402024@xxxxxxxx.database.windows.net/xxxxx?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no'
    st.session_state.db = SQLDatabase.from_uri(connection_string)

def runQuery(query):
    return st.session_state.db.run(query) if st.session_state.db else "Please connect to database"

def getDatabaseSchema():
    return st.session_state.db.get_usable_table_names() if st.session_state.db else "Please connect to database"


connectDatabase(username='xxxxxx',port='',host='xxxxxx.database.windows.net',password='Mar@2024',database='xxxxxx')

llm = AzureOpenAI(
    deployment_name="chatbot_1",  # Replace with your model deployment
    model_name="gpt-35-turbo",
    api_key=openai.api_key,
    azure_endpoint=openai.api_base,
    api_version=openai.api_version,
    temperature=0
)

def getQueryFromLLM(question):
    template = """Below is the schema of a MySQL database. Read the schema carefully about the table and column names, taking care of case sensitivity.

    {schema}

    I. Database Context:
    The table name which is of interest is named Stage_Facesheet. This is the only Table you will use from the Database.
    It contains various patient-related columns, including:
    Member details (Last Name, First Name, DOB, Gender, ID)
    Guarantor details (Last Name, First Name)
    Other coverage information
    Admission details (Type, Source, Level of Urgency)
    Medical details (Primary Diagnosis, Requesting Physician, Servicing Facility)
    Summary content and extracted date/time information \n\n
    II. Specific Information:\n

    The Member_Gender column can have either "Male" or "Female" values.
    Member_First_Name and Member_Last_Name are strings representing patients' names.
    Guarantor_Last_Name and Guarantor_First_Name are strings representing guardians' names.
    Other_Coverage contains strings describing patients' insurance plans.
    Level_of_Urgency is a string. If no value exists, return "relevant information not found."
    Admission_Type is a string containing numbers or text like "Inpatient," "Urgent," or "Emergency."
    Admission_Source is a string with values like "Self Referred (Home)," "Home/Self Referral," or "N/A."
    Source_File is the reference file name for the information.
    Primary_Diagnosis contains text sentences describing the doctor's primary diagnosis.
    Requesting_Provider_Name is a string with the requesting doctor's name.
    Requesting_Provider_NPI and Requesting_Provider_Tax_Id are strings with numerical values.
    Date_Time_of_Request is formatted as MM/DD/YYYY HH:MM:SS.
    Servicing_Facility is the hospital or clinic name.
    Summary_content is a short paragraph summarizing the original source file. Use this for questions without a direct answer in other columns.
    Extracted_Date is a date object indicating when the database was populated with the patient's details.
    Extracted_Time is a time object indicating when the database was populated with the patient's details.

    Please only provide the SQL query response and STOP generating.

    For example:
    Question: Show all records where the 'Admission_Type' is 'Emergency'.
    SQL query: SELECT * FROM Stage_Facesheet WHERE Admission_Type = 'Emergency'

    Question: {question}
    SQL query:
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm.bind(stop=["Question"]) | StrOutputParser()

    response = chain.invoke({
        "question": question,
        "schema": getDatabaseSchema()
    })

    return response

def getResponseForQueryResult(question, query, result):
    template2 = """Below is the schema of MYSQL database, read the schema carefully about the table and column names of each table.
    Also look into the conversation if available
    Finally write a response in natural language by looking into the conversation and result.

{schema}. 
    Here are some examples for you:
    question: how many patient records do we have in database
    SQL query: SELECT COUNT(*) FROM Stage_Facesheet
    Result : [(34,)]
    Response: There are 34 albums in the database.

    question: Show all records where the 'Admission_Type' is 'Emergency'
    SQL query: SELECT * FROM Stage_Facesheet WHERE Admission_Type = 'Emergency'
    Result : [(1,)]
    Response: There was 1 emergency patient.

    Your turn to write response in natural language from the given result :
    Question: {question}
    SQL Query: {query}
    Result: {result}
    Response:
    """

    prompt2 = ChatPromptTemplate.from_template(template2)
    chain2 = prompt2| llm.bind(stop=["Question"]) 
    
    response = chain2.invoke({
        "question": question,
        "schema": getDatabaseSchema(),
        "query": query,
        "result": result
    })

    return response

# Streamlit configuration
st.set_page_config(
    page_icon="🤖",
    page_title="Chat with SQL DB",
    layout="centered"
)

question = st.chat_input('Chat with your SQL database')

if "chat" not in st.session_state:
    st.session_state.chat = []

if question:
    if "db" not in st.session_state:
        st.error('Please connect to the database first.')
    else:
        st.session_state.chat.append({
            "role": "user",
            "content": question
        })

        query = getQueryFromLLM(question)
        result = runQuery(query)
        response = getResponseForQueryResult(question, query, result)
        st.session_state.chat.append({
            "role": "assistant",
            "content": response
        })

for chat in st.session_state.chat:
    st.chat_message(chat['role']).markdown(chat['content'])

# Sidebar for database connection
with st.sidebar:
    st.title('Connect to database')
    st.text_input(label="Host", key="host", value="xxxxxxxx.database.windows.net")
    st.text_input(label="Port", key="port", value=" ")
    st.text_input(label="Username", key="username", value="xxxxxxx")
    st.text_input(label="Password", key="password", value="yyyyyy", type="password")
    st.text_input(label="Database", key="database", value="xxxxxx")
    connectBtn = st.button("Connect")

if connectBtn:
    connectDatabase(
        username=st.session_state.username,
        port=st.session_state.port,
        host=st.session_state.host,
        password=st.session_state.password,
        database=st.session_state.database,
    )
    st.success("Database connected")


