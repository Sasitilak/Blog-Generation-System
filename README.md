# Enhanced Blog Generation System

This application is an advanced Blog Generation System built with Streamlit and powered by Langchain with Groq LLMs. It allows users to generate highly customizable blog posts by providing a topic and selecting various generation parameters. The system can optionally integrate with Wikipedia to fetch contextual information, enhancing the depth and relevance of the generated content.

## Features

This Blog Generation System boasts a comprehensive set of features designed to give users maximum control over the content creation process:

*   **Topic-Based Generation:** Simply input a blog topic to get started.
*   **Intelligent Wikipedia Integration:**
    *   Automatically fetches relevant summaries from Wikipedia to provide context.
    *   **Language Selection:** Choose from multiple languages (English, Spanish, French, German, Japanese, Chinese) for Wikipedia summaries.
    *   **Toggle Summary Inclusion:** Decide whether to include the fetched Wikipedia summary in the context for the LLM.
*   **Customizable Blog Structure:**
    *   **Length/Style Selection:** Choose from "Default", "Short (1-2 paragraphs)", or "Detailed (4-5 paragraphs)" to control the output length and structure.
*   **Flexible LLM Choice:**
    *   **Model Selection:** Select between different powerful language models like "Mixtral 8x7B (Default)" and "Llama2 70B".
*   **Advanced Content Customization:**
    *   **Tone Selection:** Define the tone of the blog post (e.g., "Formal", "Informal", "Humorous", "Professional", "Technical").
    *   **Target Audience:** Specify the intended audience (e.g., "General Public", "Beginners", "Experts", "Students") to tailor the language and complexity.
    *   **Keyword/SEO Focus:** Input comma-separated keywords to be naturally incorporated into the blog post for SEO purposes.
*   **Output and Usability:**
    *   **Markdown Formatting:** Generated blog posts are displayed in Markdown for better readability.
    *   **Download Option:** Easily download the generated blog post as a `.md` (Markdown) file.
    *   **Loading Spinners & Error Handling:** User-friendly notifications for background processes and potential issues.

## How to Run

1.  **Set up Environment Variables:** (See section below)
2.  **Install Dependencies:** (See section below)
3.  **Run the Application:** Open your terminal, navigate to the project directory, and run:
    ```bash
    streamlit run BlogAPP.py
    ```
    This will open the application in your web browser.

## Using the Application

The application interface is designed for ease of use:

**Main Area:**

*   **Enter Blog Topic Here:** A text area where you input the desired topic for your blog post.
*   **🚀 Generate Blog Post Button:** Click this after setting your topic and desired customizations.
*   **📄 Generated Blog Post Area:** Once generation is complete, the blog post will be displayed here in Markdown format.
*   **📥 Download Blog Post Button:** Appears below the generated content, allowing you to download the blog as a `.md` file.

**Sidebar (⚙️ Customization):**

*   **Select Language Model:** Dropdown to choose the LLM (e.g., Mixtral 8x7B, Llama2 70B).
*   **Select Blog Post Style/Length:** Dropdown to define the structure and length (Default, Short, Detailed).
*   **Select Wikipedia Language:** Dropdown to choose the language for Wikipedia summaries.
*   **Include Wikipedia Summary as Context:** Checkbox (selected by default) to decide if the fetched Wikipedia summary should be used as context for the LLM.
*   **Select Blog Post Tone:** Dropdown to set the desired tone for the blog post.
*   **Select Target Audience:** Dropdown to specify the intended audience.
*   **Optional Keywords (comma-separated):** Text input field to provide keywords for SEO focus.

## Environment Variables Setup

To run this application, you need to configure your Groq API key.

1.  **Create a `.env` file:** In the root directory of the project, create a file named `.env`.
2.  **Set the API Key:** Open the `.env` file and add the following line, replacing `'your_actual_api_key_here'` with your actual Groq API key:
    ```
    GROQ_API_KEY='your_actual_api_key_here'
    ```
3.  The application uses `python-dotenv` to load this key.

## Dependencies

This project relies on several Python libraries. You should install them, preferably in a virtual environment.

It's recommended to create a `requirements.txt` file with the following content and install using `pip install -r requirements.txt`:

```
streamlit
wikipedia
langchain-groq
python-dotenv
langchain
```

Ensure these libraries are installed in your Python environment before running the application.

## Screenshots

*(Note: The screenshots in this README may be outdated. The application UI has been significantly updated with new sidebar controls for enhanced customization as described in the features list.)*

(The old image links can be kept here if they still show the basic input/output, but ideally, they should be replaced with new ones reflecting the current UI.)

Old Input/Output example:
![image](https://github.com/Sasitilak/Blog-Generation-System/assets/116880437/4f27562d-f869-4b24-80da-57243f307b15)
![image](https://github.com/Sasitilak/Blog-Generation-System/assets/116880437/61b17cff-0331-4fff-a04e-eb380f45eb5b)

---

This updated README should provide a comprehensive guide for users of the enhanced Blog Generation System.
