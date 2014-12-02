#! /usr/bin/python

'''
Depends of packages:
- 

And uses the tool:
- pandoc
'''

import argparse, re, codecs, sys, os
from subprocess import Popen,PIPE

HTML_ELEMENT = r'<%(tag)s %(attr)s>%(body)s</%(tag)s>'

PANDOC_CALL = ["pandoc", "-t","html5","--section-divs", "-s"]
TAGATTR_RE = re.compile(r'(.+?)=(.*)')
TRANSLATE_RE = re.compile(r'#.*?\{(.*?)\}')


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
    (r'rot((?:-[xyz]{1,3})?)=\(?((?:.*?,){0,2}(?:.*?))\)?(?:$| )', rotation),
)

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_FILE = os.path.join(BASE_PATH,"impress-template.html")
IMPRESS_PATH = os.path.join(BASE_PATH, "impress.js")

def translation_process(md):
    table = [(re.compile(i[0]),i[1]) for i in TRANSLATION_TABLE]
    
    for l in md.splitlines():
        m = TRANSLATE_RE.match(l)
        if not m: continue
        for r in table:
            m1=r[0].search(m.group(1))
            if m1:
                md = md.replace(m1.group(0)," %s " % r[1](m1))
    return md


def parsetag(gr):
    '''
    Parses de body of a tag of the form:
    
    	<tag #id .class1 .class2 attr1=value1 attr2=value2>
    And returns a pair (tag, attributes) for use in a html element
    '''
    tag = 'span'
    attr = {}
    for w in gr.split():
        # id
        if w[0]=="#": attr["id"]=[w[1:]]

        # class
        elif w[0]==".": attr["class"] = attr.get("class",[])+[w[1:]] 
        
	else:
            r = TAGATTR_RE.match(w)
            if r: attr[r.group(1)] = attr.get(r.group(1),[])+[r.group(2)]
            else: tag = w
        
    return tag, ' '.join(['%s=%s'%(k,' '.join(v)) for k,v in attr.iteritems()])

def elementclass(md):
    '''
    Transforms elements of the form:

    	<tag .class #id attr=value>[text]

    To elements of the form `<tag class="class">text</tag>`.
    If `tag` is not included, `span` will be used
    '''
    finds = re.finditer(r"<(.*?)>\[(.*?)(?<!\\)\]",md)
    for i in list(finds):
        tag, attr = parsetag(i.group(1))
        md = md.replace(i.group(0),
                            HTML_ELEMENT % {"tag":tag, "attr":attr,
                                            "body":i.group(2)})
    return md


# parse arguments
parser = argparse.ArgumentParser(description='')
parser.add_argument('mdfile', nargs='?')
parser.add_argument('--output-file','-o', nargs='?')
parser.add_argument('--extra-css','-css',nargs='?')
parser.add_argument('--self-contained','-S',action='store_true')
args = parser.parse_args()

# Choose input file depending on parameters
if args.mdfile: 
    with codecs.open(args.mdfile,mode="rd",encoding="utf-8") as f:
        input_file = f.read()
else: input_file = sys.stdin.read().decode('utf-8')

if args.self_contained: PANDOC_CALL+=["--self-contained"]
if args.extra_css: PANDOC_CALL+=["-V","extra-css-url=%s" % (args.extra_css,)]

# Template file is compulsory
PANDOC_CALL += ["--template", TEMPLATE_FILE]
# impress js folder
PANDOC_CALL += ["-V","impress-url=%s" % IMPRESS_PATH ]




# process input to preparse it
preprocessed = translation_process(input_file)
preprocessed = elementclass(preprocessed)


# Execute pandoc to generate output
pid = Popen(PANDOC_CALL, stdin=PIPE,stdout=PIPE)
out = pid.communicate(preprocessed.encode('utf-8'))


output_file = sys.stdout
if args.output_file: output_file = open(args.output_file,mode="w")

output_file.write(out[0])
