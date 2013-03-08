import os
from django.conf import settings


class Repository(object):
    def __init__(self, name):
        self.name = name
        self.path = os.path.join(
            settings.SALAWEB_DATADIR,
            'repositories',
            name,
        )

    def exists(self):
        return os.path.isdir(self.path)

    def as_html(self):
        def walk(start, depth=0):
            for node in sorted(os.listdir(start)):
                fullpath = os.path.join(start, node)
                if os.path.isdir(fullpath):
                    yield '<div class="dir depth%d">' % depth

                    # me wants yield from :(
                    for fragment in walk(fullpath, depth + 1):
                        yield fragment

                    yield '</div>'

                else:
                    yield '<div class="file depth%d">' % depth
                    yield cgi.escape(node)
                    yield '</div>'
