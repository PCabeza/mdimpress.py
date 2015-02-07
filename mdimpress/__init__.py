import os, logging, sys, re
from collections import namedtuple


_ROOT = os.path.abspath(os.path.dirname(__file__))
def _get_data(path):
    return os.path.join(_ROOT, 'data', path)


logger = logging.getLogger()
logger.setLevel(logging.INFO)
_ch = logging.StreamHandler(sys.stdout)
logger.addHandler(_ch)


CONSTANTS_DICT = {
	'MD_HTML_RE': r"\[(?P<text>.*?)(?<!\\)\]<(?P<tag>.*?)>", # uses 'text' and 'tag' groups
	'HTML_ELEMENT': r'<%(tag)s %(attr)s>%(body)s</%(tag)s>',
	'STYLESHEET': r'<link rel="stylesheet%(type)s" type="text/css" href="%(href)s"/>',


	'TAGATTR_RE': re.compile(r'(.+?)=(.*)'),
	'TRANSLATE_RE': re.compile(r'(?P<header_brace>#.*?\{)(?P<braces>.*?)\}'),
	'TRANSLATE_RE_SUB': r'\g<header_brace>%(braces)s}',
	'HEADER_LEVEL': 1, # to which header level append .step automatically


	'PATHS': dict(
		BASE_PATH = _get_data(''),
		TEMPLATE_PATH = _get_data("template"),
		TEMPLATE_FILE = _get_data("template/impress-template.html"),
		GRUNT_DIR = _get_data("grunt"),
	),
}

Constant = namedtuple('Constant',CONSTANTS_DICT.keys())
constants = Constant(**CONSTANTS_DICT)