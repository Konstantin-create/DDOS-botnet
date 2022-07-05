import os
from sys import platform


def modify_path(path):
    if sys.platform.startswith("linux"):
        return path.replace('\\', '/')
    elif platform == 'win32':
        return path.replace('/', '\\')


class PathConfigs:
    # Path to folders
    project_folder = os.path.dirname(os.path.abspath(__file__))
    static_folder = f'{project_folder}\\static'
    templates_folder = f'{project_folder}\\templates'

    # Let's bring the paths into the form of a os
    if platform == 'linux' or platform == 'linux2':
        project_folder = project_folder.replace('\\', '/')
        static_folder = static_folder.replace('\\', '/')
        templates_folder = templates_folder.replace('\\', '/')
    elif platform == 'win32':
        project_folder = project_folder.replace('/', '\\')
        static_folder = static_folder.replace('/', '\\')
        templates_folder = templates_folder.replace('/', '\\')
