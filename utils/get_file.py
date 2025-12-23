import requests

async def get_file_request(track_code : str):
    url = f'https://file.topcargo.uz/api/files/byname/{track_code}'
    # So'rov yuborish
    response = requests.get(url, headers={'accept': '*/*'})
    print(response.json())
    return response.json() # Fayl ma'lumotlari yoki rasm ko'rinishida


