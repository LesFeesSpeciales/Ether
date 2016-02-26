# Copyright Les Fees Speciales 2015
#
# voeu@les-fees-speciales.coop
#
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import os
import datetime

import tornado.ioloop
import tornado.web

# Config is a python file containing useful objects
import nid_config as config

# Load services and provide config if needed
import services.ouvreuse.ouvreuse as ouvreuse


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    def get(self):
        self.write("Hello la ruche %s" % self.current_user)


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/")


class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler),
                    (r"/login", LoginHandler),
                    (r"/logout", LogoutHandler)]

        handlers.extend(ouvreuse.handlers)

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret=config.COOKIE_SECRET,
            debug=config.DEBUG,
            login_url=config.LOGIN_URL

        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    print("\nStarting %s" % __file__)
    print("Server starting on port %i" % config.PORT)
    print(str(datetime.datetime.now()))
    if config.DEBUG:
        print("Debug ON")

    app = Application()
    app.listen(config.PORT)

    main_loop = tornado.ioloop.IOLoop.instance()

    # Start main loop
    main_loop.start()
