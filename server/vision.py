import sys
import json
import supabase
from supabase import create_client
from typing import Dict, Any

import google.generativeai as genai
import json
import sys
import os

SUPABASE_URL = "https://tnrnbvggkjyhgfqwbjtb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRucm5idmdna2p5aGdmcXdianRiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTUwNjI5ODcsImV4cCI6MjAzMDYzODk4N30.13uYxEkOIcBHaXeadljH-vvjAXTT2_qkuFzg9KRdRY4"
desc = ""
problem = ""
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

def send_data_to_supabase(latitude, longitude, location, desc, problem):
    data_to_insert = {
        "Latitude": latitude,
        "Longitude": longitude,
        "location": location,
        "desc": desc,
        "problem": problem
    }
    print("Data to insert:", data_to_insert)
    response = supabase_client.table("Epics").insert(data_to_insert).execute()
    print("Response from Supabase:", response)
    return {
        "success": True,
        "Latitude": latitude,
        "Longitude": longitude,
        "location": location,
        "desc": desc,
        "problem": problem,
        "data": response.data
    }

def handle_location_data(location_data):
    print("Location data received:", location_data)
    latitude = location_data.get("Latitude")
    longitude = location_data.get("Longitude")
    location = location_data.get("location")
    desc = location_data.get("desc", "Unknown Location")
    problem = location_data.get("problem", "Unknown Problem Type")
    print("Extracted data:", latitude, longitude, location, desc, problem)
    return latitude, longitude, location, desc, problem

def handle_generated_data(data_dict, location_data):
    desc = data_dict.get("ProblemDescription", "Unknown Location")
    problem = data_dict.get("ProblemType", "Unknown Problem Type")
    print("2", desc, problem)

    # Update location_data with generated data
    location_data["desc"] = desc
    location_data["problem"] = problem

    return location_data

def format_json(json_text):
    try:
        # Extract JSON string from the text
        json_string = json_text.split('```json\n')[1].replace('\\n', '\n').replace('\\"', '"').split('\n```')[0]

        # Format the extracted JSON string into perfect JSON
        formatted_json = json.loads(json_string)
        return json.dumps(formatted_json, indent=2)
    except Exception as e:
        # Return original JSON text if formatting fails
        return json_text

def generate_content(image_path, location_data):
    try:
        # Read the image content from the specified file path
        with open(image_path, 'rb') as file:
            image_content = file.read()

        print("Image content read successfully.")

        # Set up the generative model
        print("Configuring generative model...")
        genai.configure(api_key="AIzaSyCnJVnmcUm4jHHQhCw_gTTp25UtzGDGCUc")

        print("Generative model configured successfully.")

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
        print("Initializing generative model...")
        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro-vision-latest",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

        print("Generative model initialized successfully.")

        # Define the prompt using the image content
        image_parts = [{"mime_type": "image/jpeg", "data": image_content}]

        # Specify the prompt
        prompt_parts = [
            image_parts[0],
            "Write the output only in JSON format. ProblemDescription, ProblemType(Leakage,PotHoles,Contamination,Clogged Drains or NotApplicable)",
        ]

        # Generate content using the model
        print("Generating content using the model...")
        response = model.generate_content(prompt_parts)

        print("Content generated successfully.")

        # Format the generated JSON text
        formatted_json = format_json(response.text)

        # Remove occurrences of "`"
        formatted_json = formatted_json.replace('`', '')

        # Parsing JSON string into a dictionary
        data_dict = json.loads(formatted_json)

        print("Data generated:", data_dict)

        # Call handle_generated_data to update location_data
        location_data = handle_generated_data(data_dict, location_data)

        return location_data

    except Exception as e:
        print("An error occurred:", str(e))
        # Handle any exceptions and return an error message
        return json.dumps({"error": str(e)})

if len(sys.argv) == 1:
    print(json.dumps({
        "error": "Insufficient arguments. Please provide the image path and location data as arguments."
    }))
elif len(sys.argv) == 3:
    image_path = sys.argv[1]
    location_data = json.loads(sys.argv[2])
    print("Received image path:", image_path)
    print("Received location data:", location_data)

    latitude, longitude, location, desc, problem = handle_location_data(location_data)
    location_data = generate_content(image_path, location_data)
    send_data_to_supabase(latitude, longitude, location, location_data["desc"], location_data["problem"])
    print(json.dumps(location_data))
else:
    print(json.dumps({
        "error": "Invalid number of arguments. Please provide the image path and location data as arguments."
    }))
