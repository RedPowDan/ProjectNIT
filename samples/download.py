import os
import uuid
import time

from requests import request


def write_file(data: bytes):
    folder = 'download'
    if not os.path.exists(folder):
        os.mkdir(folder)

    file_name = str(uuid.uuid4()) + '.ico'
    file_path = os.path.join(folder, file_name)
    with open(file_path, 'wb') as file:
        file.write(data)


def download_image(url: str):

    response = request(method='get', url=url)

    if response.status_code == 200:
        write_file(response.content)


def main():
    for _ in range(5):
        download_image('https://www.google.com/favicon.ico')


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f'Total time: {time.time() - start_time} sec')
