import os
import requests
from dotenv import load_dotenv
from random import randint


def fetch_image(url):
    response = requests.get(url).json()
    title = '{}.png'.format(response['title'])
    comment = response['alt']
    with open(title, 'wb') as f:
        f.write(requests.get(response['img']).content)
    return title, comment


def get_upload_url(access_token, group_id):
    return requests.get('https://api.vk.com/method/photos.getWallUploadServer', params={
        'access_token': access_token,
        'v': 5.95,
        'group_id': group_id}
                              ).json()['response']['upload_url']


def upload_photo(access_token, upload_url):
    with open(title, 'rb') as photo_file:
        files = {'photo': photo_file}
        response = requests.post(upload_url, files=files, params={'access_token': access_token}).json()
    return response['server'], response['photo'], response['hash']


def save_wall_photo(access_token, photo, server, hash):
    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto', data={
        'photo': photo,
        'server': server,
        'hash': hash}, params={
        'access_token': access_token,
        'v': 5.95,
        'group_id': group_id}
                             ).json()['response'][0]
    return response['id'], response['owner_id']


def wall_post(access_token, group_id, media_id, owner_id):
    requests.get('https://api.vk.com/method/wall.post', params={
        'access_token': access_token,
        'v': 5.95,
        'owner_id': -group_id,
        'from_group': 1,
        'attachments': 'photo{}_{}'.format(owner_id, media_id),
        'message': comment})


if __name__ == '__main__':
    load_dotenv()
    access_token = os.getenv('access_token')
    group_id = int(os.getenv('group_id'))
    amount_of_comics = requests.get('http://xkcd.com/info.0.json').json()['num']
    title, comment = fetch_image('http://xkcd.com/{}/info.0.json'.format(randint(1, amount_of_comics)))
    upload_url = get_upload_url(access_token, group_id)
    server, photo, hash = upload_photo(access_token, upload_url)
    media_id, owner_id = save_wall_photo(access_token, photo, server, hash)
    wall_post(access_token, group_id, media_id, owner_id)
    os.remove(title)
