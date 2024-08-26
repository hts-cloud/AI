import json

# Load the corrected data
with open('./corrected_cleaned_content.json', 'r') as file:
    corrected_data = json.load(file)

# Print the first few entries to verify the data
print(corrected_data[:5])

def chatbot_response(context, question, data):
    # Find the matching context in the data
    relevant_content = ""
    for entry in data:
        if context in entry['content']:
            relevant_content = entry['content']
            break
    
    # Simulate a response based on the relevant content
    if "doctor" in question.lower():
        if "our doctors" in relevant_content:
            return "Dr. Geetika Sabharwal"
        else:
            return "The name of the doctor is not provided in the context."
    # Add more conditions based on expected questions
    elif "location" in question.lower():
        return "Bradenton, Florida"
    # Handle other types of questions
    else:
        return "I am sorry, I don't understand what you are asking. Could you please rephrase or provide more context?"

# Test the chatbot response
context = "our doctors"
question = "What is the doctor's name?"
response = chatbot_response(context, question, corrected_data)
print(response)

