**Conversational AI for Health and Fitness**

**Overview**
This application is designed to help users obtain tailored advice on health and fitness. It utilizes a conversational AI model that can provide information based on predefined prompts regarding health concerns and fitness routines.

**Features**
Health and Fitness Guidance: Get reliable information on various health issues and fitness routines.
Interactive Queries: Users can ask specific questions, and the AI will respond based on the most relevant information stored in the system.
How to Use
Make a Request: To get information from the AI, you need to send a request in JSON format to the API endpoint.

**Sample Request**:
 Here's an example of the JSON payload you can send to the application:

**json - Copy code**
{
  "query_text": "fitness",
  "version": 2,
  "question": "Give me proper exercise routine I need to follow"
}

query_text: A keyword related to your inquiry (e.g., "fitness").
version: An integer representing the version of the prompt (e.g., 1 for health concerns, 2 for fitness).
question: Your specific question regarding health or fitness.
Send the Request: You can send the request using tools like Postman or directly through your browser if you have an API client.

Receive the Response: The AI will respond with a generated exercise routine or health advice based on your question.

Example
Request
If you send the following JSON payload:

json
Copy code
{
  "query_text": "fitness",
  "version": 2,
  "question": "Give me proper exercise routine I need to follow"
}
Response
The application will generate a response that provides a structured exercise routine tailored to your fitness goals.

**How It Works**
Backend Logic: The application uses a combination of FastAPI for handling requests, ChromaDB for storing health and fitness prompts, and Ollama for generating responses based on user questions.

Document Storage: The AI is preloaded with specific prompts related to health and fitness, ensuring that responses are relevant and informative.

**Getting Started**
Prerequisites
Python 3.7 or higher
Basic understanding of API interactions (using tools like Postman)
Installation
Clone this repository to your local machine.

Install the required packages using the following command:

bash
Copy code
pip install -r requirements.txt
Run the FastAPI server:

bash
Copy code
uvicorn main:app --reload
(Assuming your main Python file is named main.py)

**Accessing the API**
Once the server is running, you can access the API documentation by navigating to http://localhost:8000/docs in your web browser. This interface allows you to test the API directly.

**Conclusion**
This application is a powerful tool for anyone seeking health and fitness advice. By simply sending a question, you can leverage the capabilities of AI to get personalized recommendations. Enjoy exploring your health journey!