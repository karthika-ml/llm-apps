import os
import streamlit as st
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from utils import get_openai_api_key
from utils import StreamToExpander
import sys
import re

load_dotenv()
# Assuming 'get_openai_api_key' is defined elsewhere or replace with your method to get the API key
def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY")

# Set the API key and model environment variable safely
openai_api_key = get_openai_api_key()

# Define agents with specific roles and goals
planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article about the topic: {topic}."
              "You collect information that helps the audience learn something "
              "and make informed decisions. Your work is the basis for "
              "the Content Writer to write an article on this topic.",
    allow_delegation=False,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate opinion piece about the topic: {topic}",
    backstory="You're working on writing a new opinion piece about the topic: {topic}. "
              "You base your writing on the work of the Content Planner, who provides an outline "
              "and relevant context about the topic.",
    allow_delegation=False,
    verbose=True
)

editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with the writing style of the organization.",
    backstory="You are an editor who receives a blog post from the Content Writer. "
              "Your goal is to review the blog post to ensure that it follows journalistic best practices,"
              "provides balanced viewpoints when providing opinions or assertions, "
              "and also avoids major controversial topics or opinions when possible.",
    allow_delegation=False,
    verbose=True
)

# Define tasks associated with each agent
plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
            "and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering "
            "their interests and pain points.\n"
        "3. Develop a detailed content outline including "
            "an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output="A comprehensive content plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources.",
    agent=planner,
)

write = Task(
    description=(
        "1. Use the content plan to craft a compelling "
            "blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
		"3. Sections/Subtitles are properly named "
            "in an engaging manner.\n"
        "4. Ensure the post is structured with an "
            "engaging introduction, insightful body, "
            "and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and "
            "alignment with the brand's voice.\n"
    ),
    expected_output="A well-written blog post "
        "in markdown format, ready for publication, "
        "each section should have 2 or 3 paragraphs.",
    agent=writer,
)

edit = Task(
    description=("Proofread the given blog post for "
                 "grammatical errors and "
                 "alignment with the brand's voice."),
    expected_output="A well-written blog post in markdown format, "
                    "ready for publication, "
                    "each section should have 2 or 3 paragraphs.",
    agent=editor
)

# Initialize your Crew
crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=2
)

# Define the Streamlit user interface
st.title('AI Content Creation Assistant')
topic = st.text_input("Enter the topic:")

if st.button("Generate Article"):
    with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
    # Execute the crew kickoff with the given topic
        with st.container(height=500, border=False):
            sys.stdout = StreamToExpander(st)
            result = crew.kickoff(inputs={"topic": topic})
            # trip_crew = TripCrew(location, cities, date_range, interests)
            # result = trip_crew.run()
        status.update(label="✅ Ready !",
                      state="complete", expanded=False)

    st.subheader("Here is Topic", anchor=False, divider="rainbow")
    st.markdown(result)
