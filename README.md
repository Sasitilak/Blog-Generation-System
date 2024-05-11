# Blog-Generation-System

This code implements a straightforward Blog Generation System using Streamlit and Langchain, accessing the Groq Langchain service via an API key. Users input a topic via a text area, prompting the system to gather additional information from Wikipedia to enhance blog post generation. The Langchain service processes user input, including the topic and accompanying text, using a pre-trained language model ('mixtral-8x7b-32768'). The model generates natural language responses based on the input provided, allowing for the creation of coherent blog content. The resulting blog post is then displayed on the interface, enabling quick and easy blog content generation based on user-provided topics.


**User Input:**

After the user enters a blog topic into the text area and clicks the "Generate Blog Post" button, the application proceeds to process the input.

# Wikipedia Interaction:

If the user-provided topic exists on Wikipedia, the application fetches relevant information from the Wikipedia page using the Wikipedia API.
The Wikipedia summary of the topic is obtained to provide additional context for generating the blog post.

# Langchain Interaction:

The application interacts with the Langchain service to generate the blog post content.
The Langchain service is accessed using the provided Groq API key, which authorizes the application to utilize the language model for text generation.

# Text Generation with Mixtral Model:

The Langchain service utilizes the specified language model ('mixtral-8x7b-32768') to process the user input and generate natural language responses.
The model, trained on vast amounts of text data, is capable of understanding and generating human-like text based on the input provided.

# Combining Wikipedia Data and User Input:

If the Wikipedia summary is available, it is combined with the user's input to provide additional context and depth to the blog post generation process.
The Langchain model incorporates this combined information to produce a coherent and informative blog post response.

# Displaying the Generated Blog Post:

The generated blog post content is displayed on the application interface, allowing the user to view the result of the generation process.
The user can then review the generated content and make any necessary adjustments or edits as desired.

here is the Blog Generation System 

![image](https://github.com/Sasitilak/Blog-Generation-System/assets/116880437/4f27562d-f869-4b24-80da-57243f307b15)
After entering the topic we like and hitting Generate Blog Button we can get a detailed Blog with sections:

1.Heading
2.Introduction
3.Context
4.Summary
![image](https://github.com/Sasitilak/Blog-Generation-System/assets/116880437/61b17cff-0331-4fff-a04e-eb380f45eb5b)

