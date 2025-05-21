import streamlit as st
import wikipedia
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import re

load_dotenv()

# API key for accessing Groq Langchain service
groq_api_key = os.getenv('GROQ_API_KEY')

# --- Helper Functions ---

def fetch_wikipedia_summary(topic: str, lang_code: str) -> str | None:
    """
    Fetches the summary of a given topic from Wikipedia in the specified language.

    Args:
        topic (str): The topic to search for on Wikipedia.
        lang_code (str): The language code for Wikipedia (e.g., "en", "es").

    Returns:
        str | None: The Wikipedia summary string if found, otherwise None.
                     Displays Streamlit warnings/errors for disambiguation or page errors.
    """
    wiki_summary = None
    try:
        wikipedia.set_lang(lang_code)
        wiki_summary = wikipedia.summary(topic)
    except wikipedia.exceptions.DisambiguationError as e:
        st.warning(f"The topic '{topic}' is ambiguous on Wikipedia. Trying the first suggestion: '{e.options[0]}'. If this is not what you intended, please be more specific.")
        try:
            wiki_summary = wikipedia.summary(e.options[0])  # Try fetching the first suggestion
        except Exception as inner_e:
            st.error(f"Could not fetch details for suggestion '{e.options[0]}': {inner_e}")
            wiki_summary = None # Ensure summary is None if suggestion fails
    except wikipedia.exceptions.PageError:
        st.error(f"Could not find a Wikipedia page for '{topic}'. Generating blog post without Wikipedia context.")
        wiki_summary = None
    except Exception as e:  # Catch any other potential Wikipedia errors
        st.error(f"An unexpected error occurred while fetching from Wikipedia: {e}")
        wiki_summary = None
    return wiki_summary

def generate_prompt(
    topic: str, 
    wiki_summary: str | None, 
    use_wiki_summary_toggle: bool, 
    style_choice: str, 
    tone_choice: str, 
    audience_choice: str, 
    keywords_input: str
) -> str:
    """
    Constructs the detailed prompt string for the LLM based on user selections and Wikipedia summary.

    Args:
        topic (str): The main blog topic.
        wiki_summary (str | None): The fetched Wikipedia summary, or None.
        use_wiki_summary_toggle (bool): Whether the user wants to include the Wikipedia summary.
        style_choice (str): The desired blog post style/length (e.g., "default", "short", "detailed").
        tone_choice (str): The desired tone (e.g., "default", "formal", "humorous").
        audience_choice (str): The target audience (e.g., "general", "beginners", "experts").
        keywords_input (str): Comma-separated keywords, or an empty string.

    Returns:
        str: The fully formatted prompt string.
    """
    prompt_parts = []
    effective_wiki_summary = None # To track if wiki_summary was actually used for the reference part

    # Add Wikipedia summary if available and toggled on
    if wiki_summary and use_wiki_summary_toggle:
        prompt_parts.append(f"{wiki_summary}\n\n")
        effective_wiki_summary = wiki_summary

    # Base instruction based on style
    if style_choice == "short":
        prompt_parts.append(f"Create a SHORT blog post (1-2 paragraphs) with a Heading, Introduction, and Summary using the topic \"{topic}\"")
    elif style_choice == "detailed":
        prompt_parts.append(f"Create a DETAILED blog post (4-5 paragraphs) with a Heading, Introduction, multiple Context sections (around 3-4 paragraphs for context), and a Conclusion using the topic \"{topic}\"")
    else:  # Default style
        prompt_parts.append(f"Create a blog with the Heading, Introduction, context (around 3 paragraphs), and summary using the topic \"{topic}\"")

    # Add tone instruction
    if tone_choice != "default":
        prompt_parts.append(f" The tone of the blog post should be {tone_choice}.")

    # Add audience instruction
    if audience_choice != "general":
        if audience_choice == "beginners":
            prompt_parts.append(" The blog post should be written for beginners, explaining concepts clearly and avoiding jargon where possible.")
        elif audience_choice == "experts":
            prompt_parts.append(" The blog post should be written for an expert audience, assuming deep prior knowledge and technical understanding.")
        elif audience_choice == "students":
            prompt_parts.append(" The blog post should be suitable for students, being informative, engaging, and easy to understand.")
    
    # Add keyword instruction
    if keywords_input:
        prompt_parts.append(f" Please try to naturally incorporate the following keywords: {keywords_input}.")

    # Add reference instruction if Wikipedia was used
    if effective_wiki_summary:  # Check if wiki summary was actually prepended
        prompt_parts.append(" Take the provided Wikipedia summary (if any was prepended to these instructions) as reference for the content.")
    
    input_text = "".join(prompt_parts)
    # Ensure the prompt ends with a period if it doesn't already (and isn't empty).
    if input_text and not input_text.strip().endswith("."):
        input_text += "."
    return input_text

def get_blog_post(api_key: str, model_name: str, input_text: str) -> str | None:
    """
    Generates the blog post content using the Langchain Groq LLM.

    Args:
        api_key (str): The Groq API key.
        model_name (str): The name of the Groq model to use.
        input_text (str): The prompt to send to the LLM.

    Returns:
        str | None: The generated blog content string, or None if an error occurs.
    """
    try:
        # Initialize Groq Langchain chat object and conversation
        groq_chat = ChatGroq(
            groq_api_key=api_key, 
            model_name=model_name
        )
        conversation = ConversationChain(llm=groq_chat)
        response = conversation(input_text)
        return response['response']
    except Exception as e:
        st.error(f"Failed to generate blog post due to an LLM error: {e}")
        return None

# --- Main Application ---

def main():
    """
    Main function to run the Streamlit Blog Generation System.
    Sets up the UI, handles user input, and orchestrates the blog generation process.
    """
    st.title("📝 Blog Generation System")

    # --- Sidebar for Customization Options ---
    st.sidebar.title("⚙️ Customization")

    # Model Selection
    models = {"Mixtral 8x7B (Default)": "mixtral-8x7b-32768", "Llama2 70B": "llama2-70b-4096"}
    selected_model_name = st.sidebar.selectbox("Select Language Model", list(models.keys()), help="Choose the underlying language model for generation.")
    selected_model = models[selected_model_name]

    # Blog Post Style/Length
    styles = {"Default": "default", "Short (1-2 paragraphs)": "short", "Detailed (4-5 paragraphs)": "detailed"}
    selected_style_name = st.sidebar.selectbox("Select Blog Post Style/Length", list(styles.keys()), help="Define the desired length and structure of the blog post.")
    style_choice = styles[selected_style_name]
    
    # Wikipedia Language Selection
    languages = {"English": "en", "Spanish": "es", "French": "fr", "German": "de", "Japanese": "ja", "Chinese": "zh"}
    selected_lang_name = st.sidebar.selectbox("Select Wikipedia Language", list(languages.keys()), help="Language for Wikipedia summaries.")
    lang_code = languages[selected_lang_name]

    # Toggle Wikipedia Summary
    use_wiki_summary_toggle = st.sidebar.checkbox("Include Wikipedia Summary as Context", value=True, help="Use a Wikipedia summary as additional context for the blog post.")

    # Tone Selection
    tones = {"Default (Balanced)": "default", "Formal": "formal", "Informal": "informal", "Humorous": "humorous", "Professional": "professional", "Technical": "technical"}
    selected_tone_name = st.sidebar.selectbox("Select Blog Post Tone", list(tones.keys()), help="Set the overall tone of the generated blog post.")
    tone_choice = tones[selected_tone_name]

    # Target Audience
    audiences = {"General Public (Default)": "general", "Beginners": "beginners", "Experts": "experts", "Students": "students"}
    selected_audience_name = st.sidebar.selectbox("Select Target Audience", list(audiences.keys()), help="Specify the intended audience for the blog post.")
    audience_choice = audiences[selected_audience_name]

    # Keyword/SEO Focus
    keywords_input = st.sidebar.text_input("Optional Keywords (comma-separated)", help="Enter keywords to be naturally incorporated for SEO.").strip()

    # --- Main Area for Topic Input and Blog Display ---
    user_question = st.text_area("Enter Blog Topic Here:", help="What subject do you want the blog post to be about?")

    # Button to trigger blog post generation
    if st.button('🚀 Generate Blog Post'):
        if not user_question:
            st.warning("Please enter a blog topic to generate a post.")
        else:
            with st.spinner("🧠 Generating blog post, please wait... This may take a moment."):
                topic_for_generation = user_question # Keep the original user input for topic
                
                # 1. Fetch Wikipedia Summary (if toggled)
                actual_wiki_summary = None
                if use_wiki_summary_toggle:
                    actual_wiki_summary = fetch_wikipedia_summary(topic_for_generation, lang_code)
                
                # 2. Generate the Prompt
                prompt_text = generate_prompt(
                    topic=topic_for_generation,
                    wiki_summary=actual_wiki_summary,
                    use_wiki_summary_toggle=use_wiki_summary_toggle, # Pass the toggle state
                    style_choice=style_choice,
                    tone_choice=tone_choice,
                    audience_choice=audience_choice,
                    keywords_input=keywords_input
                )
                
                # 3. Get Blog Post from LLM
                if prompt_text: # Ensure prompt is not empty
                    blog_content = get_blog_post(groq_api_key, selected_model, prompt_text)
                    
                    if blog_content:
                        # Display the generated blog post
                        st.subheader("📄 Generated Blog Post")
                        st.markdown(blog_content)

                        # Add download button
                        sanitized_topic = re.sub(r'[^a-zA-Z0-9_]+', '', topic_for_generation.lower().replace(' ', '_'))
                        if not sanitized_topic:  # Handle empty topic after sanitization
                            sanitized_topic = "untitled_blog"
                        download_filename = f"{sanitized_topic}_blog.md"
                        
                        st.download_button(
                            label="📥 Download Blog Post",
                            data=blog_content,
                            file_name=download_filename,
                            mime="text/markdown"
                        )
                else:
                    st.error("Failed to generate a valid prompt for the blog post.")

if __name__ == "__main__":
    main()
