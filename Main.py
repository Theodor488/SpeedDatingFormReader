import os
import asyncio
from os import listdir
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Configuration
endpoint = "https://speeddatingformreader.cognitiveservices.azure.com/"
api_key = os.getenv("AZURE_API_KEY")  # Access the API key from environment variables
form_path = "C:/Users/theod/Pictures/Matches"  # Path to form images

# Initialize the client
client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

from FormInfoExtractor import FormInfoExtractor
infoExractor = FormInfoExtractor()

async def process_image(image_path, client, info_extractor):
    result = await info_extractor.analyze_layout(image_path, client)
    return result

# Main script
async def main():
    results_dict = {}
    info_extractor = FormInfoExtractor()
    tasks = []

    for image in os.listdir(form_path):
        if (image.endswith(".jpg")):
            image_path = os.path.join(form_path, image)
            tasks.append(process_image(image_path, client, info_extractor))
    
    results = await asyncio.gather(*tasks)

    for result in results:
        # get name
        name = infoExractor.extractName(result)
        # Get results for each name
        if name:
            infoExractor.GetResultsForName(result, name, results_dict)
        
    matches_dict = {}
    
    # Calculate matches for each person
    for name in results_dict:
        for match_person in results_dict:
            infoExractor.CalculateMatches(results_dict, name, matches_dict, match_person)
    
    print(matches_dict)

        
if __name__ == "__main__":
    asyncio.run(main())
