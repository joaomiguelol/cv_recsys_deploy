from os.path import join

from config import project_dir


with open(join(project_dir, 'VERSION.txt'), encoding='utf-8') as f:
    __version__ = f.read()


if __name__ == "__main__":
    print(__version__)

# EOF
