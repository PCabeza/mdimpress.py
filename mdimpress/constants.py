import re

MD_HTML_RE = r"\[(?P<text>.*?)(?<!\\)\]<(?P<tag>.*?)>" # uses 'text' and 'tag' groups
HTML_ELEMENT = r'<%(tag)s %(attr)s>%(body)s</%(tag)s>'
STYLESHEET = r'<link rel="stylesheet%(type)s" type="text/css" href="%(href)s"/>'

PANDOC_CALL = ["pandoc", "-t","html5","--section-divs", "-s"]
TAGATTR_RE = re.compile(r'(.+?)=(.*)')
TRANSLATE_RE = re.compile(r'(?P<header_brace>#.*?\{)(?P<braces>.*?)\}')
TRANSLATE_RE_SUB = r'\g<header_brace>%(braces)s}'
HEADER_LEVEL = 1 # to which header level append .step automatically






def translation(match):
    res = []
    numbers = match.group(2).split(",")
    for i,x in enumerate(match.group(1)):
        res += ["data-%s=%s" % (x,numbers[i])]

    return ' '.join(res)


def rotation(match):
    res = []
    numbers = match.group(2).split(",")
    for i,x in enumerate(match.group(1)[1:] if match.group(1) else ['z']):
        res += ["data-rotate-%s=%s" % (x,numbers[i])]

    return ' '.join(res)


TRANSLATION_TABLE=(
    (r'(?:^| )([xyz]{1,3})=\(?((?:.*?,){0,2}(?:.*?))\)?(?:$| )', translation,),
    (r'(?:^| )rot((?:-[xyz]{1,3})?)=\(?((?:[^\s]*?,){0,2}(?:[^\s]*?))\)?(?:$| )', rotation),
    (r'(?:^| )zoom=(.*?)(?:$| )', lambda m: "data-scale=%s" % m.group(1)),
)
