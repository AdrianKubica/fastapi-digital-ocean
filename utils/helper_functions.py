import requests


async def upload_image_to_server(file):
    result = requests.post("http://some_upload_photo_url", files={"image": file})
    print(result.json())
