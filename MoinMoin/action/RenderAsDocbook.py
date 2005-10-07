"""
    MoinMoin - Render as DocBook action - redirects to the DocBook formatter

    @copyright: 2005 MoinMoin:AlexanderSchremmer
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.Page import Page
from MoinMoin.util import MoinMoinNoFooter

def execute(pagename, request):
    url = Page(request, pagename).url(request, {'action': 'format',
                                                'mimetype': 'xml/docbook'}, 0)
    request.http_redirect(url)
    raise MoinMoinNoFooter