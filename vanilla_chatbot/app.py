from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

api_key = os.environ.get('OPENAI_API_KEY')
gpt_model = os.environ.get('OPENAI_MODEL')

def simple_llm(question):
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model = gpt_model,
            messages = [
                {"role": "system", "content":"You are a helpful and informative AI assistant."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content.strip()
    
    except OpenAI.error.OpenAIError as e:
            print(f"Error asking GPT-4: {e}")
            return None

if __name__ == '__main__':
      st.write("Ask GPT-4 a question")
      question = st.text_input("question")
      if question:
        answer = simple_llm(question)
        st.write(answer)
