from pathlib import Path
import requests
import google.generativeai as genai
import json

genai.configure(api_key="AIzaSyCnJVnmcUm4jHHQhCw_gTTp25UtzGDGCUc")

# Set up the model
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 300,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Download the image from the URL
image_url = "https://pipedream-catcher-bodies.s3.amazonaws.com/0a53b505-fc39-49c8-aecf-7244654355a3?AWSAccessKeyId=ASIA5F5AGIEAQKUXDH7I&Expires=1709578382&Signature=zZysC7SRKXkDihAjoZWicEC4n0k%3D&x-amz-security-token=FwoGZXIvYXdzEJP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDGTSeCsnZnhxiwflJyKNBJWTMn7P9QFTHCTvjQ1RlN0sTnUhkKP5kgFEo6rgExIIBBEQag87p258VdWQOs4%2FcPKB8QgGT1FjR%2BXm2mCy4KJNAPomFSWQsjRbTSpSGIJ2HunOwZXGQTAd8RdWR8EZzk7wHcD14jqelXeFKKRU0V8eNf04WgR4f63hTnPUpGNSIScHQWZEI9A16SVmi3Sg4ax%2B2Na30FR6gb6%2FwAtQUJ8t8UkmMAEYNjzPNuRPMKsjIMTzUF4lZHZmIXbnLSs6zBmP5%2FxI%2Fww4PKwE3IB8oR0Ca8L9%2BdncLemf1LrkyRoRYCcktdBMTiwqq0sJEg6uPqtrF2AejCO94Wgs3UhjwUT%2F%2BpZzH8pvNNWb9WW4Uo%2FMF8dTWXo2D3G72pFCmuNAa6oqfer%2FhH%2BbQFm2Hyt7eCwO2n%2Bgt%2F1ocR3IsJzSCSIQoj1zNZbpVakIIQZcsO6t8%2BAY8Q1wxFZ%2B5jueYGMd%2FSa5yPG2oY%2FUX0AFr%2BptUAIJ1%2Bn4XODh6a1ZRePSRQe9zQjPfWTHZVUrVuRum7Kgwi6EaIwG6KUchD7pvL%2FFgAJOHeJeEqM8a83Q5SnBXWpLWPURy99pSkzGPemNP3wlwBkTowN%2FqEF9L9o1pcBNhxLKHphqmvZudR93OPJKMms19SJTtY%2BFHmUPVu5PaFdb4TgRgwBNgmtEEU5IqTus4ykEbRF0eW0ldn4E9CmiwSiLmJivBjIqxnbS8Vp7dXa8rRd091nhj%2F4l4%2BMp9toArnP0XxFrUhS6ClYFqwSKhk6h"
image_content = requests.get(image_url).content

image_parts = [
    {
        "mime_type": "image/jpeg",
        "data": image_content
    },
]

prompt_parts = [
    image_parts[0],
    "Write the output only in JSON format. ProblemDescription, ProblemType(Leakage, PotHoles,Contamination)",
]

response = model.generate_content(prompt_parts)
print(response.text)

# Save the response text to a JSON file
with open('res.json', 'w') as json_file:
    json.dump(response.text, json_file)
