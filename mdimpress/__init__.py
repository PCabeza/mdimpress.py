import os
import mdimpress

_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data(path):
    return os.path.join(_ROOT, 'data', path)


PATHS = dict(
	BASE_PATH = get_data(''),
	TEMPLATE_PATH = get_data("template"),
	TEMPLATE_FILE = get_data("template/impress-template.html"),
	GRUNT_DIR = get_data("grunt"),
)


def main(): mdimpress.main(PATHS)
