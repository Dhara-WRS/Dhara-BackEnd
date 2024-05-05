import google.generativeai as genai
import json
import sys
import os

def generate_content(image_path):
    # Read the image content from the specified file path
    with open(image_path, 'rb') as file:
        image_content = file.read()

    # Set up the generative model
    genai.configure(api_key="AIzaSyCnJVnmcUm4jHHQhCw_gTTp25UtzGDGCUc")

    generation_config = {
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32,
        "max_output_tokens": 300,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    # Initialize the model
    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro-vision-latest",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    # Define the prompt using the image content
    image_parts = [{"mime_type": "image/jpeg", "data": image_content}]
    
    # Specify the prompt
    prompt_parts = [
        image_parts[0],
        "Write the output only in JSON format. ProblemDescription, ProblemType(Leakage, PotHoles, Contamination)",
    ]

    try:
        # Generate content using the model
        response = model.generate_content(prompt_parts)

        # Return the generated text as JSON
        result = {"generated_text": response.text}
        return json.dumps(result)
    
    except Exception as e:
        # Handle any exceptions and return an error message
        return json.dumps({"error": str(e)})

# Get the image path from the command-line argument
if len(sys.argv) > 1:
    image_path = sys.argv[1]
    # Call the function and print the output as JSON
    print(generate_content(image_path))
else:
    print(json.dumps({"error": "No image path provided as argument"}))
