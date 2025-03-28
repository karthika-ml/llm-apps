from quart import Quart, render_template, request, jsonify, session
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureOpenAI
from langchain_core.output_parsers import StrOutputParser
import openai

app = Quart(__name__)
app.secret_key = "your_secret_key"  # Replace with a strong secret key

openai.api_type = "azure"
openai.model = "gpt-35-turbo"
openai.api_base = "https://sqlalmeda2.openai.azure.com/"
openai.api_version = "2023-05-15"
openai.api_key = "60436d3dcae2441bb9bd099bebcfa9e7"

def connectDatabase(username, port, host, password, database):
    connection_string = f'mssql+pyodbc://{username}:{password}@{host}/{database}?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no'
    session['db'] = SQLDatabase.from_uri(connection_string)

def runQuery(query):
    return session['db'].run(query) if 'db' in session else "Please connect to database"

def getDatabaseSchema():
    return session['db'].get_usable_table_names() if 'db' in session else "Please connect to database"

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

@app.route("/", methods=["GET", "POST"])
async def index():
    if request.method == "POST":
        question = await request.form.get('question')
        if 'chat' not in session:
            session['chat'] = []

        if question:
            if 'db' not in session:
                return jsonify({"error": "Please connect to the database first."})
            else:
                session['chat'].append({"role": "user", "content": question})
                query = getQueryFromLLM(question)
                result = runQuery(query)
                response = getResponseForQueryResult(question, query, result)
                session['chat'].append({"role": "assistant", "content": response})
                return jsonify(session['chat'])
    return await render_template("index.html")

@app.route("/connect", methods=["POST"])
async def connect():
    username = await request.form.get('username')
    port = await request.form.get('port')
    host = await request.form.get('host')
    password = await request.form.get('password')
    database = await request.form.get('database')

    connectDatabase(username, port, host, password, database)
    return jsonify({"message": "Database connected"})

if __name__ == "__main__":
    app.run(debug=True)