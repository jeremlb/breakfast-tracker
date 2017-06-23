from __future__ import absolute_import

app = None

def init_app(appli):
    global app

    app = appli

    from .index import *
    from .notification import *