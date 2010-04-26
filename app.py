from pymongo import Connection
import web
from web.contrib.template import render_jinja


#connection = Connection()

#db = connection.test

#db.foo.insert(foo)
#print(db.foo.find_one())

urls = (
    '/(.*)', 'Index' 
)

app = web.application(urls, globals())

render = render_jinja(
        'templates',   # Set template directory.
        encoding = 'utf-8',                         # Encoding.
    )


class Index:
    def GET(self, name):        
        return render.index()

if __name__ == '__main__':
    app.run()


app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
