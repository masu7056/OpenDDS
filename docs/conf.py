# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import re
import sys
from pathlib import Path

docs_path = Path(__file__).parent
opendds_root_path = docs_path.parent
ext = (docs_path / 'sphinx_extensions').resolve()
sys.path.append(str(ext))
github_links_root_path = str(opendds_root_path)

from mpc_lexer import MpcLexer
from newsd import parse_newsd
from version_info import VersionInfo

# Custom Values ---------------------------------------------------------------

def setup(app):
    app.add_config_value('is_release', False, True)
    app.add_lexer('mpc', MpcLexer)


# -- Project information -----------------------------------------------------

needs_sphinx = '2.4'
master_doc = 'index'
primary_domain = 'cpp'
pygments_style = 'manni'
nitpicky = True

project = 'OpenDDS'
copyright = '2023, OpenDDS Foundation'
author = 'OpenDDS Foundation'
github_links_repo = 'OpenDDS/OpenDDS'
github_repo = 'https://github.com/' + github_links_repo

# Get Version Info
version_info = VersionInfo()
release = version_info.version
is_release = version_info.is_release
if is_release:
    github_links_release_tag = version_info.tag

# Generate WIP News if this isn't a release
wip_news = 'wip_news.rst'
with (docs_path / wip_news).open('w') as f:
    if is_release:
        print('', file=f)
    else:
        parse_newsd().print_all(file=f)


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # Custom ones
    'links',

    # Official ones
    'sphinx.ext.ifconfig',

    # Other ones
    'sphinx_copybutton',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'history/**',
    'design/**',
    'OpenDDS.docset/**',
    '.venv',
    'sphinx_extensions/**',
    'news.d/**',
    wip_news,
]

source_suffix = {
    '.rst': 'restructuredtext',
}

numfig = True

highlight_language = 'none'

linkcheck_ignore = [
    # Linkcheck fails to work with GitHub anchors
    r'^https?://github\.com/.*#.+$',
    # Returns 403 for some reason
    r'^https?://docs\.github\.com/.*$',
]


# -- Options for HTML output -------------------------------------------------

html_static_path = ['.']

html_theme = 'furo'
# See documentation for the theme here:
#   https://pradyunsg.me/furo/

html_title = project + ' ' + release

html_theme_options = {
    'light_logo': 'logo_with_name.svg',
    'dark_logo': 'logo_with_name.svg',
    'sidebar_hide_name': True, # Logo has the name in it
    # furo doesn't support a veiw source link for some reason, force edit
    # button to do that.
    'source_edit_link': github_repo + '/blob/master/docs/{filename}?plain=1',
}

# Change the sidebar to include fixed links
#   https://pradyunsg.me/furo/customisation/sidebar/#making-changes
sidebar_links = {
    'Main Website': 'https://opendds.org',
    'GitHub Repo': github_repo,
}
our_template_path = ext / 'templates'
sidebar_links_template_name = 'sidebar-links.html'
with (our_template_path / sidebar_links_template_name).open('w') as f:
    print('<div class="sidebar-tree" style="margin-top: 0px;"><ul>', file=f)
    for name, url in sidebar_links.items():
        print('  <li><a class="reference" href="{}">{}</a></li>'.format(url, name), file=f)
    print('</ul></div>', file=f)
templates_path = [str(our_template_path)]
html_sidebars = {
    '**': [
        'sidebar/brand.html',
        sidebar_links_template_name,
        'sidebar/search.html',
        'sidebar/scroll-start.html',
        'sidebar/navigation.html',
        'sidebar/ethical-ads.html',
        'sidebar/scroll-end.html',
        'sidebar/variant-selector.html',
    ]
}

html_favicon = 'logo_32_32.ico'


# -- LaTeX (PDF) output ------------------------------------------------------

latex_logo = 'logo_276_186.png'

# vim: expandtab:ts=4:sw=4
