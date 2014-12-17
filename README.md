# mdimpress.py

The idea behind it is to create a tool that allows a fluid workflow
when creating impress.js based presentations, while retaining full
control over the html and css code.

Based in this [page][pandoc_impress] from the pandoc wiki you can
already use markdown to build a simple presentation, but I wanted to
optimize the process, because the markdown files created this way
weren't readable.

# Features

- [x] Extensions of headings `{}` pandoc syntax.
- [x] Append automatically .step to header `{}` blocks.
- [x] Extension of markdown semantic syntax.
- [ ] Metadata included into generated html.
- [x] Header block syntax to pass arguments to mdimpress.py from the
  markdown file.

# Extension of headings syntax

In pandoc you can write headings that when rendered to html includes
the specified id, classes and attributes into its node. For writing
presentations this means you have to write many `data-x=number` or
`data-rotate-z=number` attributes, for example:
	
	# some heading {.step data-x=1000 data-y=-250 data-rotate-y=90 data-scale=1.5}

Using the mdimpress.py syntax this will be written as:

	# some heading {xy=(1000,-250) rot-y=90 zoom=1.5}

Saving you space, time and improving readability. Here is a list of special
attributes added to heading in order to save time.

### `.step` append automatically

When there is a first level header block, a `.step` class will added. This means that `# heading {}` is transformed into `# heading {.step}`.

*Note*: As for now `{}` is compulsory, even if empty.

### Translations

**Syntax**: `xyz=(a,b,c)`

Any subset of `xyz` can be used, in any order, the coordinates and numbers
will be matched in the order given. This means you can write, for example,
`zy=(c,b)`. 

Parenthesis are optional.

### Rotations

**Syntax**: `rot-xyz=(a,b,c)` | `rot=a`

The meaning and syntax is the same as for [Translations](#translations). For
the case without coordinates, `z` is used (same as using data-rotate with
impress.js).

### Zoom

**Syntax**: `zoom=n`

This is just a shortcut for `data-scale=n`, uses fewer letters and is easy to
remember.

# Header block

To not pass all arguments to mdimpress.py you can write a *header block*. This
block is composed of arguments as obtained from `mdimpres.py -h`, in the long
version.

There are different types of blocks. They can appear one after another, having
more than one header block, but all must appear before any non-blank, non %
prefixed line. The arguments defined in header blocks can be overridden by
command-line options.

## Anonymous header block

They have the form of:

	%%
	% argument1
	% argument2: value

This will be roughly the same as calling the program with `--argument1
--argument2 value`


## Prefixed header block

	%% arg
	% key1: value1
	% key2: value2
	% key3

This will be translated to `--arg key1=value1 --arg key2=value2 --arg key3`.
This block is useful when including many stylesheets or for defining metadata.


# Extension of pandoc markdown syntax

## inline html elements

**Syntax**: `[text]<[tag] #id .class attr1=val1>`

It is based on pandoc header `{}` syntax and on markdown links. HTML
can be inlined into markdown files, but this syntax is more readable
and less verbose.

`tag` is optional, if omitted `span` is used, but can be any.


# Future features

- Relative translations and rotations

[pandoc_impress]: <https://github.com/jgm/pandoc/wiki/Creating-impress.js-slide-shows-with-pandoc>

[grunt_livereload]: <https://github.com/gruntjs/grunt-contrib-watch#optionslivereload>
[extensions_livereload]: <http://feedback.livereload.com/knowledgebase/articles/86242-how-do-i-install-and-use-the-browser-extensions>
 

