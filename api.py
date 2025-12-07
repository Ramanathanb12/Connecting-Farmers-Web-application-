# # bot_api.py
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os

# # Load environment variables from the .env file
# load_dotenv()

# # Get the API key from the environment variable
# api_key = os.getenv("API_KEY")

# # Ensure API key is loaded properly
# if not api_key:
#     raise ValueError("API_KEY not found in the environment variables!")

# # Now you can use the api_key in your code
# genai.configure(api_key=api_key)

# # Create the model configuration
# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 40,
#     "max_output_tokens": 8192,
#     "response_mime_type": "text/plain",
# }

# # Define the model with the configuration
# model = genai.GenerativeModel(
#     model_name="gemini-1.5-flash",
#     generation_config=generation_config,
#     system_instruction=(
#         "I am going to create a farmer and marketer chatbot. "
#         "Only you can respond to agriculture-related topics, "
#         "otherwise, if the topic is not related to agriculture, do not respond. "
#         "Additionally, provide weather details when asked and approximate market prices "
#         "for agricultural products in Tamil Nadu, India (not real-time data). "
#         "This bot is developed by Ram Developer."
#     ),
# )

# # Function to generate a response based on user input
# def generate_response(input_text):
#     response = model.generate_content([
#         f"input: {input_text}",
#         "output: ",
#     ])
#     return response.text


# # Start a loop to continuously prompt the user for input
# def chat():
#     print("Welcome to the Farmer and Marketer Chatbot!")
#     print("Type 'exit' to end the chat.")

#     while True:
#         # Get input from the user
#         user_input = input("Ask the chatbot: ")

#         # Check if the user wants to exit the loop
#         if user_input.lower() == 'exit':
#             print("Ending the chat. Goodbye!")
#             break

#         # Generate a response based on the user input
#         response_text = generate_response(user_input)

#         # Print the chatbot's response
#         print(f"Chatbot Response: {response_text}")


# # Run the chatbot
# if __name__ == "__main__":
#     chat()



import google.generativeai as genai

# Configure API key
genai.configure(api_key="AIzaSyClwCo8aIpV8gieeDQ5HsjiASODhGkxt-0")

# Generation settings
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are a chatbot to help users with farmer details and all marketing-related topics."
)

# Start the chat session
chat_session = model.start_chat()

# Chat loop
print("🤖 Bot is ready to chat! Type 'exit' to quit.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    response = chat_session.send_message(user_input)
    print(f"Bot: {response.text}\n")
