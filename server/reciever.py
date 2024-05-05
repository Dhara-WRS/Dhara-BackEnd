import os
import google.generativeai as genai
import json

def get_latest_image_path(folder_path):
    # Get the list of files in the specified folder
    files = os.listdir(folder_path)
    
    # Create a list of full paths to the files
    files_with_paths = [os.path.join(folder_path, file) for file in files]

    # Get the file with the most recent modification time
    latest_file = max(files_with_paths, key=os.path.getmtime)
    
    return latest_file

def generate_content_from_latest_image(folder_path):
    # Get the path of the latest image file
    latest_image_path = get_latest_image_path(folder_path)
    
    # Read the image content from the latest image file
    with open(latest_image_path, 'rb') as file:
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

    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro-vision-latest",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    
    image_parts = [
        {"mime_type": "image/jpeg", "data": image_content},
    ]
    
    prompt_parts = [
        image_parts[0],
        "Write the output only in JSON format. ProblemDescription, ProblemType(Leakage,PotHoles,Contamination)",
    ]
    
    # Generate content using the model
    response = model.generate_content(prompt_parts)
    
    # Return the generated text as a dictionary
    return {"generated_text": response.text}

# Example usage:
folder_path = "/root/AYUSH/Dhara-BackEnd/images"
result = generate_content_from_latest_image(folder_path)
print(result)
