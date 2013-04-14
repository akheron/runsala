import cgi
import os
import urllib

from django.conf import settings


class Repository(object):
    def __init__(self, name):
        self.name = name
        self.path = os.path.join(
            settings.RUNSALA_DATADIR,
            'repositories',
            name,
        )

    def exists(self):
        return os.path.isdir(self.path)

    def as_html(self):
        def walk(start, depth=0):
            for node in sorted(os.listdir(start)):
                if node.startswith('.'):
                    continue

                path = os.path.join(start, node)
                if os.path.isdir(path):
                    yield '<div class="dir depth%d">' % depth
                    yield '<div>%s</div>' % cgi.escape(node)

                    # me wants yield from :(
                    for fragment in walk(path, depth + 1):
                        yield fragment

                    yield '</div>'

                else:
                    yield '<div class="file depth%d">' % depth
                    yield '<a href="%s">%s</a>' % (
                        cgi.escape(urllib.quote(os.path.join(
                            self.name,
                            os.path.relpath(path, self.path),
                        ))),
                        cgi.escape(node),
                    )
                    yield '</div>'

        return ''.join(walk(self.path))
