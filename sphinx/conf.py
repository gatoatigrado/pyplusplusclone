# -*- coding: utf-8 -*-
#
# Language Binding documentation build configuration file, created by
# sphinx-quickstart on Wed Jan 28 10:41:40 2009.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed automatically).
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os, shutil, getopt

opts, args = getopt.getopt( sys.argv[1:], 'ab:d:c:CD:A:NEqQP:w')
print 'opts: ', opts
print 'args: ', args
outdir = args[1]

# If your extensions are in another directory, add it here. If the directory
# is relative to the documentation root, use os.path.abspath to make it
# absolute, like shown here.
#sys.path.append(os.path.abspath('.'))

project_root = os.path.abspath('..')
doc_project_root = os.path.abspath('.')
packages = ( 'pydsc', 'pygccxml', 'pyplusplus' )

sys.path.append( doc_project_root )

has_true_links = 'linux' in sys.platform
for pkg in packages:
    target = os.path.join( doc_project_root, pkg )
    source = os.path.join( project_root, pkg + '_dev', 'docs' )
    sys.path.append( os.path.join( project_root, pkg + '_dev' ) )
    if os.path.exists( target ):
        if has_true_links:
            os.unlink( target )
        else:
            shutil.rmtree( target )

    if has_true_links:
        os.symlink( source, target )
    else:
        shutil.copytree( source, target, ignore=shutil.ignore_patterns( r'.svn', '*.pyc', 'osdc2006' ) )
if has_true_links:
    if os.path.exists(os.path.join( doc_project_root, 'index.rest' )):
        os.unlink( os.path.join( doc_project_root, 'index.rest' ) )
    os.symlink( os.path.join( project_root, 'index.rest' )
                , os.path.join( doc_project_root, 'index.rest' ) )
else:
    shutil.copy( os.path.join( project_root, 'index.rest' ), doc_project_root )

try:
    #~ import pydsc
    #report errors related to the project only
    #~ pydsc.include_paths( project_root )
    #~ pydsc.ignore_dictionary( 'ignore_dictionary.txt' )
    #~ pydsc.set_text_preprocessor( pydsc.sphinx_preprocessor )
    import pygccxml
    import pyplusplus
except:
    pass #it is possible that pyenchant is not installed

def copy_indexing_suite_v2_files(app, exception):
    if exception:
        print 'Indexing suite V2 copying was skipped - there were errors during the build process'
        return
    source_dir = os.path.join( project_root, 'pyplusplus_dev', 'docs', 'documentation', 'indexing_suite_v2_files' )
    target_dir = os.path.join( doc_project_root, outdir, 'pyplusplus', 'documentation', 'indexing_suite_v2_files' )
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    shutil.copytree( source_dir, target_dir, ignore=shutil.ignore_patterns( r'.svn' ) )

def generate_sitemap(app, exception):
    if 'www' not in outdir:
        return
    if exception:
        print 'SITEMAP generation was skipped - there were errors during the build process'
        return
    try:
        import sitemap_gen

        working_dir = os.path.join( doc_project_root, outdir )
        config = \
        """<?xml version="1.0" encoding="UTF-8"?>
        <site base_url="http://www.language-binding.net/" store_into="%(path)s/sitemap.xml.gz" verbose="1">
            <directory path="%(path)s" url="http://www.language-binding.net/" default_file="index.html" />
            <filter  action="drop"  type="regexp"    pattern="/\.[^/]*" />
            <filter  action="drop"  type="regexp"    pattern="/_[^/]*" />
        </site>
        """ % dict( path=os.path.join( doc_project_root, working_dir ) )

        f_config_path = os.path.join( working_dir, 'sitemap_config.xml' )
        f_config = file( f_config_path, 'w+' )
        f_config.write( config )
        f_config.close()

        sitemap = sitemap_gen.CreateSitemapFromFile(f_config_path, True)
        if not sitemap:
            print 'ERROR(SITEMAP): configuration file errors'
        else:
            sitemap.Generate()
            print 'ERRORS(SITEMAP): %d' % sitemap_gen.output.num_errors
            print 'WARNINGS(SITEMAP): %d' % sitemap_gen.output.num_warns
    except Exception, error:
        print "ERROR(SITEMAP): sitemap file was not generated - ", str(error)


def setup(app):
    app.connect('build-finished', copy_indexing_suite_v2_files)
    app.connect('build-finished', generate_sitemap)

# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.intersphinx', 'sphinx.ext.todo', 'sphinx.ext.coverage']
# Add any paths that contain templates here, relative to this directory.
templates_path = ['__templates']
if 'www' in outdir:
    templates_path = ['__templates_www']

# The suffix of source filenames.
source_suffix = '.rest'

# The encoding of source files.
#source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Language Binding'
copyright = u'2009, Roman Yakovenko'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '1.1'
# The full version, including alpha/beta/rc tags.
release = '1.1'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ['__build']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# Options for HTML output
# -----------------------

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
html_style = 'default.css'

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = 'favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['__static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_use_modindex = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, the reST sources are included in the HTML build as _sources/<name>.
html_copy_source = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'LanguageBindingdoc'


# Options for LaTeX output
# ------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).
latex_documents = [
  ('index', 'LanguageBinding.tex', ur'Language Binding Documentation',
   ur'Roman Yakovenko', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True

#If true, keep warnings as “system message” paragraphs in the built documents.
#Regardless of this setting, warnings are always written to the standard error
#stream when sphinx-build is run.
keep_warnings = False

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'http://docs.python.org/dev': None}

autoclass_content = "both"
