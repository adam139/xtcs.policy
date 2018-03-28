# -*- coding: utf-8 -*-

message = """<html>
<body>
<p>%(from)s</p>

%(message)s

<hr/>
<p><a href="%(url)s">%(url_text)s</a></p>
</body>
</html>
"""
# dummy i18n helper for workflow states
#from zope.i18nmessageid import MessageFactory
from Products.CMFPlone import PloneMessageFactory as _p
#_p = MessageFactory('plone')
dummy = _p("published")
dummy = _p("draft")
dummy = _p("pendingsponsor")
dummy = _p("pendingagent")
dummy = _p("Agree")
dummy = _p("Veto")
dummy = _p("Pending sponsor review")

