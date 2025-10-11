import os
import random
from django.conf import settings


DEFAULT_THUMBNAIL_POST_PATH = f'{settings.MEDIA_FOLDER}/default_thumbnails'
DEFAULT_AVATAR_PATH = f'{settings.MEDIA_FOLDER}/default_avatars'


def get_random_thumbnail():
    folder_path = DEFAULT_THUMBNAIL_POST_PATH
    files = [f for f in os.listdir(folder_path) if os.path.isfile(
        os.path.join(folder_path, f))]
    if not files:
        return None
    random_file = random.choice(files)
    random_file_path = f'/default_thumbnails/{random_file}'
    return random_file_path


def get_random_avatar():
    folder_path = DEFAULT_AVATAR_PATH
    files = [f for f in os.listdir(folder_path) if os.path.isfile(
        os.path.join(folder_path, f))]
    if not files:
        return None
    random_file = random.choice(files)
    random_file_path = f'/default_avatars/{random_file}'
    return random_file_path
