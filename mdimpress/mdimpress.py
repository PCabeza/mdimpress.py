#! /usr/bin/python

import argparse, re, codecs, sys, os, tempfile, logging
from os.path import splitext
from subprocess import Popen,PIPE
from distutils.dir_util import copy_tree

from .constants import *


logger = logging.getLogger(__name__)

def translation_process(md):
    '''
    This function is used to extend pandoc markdown syntax for headings. A heading has the form:

    	# my heading title {#id .class1 attribute1=value1}

    This function uses the regexps from TRANSLATION_TABLE to create custom syntax, for example:
    
    	xy=100,-100
    
    would be translated to:
    
    	data-rotate-x=100 data-rotate-y=-100

    It also appends .step to headers automatically (only those that have {})
    '''
    table = [(re.compile(i[0]),i[1]) for i in TRANSLATION_TABLE]
    mdl = []

    for i,l in enumerate(md.splitlines()):
        m = TRANSLATE_RE.match(l)
        if not m: 
            mdl.append(l); continue

        logger.debug("Header match in line %i: %s" % (i,l)) 
        braces = m.group('braces') # new brace value to update

        # TODO: as for now {} is compulsory, or .step wont be added
        # add .step to header
        if m.group('header_brace')[HEADER_LEVEL]!= "#" and \
           reduce(lambda b,a: (a=="#") and b,m.group('header_brace')[:HEADER_LEVEL],True):
            braces = ".step " + braces

        # TODO: parse tokens
        for r in table:
            braces = r[0].sub(lambda f: " %s " % r[1](f),braces)
            # m1=r[0].search(m.group('braces'))
            # if m1:
            #     # print r,m1.groups()
            #     md = md.replace(m1.group(0)," %s " % r[1](m1))
        
        transd = TRANSLATE_RE.sub(TRANSLATE_RE_SUB % {'braces': braces}, l)
        logger.debug('after translation: %s' % transd)
        mdl.append(transd)
        # print braces

    return os.linesep.join(mdl)


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
    logging.debug("parsed tag %s, found %s" % (gr,attr))
    return tag, ' '.join(['%s=%s'%(k,' '.join(v)) for k,v in attr.iteritems()])

def elementclass(md):
    '''
    Transforms elements of the form:

    	<tag .class #id attr=value>[text]

    To elements of the form `<tag class="class">text</tag>`.
    If `tag` is not included, `span` will be used
    '''
    finds = re.finditer(MD_HTML_RE,md)
    for i in list(finds):
        tag, attr = parsetag(i.group('tag'))
        md = md.replace(i.group(0),
                            HTML_ELEMENT % {"tag":tag, "attr":attr,
                                            "body":i.group('text')})
    return md

METADATA = {
    'title': "",
    'description': type('aux_desc',(object,),{'__repr__':lambda s: METADATA['title']})(),
    'author': "" 
}


def header_args_parse(md):
    '''Parses a special header block from markdown file.
    The header block has the form of:

    	%% [master_arg]
    	% arg_key: arg_value

    Several header blocks can be given in series. It must be the
    firsts elements of the markdown file.
    
    If master_arg is give, the (key,value) pairs are used are
    arguments of the master_arg, else key is the argument and value is
    used as the argument value.
    '''
    state=None
    args = []

    lines = md.splitlines()
    lno = 0
    for l in lines:
        l = l.strip()
        if not l: 
            lno+=1; continue
        
        if l[:2]=="%%": state=l[2:].strip() # new group
    	elif l[0]=="%": # element
            w = [i.strip() for i in l[1:].split(":",1)] # strip spaces
            if state: args+= ['--%s'%state, 
                              (lambda x: "%s%s"% (x[0], "="+(x[1]) if len(x)>1 else ""))(w)]
            else: args+=(lambda x: ['--%s'%x[0]]+([x[1]] if len(x)>1 else []))(w)
            
        else: break
        lno+=1

    return (os.linesep.join(lines[lno:]),args)


def main(PATHS):
    global PANDOC_CALL

    from .argparser import MdArgumentParser
    parser = MdArgumentParser()
    args = parser.parse_args()

    if args.presentation_start: # initialize presentation grunt devstack
        copy_tree(PATHS['GRUNT_DIR'],os.getcwd())
        exit(0)
    
            

    # Choose input file depending on parameters
    if args.mdfile: 
        with codecs.open(args.mdfile,mode="rd",encoding="utf-8") as f:
            input_file = f.read()
    else: input_file = sys.stdin.read().decode('utf-8')


    # Reparse arguments using headers from markdown file
    input_file, header_args =  header_args_parse(input_file)
    args =  parser.parse_args(header_args+sys.argv[1:])

    METADATA.update(m.split('=',1) for m in args.meta) # process metadata
    
    # set logger level
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)

    # Build extra arguments for pandoc call
    if args.self_contained: PANDOC_CALL+=["--self-contained"]
    PANDOC_CALL += ["-V","base-url=%s" % PATHS['TEMPLATE_PATH'] ] # template folder

    # TODO: fix, for css, just stylesheet; for less, stylesheet/less
    template_args = {
        # stylesheet elements
        'stylesheets': ''.join(
            [ STYLESHEET % {'type':(lambda x: "/"+x if x=="less" else "")(splitext(s)[1][1:]), 'href': s} for s in args.stylesheet])
    }
    template_args.update(METADATA)

    temp_template = None    
    with tempfile.NamedTemporaryFile(mode='wb',delete=False,suffix=".html") as template:
        temp_template = template.name
        with open(PATHS['TEMPLATE_FILE'], 'r') as orig:
            template.write((orig.read().decode('utf-8') % template_args).encode('utf-8'))
    
    PANDOC_CALL += ["--template", temp_template] # Template file is compulsory


    # process input to preparse it
    preprocessed = translation_process(input_file)
    preprocessed = elementclass(preprocessed)


    # Execute pandoc to generate output
    pid = Popen(PANDOC_CALL, stdin=PIPE,stdout=PIPE)
    out = pid.communicate(preprocessed.encode('utf-8'))
    
    # remove temporary template template file 
    os.unlink(temp_template)

    output_file = sys.stdout
    if args.output_file: output_file = open(args.output_file,mode="w")

    output_file.write(out[0])

if __name__=="__main__":
    main()
