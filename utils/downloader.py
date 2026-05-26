import requests

def download_file(url, output_path):

    response = requests.get(
        url,
        stream=True
    )

    if response.status_code != 200:
        raise Exception("Erro ao baixar arquivo")

    with open(output_path, "wb") as file:

        for chunk in response.iter_content(1024):

            file.write(chunk)