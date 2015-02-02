import argparse
from .mdimpress import METADATA

class MdArgumentParser(argparse.ArgumentParser):

    construction = {
        'description':'''
    		Utility that extends pandoc markdown syntax to easy creation of
    		impress.js presentations using pandoc utility.''',
    }

    args = [
        dict(flags=['mdfile'], nargs='?', help='markdown file to compile'),
        {'flags':['--output-file','-o'], 'nargs':'?','help':'save output to this file'},
        {'flags':['--stylesheet','-s'],'action':'append',  'default':[],
                        'help':'path to stylesheets file to add'},
        {'flags':['--self-contained','-S'],'action':'store_true', 
                    'help':'include dependencies in output'},
        {'flags':['--external-links','-e'],'action':'store_false', 'dest':'self_contained', 
         'help':'force externals to not be included'},
        {'flags':['--meta','-m'], 'action':'append', 'default':[],
         'help':"update metadata for the presentation, can be any of %s" % 
         ' or '.join([', '.join(METADATA.keys()[:-1]),METADATA.keys()[-1]])},
        {'flags':['--presentation-start'],'action':"store_true", 
         'help':"creates grunt devstack structure for mdimpress"},
        {'flags':['--debug'],'action':"store_true",
         'help':"sets debug output"},

    ]

    def __init__(self):
        argparse.ArgumentParser.__init__(self,**MdArgumentParser.construction)
        for arg in MdArgumentParser.args:
            # print arg
            flags = arg.get('flags',[])
            if flags: del arg['flags']
            self.add_argument(*flags,**arg)
