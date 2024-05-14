import requests
import time

def upload_image(image_path):
    url = 'http://165.22.255.126:5000/upload'

    start_time = time.time()
    with open(image_path, 'rb') as img:
        files = {'image': img}
        response = requests.post(url, files=files)
        print(response.text)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f'Execution time: {execution_time:.2f} seconds')

if __name__ == '__main__':
    upload_image("./samples/maxresdefault.jpg")
