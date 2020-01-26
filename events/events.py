import tornado.ioloop, tornado.web
from pymongo import MongoClient

connection = MongoClient("mongodb://eventmajor:morefun@ds161471.mlab.com:61471/events_server")
database = connection['events_server']
events_collection = database['events']
users_collection = database['users']

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        username = self.get_secure_cookie("login")
        spiderman = events_collection.find_one({'id': 1})
        spiderman_ = spiderman["name"]
        thor = events_collection.find_one({'id': 2})
        thor_ = thor["name"]
        avengers = events_collection.find_one({'id': 3})
        avengers_ = avengers["name"]
        self.render('eventslist.html', username=username, spiderman=spiderman_, thor=thor_, avengers=avengers_)

class RegHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("reg.html")
    def post(self):
        name = self.get_argument("name")
        email = self.get_argument("email")
        password = self.get_argument("password")
        flag = True
        user_find = list(users_collection.find())
        if user_find != []:
            length = len(user_find)
        else:
            length = 0
        if length > 0:
            i = 0
            while flag and i < length:
                if email == user_find[i]["email"]:
                    flag = False
                i += 1

        if flag:
            users_collection.save({"name": name, "email": email, "password": password})
            self.redirect('/')
        else:
            self.write("This email is already used.")

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")
    def post(self):
        email = self.get_argument("email")
        password = self.get_argument("password")
        try:
            db_user = dict(users_collection.find_one({'email': email}))
            if password != db_user["password"]:
                self.write("Wrong password.")
            else:
                self.set_secure_cookie("login", email)
                self.redirect("/")
        except Exception as e:
            self.write("Wrong login.")

class ExitHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("login")
        self.redirect("/")

class EventHandler(tornado.web.RequestHandler):
    def get(self):
        event_id = self.get_argument("id")
        event = events_collection.find_one({'id': int(event_id)})
        username = self.get_secure_cookie("login")
        igo = self.get_cookie("igo")

        if event["visitors"] == []:
            visitors = "Nobody signed up yet."
        else:
            visitors = str(len(event["visitors"])) + " people."

        self.render('event.html', event=event, visitors=visitors, username=username, igo=igo)

class IgoHandler(tornado.web.RequestHandler):
    def get(self):
        new_visitor = str(self.get_secure_cookie("login"))
        new_visitor = users_collection.find_one({"email": new_visitor[2:-1]})
        new_visitor = new_visitor["name"]
        event_id = self.get_argument("id")
        event = events_collection.find_one({"id": int(event_id)})
        event["visitors"].append(new_visitor)
        events_collection.update({"id": int(event_id)}, event)
        self.set_cookie("igo", "igo")
        self.redirect("/event?id={0}".format(event_id))

class IdontgoHandler(tornado.web.RequestHandler):
    def get(self):
        event_id = self.get_argument("id")
        self.clear_cookie("igo")
        event = events_collection.find_one({"id": int(event_id)})
        visitor = str(self.get_secure_cookie("login"))
        visitor = users_collection.find_one({"email": visitor[2:-1]})
        visitor = visitor["name"]
        event["visitors"].remove(visitor)
        events_collection.update({"id": int(event_id)}, event)
        self.redirect("/event?id={0}".format(event_id))

routes = [
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/register", RegHandler),
    (r"/exit", ExitHandler),
    (r"/event", EventHandler),
    (r"/igo", IgoHandler),
    (r"/idontgo", IdontgoHandler),
]
app = tornado.web.Application(routes, debug=True, cookie_secret="myCookieSecret")
app.listen(8888)
tornado.ioloop.IOLoop.current().start()[[]]
