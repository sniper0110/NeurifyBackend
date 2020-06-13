import os
import magic


def image_is_valid(file):

    valid_mime_types = ['image/png', 'image/jpeg', 'image/jpg']
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    if file_mime_type not in valid_mime_types:
        return False

    valid_file_extensions = ['.png', '.jpeg', '.jpg']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        return False

    return True