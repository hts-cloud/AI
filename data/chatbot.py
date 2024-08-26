import json
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import openai
import os
import tiktoken  # This is a tokenizer package that helps count tokens

# Replace these with your Azure and OpenAI details
search_service_name = "allergyaffiliates-ai-search"
search_api_key = "u8p0c3Sqn6e1HOtUDfEUD84UGpEzweNlKPqn8PlbvwAzSeDF440q"
index_name = "clinicdata"
openai_api_key = "64f682f1ff464195a3457cd3c6cef8fe"
openai_endpoint = "https://allergyaffiliatesassistant.openai.azure.com/"
openai_deployment_name = "AllergyAffiliates"  # Use this deployment name

# Initialize the SearchClient
search_client = SearchClient(endpoint=f"https://{search_service_name}.search.windows.net",
                             index_name=index_name,
                             credential=AzureKeyCredential(search_api_key))

# Initialize OpenAI for Azure
openai.api_type = "azure"
openai.api_base = openai_endpoint
openai.api_version = "2022-12-01"
openai.api_key = openai_api_key

def search_query(query):
    results = search_client.search(search_text=query, top=5)  # Limiting to top 5 results
    documents = [result['content'] for result in results if 'content' in result]
    return documents

def truncate_context(context, max_tokens):
    encoder = tiktoken.get_encoding("gpt2")  # Use the appropriate tokenizer for your model
    tokens = encoder.encode(context)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    return encoder.decode(tokens)

def generate_response(documents, query):
    max_context_tokens = 8192 - 150  # maximum context length minus buffer for response tokens
    context = "\n".join(documents)
    
    # Truncate context to fit within the token limit
    context = truncate_context(context, max_context_tokens)
        
    prompt = f"You are an AI assistant named Geet. Use the provided context to answer the following question accurately.\n\nContext: {context}\n\nQuestion: {query}\n\nAnswer:"
    response = openai.Completion.create(
        engine=openai_deployment_name,
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def chat():
    print("Geet: Hello! How can I assist you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Geet: Goodbye!")
            break
        
        # Perform search
        documents = search_query(user_input)
        
        # Generate response
        if documents:
            response = generate_response(documents, user_input)
        else:
            response = "I'm sorry, I couldn't find any information on that topic."

        print(f"Geet: {response}")

if __name__ == "__main__":
    chat()

