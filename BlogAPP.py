import streamlit as st
import wikipedia
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os 

load_dotenv()

# API key for accessing Groq Langchain service
groq_api_key = 'GROQ_API_KEY'

def main():
    st.title("Blog Generation System")

    # Add customization options to the sidebar
    model = 'mixtral-8x7b-32768'  # Model for language generation

    # Text area for user to input blog topic
    user_question = st.text_area("Give Blog Topic")

    # Initialize Groq Langchain chat object and conversation
    groq_chat = ChatGroq(
        groq_api_key=groq_api_key, 
        model_name=model
    )

    conversation = ConversationChain(
        llm=groq_chat
    )

    # Button to trigger blog post generation
    if st.button('Generate Blog Post'):
        if user_question:
            # Fetch data from Wikipedia based on the topic
            topic = user_question
            try:
                wikipedia.set_lang("en")  # Set language to English
                wiki_summary = wikipedia.summary(topic)
            except wikipedia.exceptions.DisambiguationError as e:
                # If there are multiple possible pages, select the first one
                wiki_summary = wikipedia.summary(e.options[0])
            except wikipedia.exceptions.PageError:
                # If Wikipedia page not found, generate blog post directly using the topic
                input_without_reference = f"Create a blog with the Heading, Introduction, context(3 paragraphs), summary using the topic \"{topic}\"."
                response = conversation(input_without_reference)
                st.write("Blog")
                st.write(response['response'])
                return

            # Prepend the Wikipedia summary to the user's input
            input_with_reference = f"{wiki_summary}\n\nCreate a blog with the titles title, intro, context(3 paragraphs), summary using the topic and take the above information as refernece \"{topic}\"."
            
            # Generate blog post using conversation chain
            response = conversation(input_with_reference)
            
            # Display the generated blog post
            st.write("Blog")
            st.write(response['response'])

if __name__ == "__main__":
    main()
