import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
import openai

# Azure Cognitive Search configuration
search_endpoint = "https://allergyaffiliates-ai-search.search.windows.net"
search_index_name = "clinicdata"
search_api_key = "u8p0c3Sqn6e1HOtUDfEUD84UGpEzweNlKPqn8PlbvwAzSeDF440q"

# Azure OpenAI configuration
openai_endpoint = "https://allergyaffiliatesassistant.openai.azure.com/"
openai_api_key = "64f682f1ff464195a3457cd3c6cef8fe"
deployment_id = "AllergyAffiliates"

# Initialize the Azure Cognitive Search client
search_client = SearchClient(endpoint=search_endpoint,
                             index_name=search_index_name,
                             credential=AzureKeyCredential(search_api_key))

# Initialize the OpenAI API client
openai.api_type = "azure"
openai.api_base = openai_endpoint
openai.api_version = "2022-12-01"
openai.api_key = openai_api_key

def search_documents(query):
    results = search_client.search(query, query_type=QueryType.SIMPLE)
    return [result['content'] for result in results]

def truncate_context(context, max_tokens):
    words = context.split()
    truncated_context = ""
    token_count = 0
    for word in words:
        token_count += 1  # Rough approximation: 1 word = 1 token
        if token_count > max_tokens:
            break
        truncated_context += word + " "
    return truncated_context.strip()

def generate_response(documents, user_input):
    context = "\n".join(documents)
    max_context_tokens = 6000  # Adjust this to fit within the model's context length limit
    context = truncate_context(context, max_context_tokens)
    prompt = f"You are an AI assistant named Geet. Use the provided context to answer the following question accurately.\n\nContext:\n{context}\n\nQuestion: {user_input}\nAnswer:"

    response = openai.Completion.create(
        engine=deployment_id,
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        n=1,
        stop=None
    )
    
    return response.choices[0].text.strip()

def chat():
    while True:
        user_input = input("You: ")
        documents = search_documents(user_input)
        if documents:
            response = generate_response(documents, user_input)
            print(f"Geet: {response}")
        else:
            print("Geet: I'm sorry, I couldn't find any information on that topic.")

if __name__ == "__main__":
    chat()

