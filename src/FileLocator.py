import os


class FileLocator:

    @staticmethod
    def get_file_path(file_name: str, search_root_path: str) -> str:
        for dir_path, dir_name, file_name_in_dir in os.walk(search_root_path):
            if file_name in file_name_in_dir:
                return os.path.join(dir_path, file_name)
