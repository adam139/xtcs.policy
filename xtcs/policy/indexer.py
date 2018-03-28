from plone.indexer.decorator import indexer
from Products.ZCatalog.interfaces import IZCatalog
from plone.app.contenttypes.interfaces import IDocument



#disable Document text field indexer
@indexer(IDocument)
def indexer_text(obj, **kw):
    return ""

