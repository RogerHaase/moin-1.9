# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - common functions for notification framework

    Code for building messages informing about events (changes)
    happening in the wiki.

    @copyright: 2007 by Karol Nowak <grywacz@gmail.com>
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin import user, wikiutil
from MoinMoin.Page import Page


def page_changed_notification(request, page, comment, lang, revisions, trivial):
    """ Prepare a notification text for a single language

    @param comment: editor's comment given when saving the page
    @param lang: language of notifications
    @param revisions: revisions of this page (newest first!)
    @param trivial: the change is marked as trivial
    @rtype: int
    @return: composed string message
    """
    _ = request.getText
    page._ = lambda s, formatted=True, r=request, l=lang: r.getText(s, formatted=formatted, lang=l)

    if len(revisions) >= 2:
        querystr = {'action': 'diff',
                    'rev2': str(revisions[0]),
                    'rev1': str(revisions[1])}
    else:
        querystr = {}
        
    pagelink = request.getQualifiedURL(page.url(request, querystr, relative=False))

    messageBody = _("Dear Wiki user,\n\n"
        'You have subscribed to a wiki page or wiki category on "%(sitename)s" for change notification.\n\n'
        "The following page has been changed by %(editor)s:\n"
        "%(pagelink)s\n\n", formatted=False) % {
            'editor': page.uid_override or user.getUserIdentification(request),
            'pagelink': pagelink,
            'sitename': page.cfg.sitename or request.getBaseURL(),
    }

    if comment:
        messageBody = messageBody + \
            _("The comment on the change is:\n%(comment)s\n\n", formatted=False) % {'comment': comment}

    # append a diff (or append full page text if there is no diff)
    if len(revisions) < 2:
        messageBody = messageBody + \
            _("New page:\n", formatted=False) + \
            page.get_raw_body()
    else:
        lines = wikiutil.pagediff(request, page.page_name, revisions[1],
                                  page.page_name, revisions[0])
        if lines:
            messageBody = messageBody + "%s\n%s\n" % (("-" * 78), '\n'.join(lines))
        else:
            messageBody = messageBody + _("No differences found!\n", formatted=False)
            
    return messageBody
