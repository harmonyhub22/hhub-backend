import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage
from flask_uploads import UploadSet, AUDIO

FILE_SET = UploadSet("files", AUDIO)

def saveFile(image: FileStorage, folder: str = None, name: str = None):
    return FILE_SET.save(image, folder, name)


def getPath(filename: str = None, folder: str = None):
    return FILE_SET.path(filename, folder)


def findImageAnyFormat(filename: str, folder: str):
    '''
    Given a format-less filename, try to find the file by appending each of the allowed formats to the given
    filename and check if the file exists
    :param filename: formatless filename
    :param folder: the relative folder in which to search
    :retunn: the path of the image if exists, otherwise None
    '''
    for _format in AUDIO:  # look for existing avatar and delete it
        avatar = f"{filename}.{_format}"
        avatar_path = FILE_SET.path(filename=avatar, folder=folder)
        if os.path.isfile(avatar_path):
            return avatar_path
    return None


def _retrieveFilename(file: Union[str, FileStorage]):
    '''
    Make our filename related functions generic, able to deal with FileStorage object as well as filename str.
    '''
    if isinstance(file, FileStorage):
        return file.filename
    return file
    


def getBasename(file: Union[str, FileStorage]):
    '''
    Return file's basename, for example
    get_basename('some/folder/image.jpg') returns 'image.jpg'
    '''
    filename = _retrieveFilename(file)
    return os.path.split(filename)[1]


def getExtension(file: Union[str, FileStorage]):
    """
    Return file's extension, for example
    get_extension('image.jpg') returns '.jpg'
    """
    filename = _retrieveFilename(file)
    return os.path.splitext(filename)[1]