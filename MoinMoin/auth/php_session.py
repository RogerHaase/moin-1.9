# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - PHP session cookie authentication
    
    Currently supported systems:

        * eGroupware 1.2 ("egw")
         * You need to configure eGroupware in the "header setup" to use
           "php sessions plus restore"

    @copyright: 2005 MoinMoin:AlexanderSchremmer (Thanks to Spreadshirt)
    @license: GNU GPL, see COPYING for details.
"""

import Cookie, urllib
from MoinMoin import user
from MoinMoin.auth import _PHPsessionParser

class php_session:
    """ PHP session cookie authentication """
    def __init__(self, apps=['egw'], s_path="/tmp", s_prefix="sess_"):
        """ @param apps: A list of the enabled applications. See above for
            possible keys.
            @param s_path: The path where the PHP sessions are stored.
            @param s_prefix: The prefix of the session files.
        """

        self.s_path = s_path
        self.s_prefix = s_prefix
        self.apps = apps

    def __call__(self, request, **kw):
        def handle_egroupware(session):
            """ Extracts name, fullname and email from the session. """
            username = session['egw_session']['session_lid'].split("@", 1)[0]
            known_accounts = session['egw_info_cache']['accounts']['cache']['account_data']

            # if the next line breaks, then the cache was not filled with the current
            # user information
            user_info = [value for key, value in known_accounts.items()
                         if value['account_lid'] == username][0]
            name = user_info.get('fullname', '')
            email = user_info.get('email', '')

            dec = lambda x: x and x.decode("iso-8859-1")

            return dec(username), dec(email), dec(name)

        user_obj = kw.get('user_obj')
        cookie = kw.get('cookie')
        if not cookie is None:
            for cookiename in cookie:
                cookievalue = urllib.unquote(cookie[cookiename].value).decode('iso-8859-1')
                session = _PHPsessionParser.loadSession(cookievalue, path=self.s_path, prefix=self.s_prefix)
                if session:
                    if "egw" in self.apps and session.get('egw_session', None):
                        username, email, name = handle_egroupware(session)
                        break
            else:
                return user_obj, True

            user = user.User(request, name=username, auth_username=username)

            changed = False
            if name != user.aliasname:
                user.aliasname = name
                changed = True
            if email != user.email:
                user.email = email
                changed = True

            if user:
                user.create_or_update(changed)
            if user and user.valid:
                return user, True # True to get other methods called, too
        return user_obj, True # continue with next method in auth list
