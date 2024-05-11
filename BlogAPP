import streamlit as st
import wikipedia
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
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
    conversational_memory_length = 10  # Length of conversational memory

    # Initialize conversational memory
    memory = ConversationBufferWindowMemory(k=conversational_memory_length)

    # Text area for user to input blog topic
    user_question = st.text_area("Give Blog Topic")

    # session state variable to store chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    else:
        # Load chat history into memory
        for message in st.session_state.chat_history:
            memory.save_context({'input': message['human']}, {'output': message['AI']})

    # Initialize Groq Langchain chat object and conversation
    groq_chat = ChatGroq(
        groq_api_key=groq_api_key, 
        model_name=model
    )

    conversation = ConversationChain(
        llm=groq_chat,
        memory=memory
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
                input_with_reference = f"Create a blog with the Heading, Introduction, context(3 paragraphs), summary using the topic \"{topic}\"."
                response = conversation(input_with_reference)
                message = {'human': user_question, 'AI': response['response']}
                st.session_state.chat_history.append(message)
                st.write("Blog")
                st.write(response['response'])
                return

            # Prepend the Wikipedia summary to the user's input
            input_with_reference = f"{wiki_summary}\n\nCreate a blog with the titles title, intro, context(3 paragraphs), summary using the topic and take the above information as refernece \"{topic}\"."
            
            # Generate blog post using conversation chain
            response = conversation(input_with_reference)
            message = {'human': user_question, 'AI': response['response']}
            
            # Append user input and AI response to chat history
            st.session_state.chat_history.append(message)
            st.write("Blog")
            st.write(response['response'])

if __name__ == "__main__":
    main()
