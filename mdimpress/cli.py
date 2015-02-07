import codecs, sys, logging
from mdimpress import MDImpress, header_args_parse

logger = logging.getLogger()

def _choose_input(mdfile):
    "Choose input file depending on parameters"
    if mdfile:
        with codecs.open(mdfile,mode="rd",encoding="utf-8") as f:
            input_file = f.read()
    else: input_file = sys.stdin.read().decode('utf-8')
    return input_file

def _choose_output(output):
    "select output stream"
    output_file = sys.stdout
    if output: output_file = open(output,mode="w")
    return output_file


def main():
    from .argparser import MdArgumentParser
    parser = MdArgumentParser()
    args = parser.parse_args()

    # initialize presentation grunt devstack
    if args.presentation_start: MDImpress.presentation_start(constants.PATHS)


    # Reparse arguments using headers from markdown file
    input_file, header_args =  header_args_parse( _choose_input(args.mdfile) )
    args =  parser.parse_args( header_args + sys.argv[1:] )


    # set logger level
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)


    mapped_args = reduce(lambda x, y: x + [(y[1],getattr(args,y[0]),)] , 
    	[('stylesheet','stylesheets'), 
    	 ('meta','metadata'),  
    	 ('self_contained','self_contained')
    	], [])

    mapped_args = filter(lambda x: x!=None, mapped_args)

    MDImpress.compile(input_file, _choose_output(args.output_file), **dict(mapped_args))

