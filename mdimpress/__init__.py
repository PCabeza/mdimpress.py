import os
from .mdimpress import main as md_main
import logging, sys

_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data(path):
    return os.path.join(_ROOT, 'data', path)


PATHS = dict(
	BASE_PATH = get_data(''),
	TEMPLATE_PATH = get_data("template"),
	TEMPLATE_FILE = get_data("template/impress-template.html"),
	GRUNT_DIR = get_data("grunt"),
)


logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
logger.addHandler(ch)


def main(): md_main(PATHS)

if __name__ == "__main__": main()