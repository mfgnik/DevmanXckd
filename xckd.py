import os
import requests
from dotenv import load_dotenv
from random import randint


def fetch_image(url):
    response = requests.get(url).json()
    try:
        title = '{}.png'.format(response['title'])
        comment = response['alt']
        with open(title, 'wb') as f:
            f.write(requests.get(response['img']).content)
    except KeyError:
        raise requests.exceptions.HTTPError
    return title, comment


def get_upload_url(access_token, group_id):
    try:
        return requests.get('https://api.vk.com/method/photos.getWallUploadServer', params={
            'access_token': access_token,
            'v': 5.95,
            'group_id': group_id}
                            ).json()['response']['upload_url']
    except KeyError:
        raise requests.exceptions.HTTPError


def upload_photo(access_token, upload_url):
    with open(title, 'rb') as photo_file:
        files = {'photo': photo_file}
        response = requests.post(upload_url, files=files, params={'access_token': access_token}).json()
    try:
        return response['server'], response['photo'], response['hash']
    except KeyError:
        raise requests.exceptions.HTTPError


def save_wall_photo(access_token, server, photo, image_hash):
    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto', data={
        'photo': photo,
        'server': server,
        'hash': image_hash}, params={
        'access_token': access_token,
        'v': 5.95,
        'group_id': group_id}
                             ).json()['response'][0]
    try:
        return response['id'], response['owner_id']
    except KeyError:
        raise requests.exceptions.HTTPError


def wall_post(access_token, group_id, media_id, owner_id):
    response = requests.get('https://api.vk.com/method/wall.post', params={
        'access_token': access_token,
        'v': 5.95,
        'owner_id': -group_id,
        'from_group': 1,
        'attachments': 'photo{}_{}'.format(owner_id, media_id),
        'message': comment}).json()
    print(response)
    if 'error' in response:
        raise requests.exceptions.HTTPError


if __name__ == '__main__':
    load_dotenv()
    access_token = os.getenv('access_token')
    group_id = int(os.getenv('group_id'))
    try:
        amount_of_comics = requests.get('http://xkcd.com/info.0.json').json()['num']
        title, comment = fetch_image('http://xkcd.com/{}/info.0.json'.format(randint(1, amount_of_comics)))
        wall_post(access_token, group_id,
                  *save_wall_photo(access_token, *upload_photo(access_token, get_upload_url(access_token, group_id))))
    finally:
        os.remove(title)
