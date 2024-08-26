import json
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchFieldDataType
from azure.core.credentials import AzureKeyCredential

# Replace these with your Azure details
search_service_name = "allergyaffiliates-ai-search"
search_api_key = "u8p0c3Sqn6e1HOtUDfEUD84UGpEzweNlKPqn8PlbvwAzSeDF440q"
index_name = "clinicdata"

# Create a client
index_client = SearchIndexClient(endpoint=f"https://{search_service_name}.search.windows.net",
                                 credential=AzureKeyCredential(search_api_key))

# Define the updated index schema
fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True, searchable=False),
    SimpleField(name="content", type=SearchFieldDataType.String, searchable=True, filterable=False, sortable=False, facetable=False)
]

index = SearchIndex(name=index_name, fields=fields)

# Delete the existing index if it exists
try:
    index_client.delete_index(index_name)
    print("Index deleted successfully")
except Exception as e:
    print(f"Index deletion failed or index does not exist: {e}")

# Ensure the index is deleted by attempting to fetch it
try:
    index_client.get_index(index_name)
    print(f"Index {index_name} still exists after deletion attempt")
except Exception as e:
    print(f"Index {index_name} confirmed deleted")

# Create the index
try:
    index_client.create_index(index)
    print("Index created successfully")
except Exception as e:
    print(f"Index creation failed: {e}")

# Initialize the SearchClient
search_client = SearchClient(endpoint=f"https://{search_service_name}.search.windows.net",
                             index_name=index_name,
                             credential=AzureKeyCredential(search_api_key))

# Load the JSON data
with open('corrected_cleaned_content.json', 'r') as f:
    data = json.load(f)

# Upload the data
try:
    result = search_client.upload_documents(documents=data)
    print(f"Upload of {len(result)} documents succeeded")
except Exception as e:
    print(f"Upload failed: {e}")

