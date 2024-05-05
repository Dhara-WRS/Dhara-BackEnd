import requests

pipedream_url = "http://165.22.255.126:5000/upload"
image_path = 'D:/CODE/projects/python/Dhara-BackEnd/samples/OIP.jpeg'

with open(image_path, 'rb') as image_file:
    image_content = image_file.read()

response = requests.post(pipedream_url, files={"image": image_content})

print(response.text)