import os

def delete_image_from_directory(directory: str, filename_without_extension: str) -> None:
    for file in os.listdir(directory):
        if file.startswith(filename_without_extension):
            os.remove(os.path.join(directory, file))
            break

def get_file_extension(directory: str, filename_without_extension: str) -> str:
    for file in os.listdir(directory):
        if file.startswith(filename_without_extension):
            return file.split('.')[-1]
    return ""