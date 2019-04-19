import torndb
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import os.path
import os
from binascii import hexlify
import datetime


define("port", default=1104, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="tickets", help="database name")
define("mysql_user", default="ellie", help="database user")
define("mysql_password", default="ellie", help="database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/signup", signup),
             (r"/login", login),
            (r"/logout", logout),
            (r"/sendticket", sendticket),
            (r"/getticketcli", getticketcli),
            (r"/closeticket", closeticket),
            (r"/getticketmod", getticketmod),
            (r"/restoticketmod", restoticketmod),
            (r"/changestatus", changestatus),
            (r"/signup/([^/]+)/([^/]+)/([^/]+)/([^/]+)", signup),
            (r"/login", login),
            (r"/logout", logout),
            (r"/sendticket", sendticket),
            (r"/getticketcli", getticketcli),
            (r"/closeticket", closeticket),
            (r"/getticketmod", getticketmod),
            (r"/restoticketmod", restoticketmod),
            (r"/changestatus", changestatus),



            (r".*", DefaultHandler),
        ]
        settings = dict()
        super(Application, self).__init__(handlers, **settings)
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def user_exists(self, user):
        result = self.db.get("SELECT * from users where username = %s", user)
        if result:
            return True
        else:
            return False

    def check_api(self, api):
        result = self.db.get("SELECT * from users where token = %s", api)
        if result:
            return True
        else:
            return False

    def check_auth(self, username, password):
        result = self.db.get("SELECT * from users where username = %s and password = %s", username, password)
        if result:
            return True
        else:
            return False

    def check_status(self, ticket):
        if ticket.status == 0:
            return 'open'
        if ticket.status == 1:
            return 'close'
        if ticket.status == 2:
            return 'in progress'

    def to_status(self, t):
        if t == 'open':
            return 0
        if t == 'close':
            return 1
        if t == 'in progress':
            return 2


class DefaultHandler(BaseHandler):
    def get(self):
        output="Bad Request"
        self.write(output)

    def post(self):
        output="Bad Request"
        self.write(output)


class signup(BaseHandler):
    def get(self, *args):
        username = self.get_argument('username')
        password = self.get_argument('password')
        frstnme = self.get_argument('firstname')
        lstnme = self.get_argument('lastname')
        if not self.user_exists(username):
            api_token = str(hexlify(os.urandom(16)))
            user_id = self.db.execute("INSERT INTO users (username, password, firstname, lastname, token) "
                                      "values (%s,%s,%s,%s,%s) "
                                      , username, password, frstnme, lstnme, api_token)

            output = {'message': 'Signed up successfully',
                      'code': '200'}
            self.write(output)
        else:
            output = {'status': 'User Exists',
                      'code': '409'}
            self.write(output)

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        frstnme = self.get_argument('firstname', None)
        lstnme = self.get_argument('lastname', None)
        if not self.user_exists(username):
            api_token = str(hexlify(os.urandom(16)))
            user_id = self.db.execute("INSERT INTO users (username, password, firstname, lastname, token) "
                                      "values (%s,%s,%s,%s,%s) "
                                      , username, password, frstnme, lstnme, api_token)

            output = {'message': 'Signed up successfully',
                      'code': '200'}
            self.write(output)
        else:
            output = {'status': 'User Exists',
                      'code': '409'}
            self.write(output)


class login(BaseHandler):
    def get(self, *args):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if self.check_auth(username, password):
            api_token = self.db.get("SELECT token from users where username = %s and password = %s", username, password)
            ['token']
            output = {'message': 'Logged in successfully',
                      'code': '200',
                      'token': api_token}
            self.write(output)
        else:
            output = {'status': 'User not found',
                      'code': '404'}
            self.write(output)

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if self.check_auth(username, password):
            api_token = self.db.get("SELECT token from users where username = %s and password = %s", username, password)
            ['token']
            output = {'message': 'Logged in successfully',
                      'code': '200',
                      'token': api_token}
            self.write(output)
        else:
            output = {'status': 'User not found',
                      'code': '404'}
            self.write(output)


class logout(BaseHandler):
    def get(self, *args):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if self.check_auth(username, password):
            api_token = str(hexlify(os.urandom(16)))
            self.db.execute("update users set token=%s where username=%s and password = %s", api_token, username, password)
            output = {'message': 'Logged out successfully',
                      'code': '200'}
            self.write(output)
        else:
            output = {'status': 'User not found',
                      'code': '404'}
            self.write(output)

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if self.check_auth(username, password):
            api_token = str(hexlify(os.urandom(16)))
            self.db.execute("update users set token=%s where username=%s and password = %s", api_token, username,
                            password)
            output = {'message': 'Logged out successfully',
                      'code': '200'}
            self.write(output)
        else:
            output = {'status': 'User not found',
                      'code': '404'}
            self.write(output)


class sendticket(BaseHandler):
    def post(self):
        token = self.get_argument('token')
        subject = self.get_argument('subject')
        body = self.get_argument('body')
        if self.check_api(token):
            origin = int(self.db.get("SELECT ID from users where token = %s ", token)['ID'])
            dt = datetime.datetime.now()
            idid = self.db.execute("INSERT INTO alltickets (subject, body, origin, status, date) "
                                   "values (%s,%s,%s ,%s,%s) ", subject, body, origin, 0,
                                   dt.strftime("%Y-%m-%d %H:%M:%S"))
            output = {'message': 'Ticket sent successfully',
                      'id': idid,
                      'code': '200',
                      }
            self.write(output)
        else:
            output = {'message': 'Invalid token',
                      'code': '401',
                      }
            self.write(output)

    def get(self):
        token = self.get_argument('token')
        subject = self.get_argument('subject')
        body = self.get_argument('body')
        if self.check_api(token):
            origin = int(self.db.get("SELECT ID from users where token = %s ", token)['ID'])
            dt = datetime.datetime.now()
            idid = self.db.execute("INSERT INTO alltickets (subject, body, origin, status, date) " 
                                   "values (%s,%s,%s ,%s,%s) ", subject, body, origin, 0,
                                   dt.strftime("%Y-%m-%d %H:%M:%S"))
            output = {'message': 'Ticket sent successfully',
                      'id': idid,
                      'code': '200',
                      }
            self.write(output)
        else:
            output = {'message': 'Invalid token',
                      'code': '401',
                      }
            self.write(output)



class getticketcli(BaseHandler):
    def post(self):
        token = self.get_argument('token')
        role = self.db.get("SELECT role from users where token = %s", token)['role']
        if self.check_api(token)and role==0 :
            idd = self.db.get("SELECT ID from users where token = %s", token)['ID']
            result = self.db.query("SELECT * from alltickets where origin = %s", idd)
            numofrec = len(result)

            output = {'tickets': "There are -" + str(numofrec) + "-tickets",
                      'code': '200',
                      }
            n = 0
            for r in result:
                s = self.check_status(r)
                part = {'subject': r.subject,
                        'body': r.body,
                        'response': r.response,
                        'status': s,
                        'ID': r.ID,
                        'date': str(r.date),
                        }
                output['block' + str(n)] = part
                n += 1

            self.write(output)

        else:
            output = {'message': 'User not found',
                      'code': '404'}
            self.write(output)

    def get(self, *args, **kwargs):
        token = self.get_argument('token')
        role = self.db.get("SELECT role from users where token = %s", token)['role']
        if self.check_api(token) and role==0:
            idd = self.db.get("SELECT ID from users where token = %s", token)['ID']
            result = self.db.query("SELECT * from alltickets where origin = %s", idd)
            numofrec = len(result)

            output = {'tickets': "There are -"+str(numofrec)+"-tickets",
                      'code': '200',
                    }
            n = 0
            for r in result:
                s = self.check_status(r)
                part = {'subject': r.subject,
                        'body': r.body,
                        'response': r.response,
                        'status': s,
                        'ID': r.ID,
                        'date': str(r.date),
                        }
                output['block'+str(n)] = part
                n+=1

            self.write(output)

        else:
            output = {'message': 'User not found',
                      'code': '404'}
            self.write(output)


class getticketmod(BaseHandler):
    def post(self):
        token = self.get_argument('token')
        role = self.db.get("SELECT role from users where token = %s", token)['role']
        if self.check_api(token) and role == 1:
            idd = self.db.get("SELECT ID from users where token = %s", token)['ID']
            result = self.db.query("SELECT * from alltickets")
            numofrec = len(result)

            output = {'tickets': "There are -" + str(numofrec) + "-tickets",
                      'code': '200',
                      }
            n = 0
            for r in result:
                s = self.check_status(r)
                part = {' subject': r.subject,
                        'body': r.body,
                        'response': r.response,
                        'status': s,
                        'ID': r.ID,
                        'date': str(r.date),
                        }
                output['block' + str(n)] = part
                n += 1

            self.write(output)

        else:
            output = {'message': "Not Enough Permissions",
                      'code': '401',
                      }
            self.write(output)

    def get(self, *args, **kwargs):
        token = self.get_argument('token')
        role = self.db.get("SELECT role from users where token = %s", token)['role']
        if self.check_api(token) and role == 1:
            result = self.db.query("SELECT * from alltickets ")
            numofrec = len(result)

            output = {'tickets': "There are -" + str(numofrec) + "-tickets",
                      'code': '200',
                      }
            n = 0
            for r in result:
                s = self.check_status(r)
                part = {' subject': r.subject,
                        'body': r.body,
                        'response': r.response,
                        'status': s,
                        'ID': r.ID,
                        'date': str(r.date),
                        }
                output['block' + str(n)] = part
                n += 1

            self.write(output)

        else:
            output = {'message': "Not Enough Permissions",
                      'code': '401',
                      }
            self.write(output)


class closeticket(BaseHandler):
    def post(self, *args, **kwargs):
        token = self.get_argument('token')
        ticket_id = self.get_argument('id')
        role = self.db.get("SELECT role from users where token = %s", token)['role']
        if self.check_api(token) and role == 0:
            idd = self.db.get("SELECT ID from users where token = %s", token)['ID']
            result = self.db.execute("update alltickets set status=%s where origin=%s and ID=%s ", 1, idd, ticket_id,)

            output = {'message': 'Ticket with ID-' + str(ticket_id) + '-closed successfully',
                      'code': '200',
                      }

            self.write(output)
        else:
            output = {'message': 'Not Enough Permissions',
                      'code': '401',
                      }
            self.write(output)

    def get(self, *args, **kwargs):
        token = self.get_argument('token')
        ticket_id = self.get_argument('id')
        role = self.db.get("SELECT role from users where token = %s", token)['role']
        if self.check_api(token) and role == 0:
            idd = self.db.get("SELECT ID from users where token = %s", token)['ID']
            result = self.db.execute("update alltickets set status=%s where origin=%s and ID=%s ", 1, idd, ticket_id, )

            output = {'message': 'Ticket with ID-' + str(ticket_id) + '-closed successfully',
                      'code': '200',
                      }

            self.write(output)
        else:
            output = {'message': "Not Enough Permissions",
                      'code': '401',
                      }
            self.write(output)


class restoticketmod(BaseHandler):
    def post(self, *args, **kwargs):
        token = self.get_argument('token')
        ticket_id = self.get_argument('id')
        body = self.get_argument('body')

        role = self.db.get("SELECT role from users where token = %s", token)['role']
        if self.check_api(token) and role == 1:
            self.db.execute("update alltickets set response=%s where  ID=%s ", body, ticket_id, )
            self.db.execute("update alltickets set status=%s where  ID=%s ", 1, ticket_id, )

            output = {'message': 'Response to ticket with ID-' + str(ticket_id) + '-sent successfully',
                      'code': '200',
                      }

            self.write(output)
        else:
            output = {'message': 'Not Enough Permissions',
                      'code': '401',
                      }
            self.write(output)

    def get(self, *args, **kwargs):
        token = self.get_argument('token')
        ticket_id = self.get_argument('id')
        body = self.get_argument('body')

        role = self.db.get("SELECT role from users where token = %s", token)['role']
        if self.check_api(token) and role == 1:
            result = self.db.execute("update alltickets set response=%s where  ID=%s ", body, ticket_id, )

            output = {'message': 'Response to ticket with ID-' + str(ticket_id) + '-sent successfully',
                      'code': '200',
                      }

            self.write(output)
        else:
            output = {'message': 'Not Enough Permissions',
                      'code': '401',
                      }
            self.write(output)


class changestatus(BaseHandler):
    def post(self, *args, **kwargs):
        token = self.get_argument('token')
        ticket_id = self.get_argument('id')
        status = self.get_argument('status')
        sta = self.to_status(status)

        role = self.db.get("SELECT role from users where token = %s", token)['role']
        if self.check_api(token) and role == 1:
            self.db.execute("update alltickets set status=%s where  ID=%s ", sta, ticket_id, )
            output = {'message': 'Ticket with ID-' + str(ticket_id) + 'changed successfully',
                      'code': '200',
                      }

            self.write(output)
        else:
            output = {'message': 'Not Enough Permissions',
                      'code': '401',
                      }
            self.write(output)

    def get(self, *args, **kwargs):
        token = self.get_argument('token')
        ticket_id = self.get_argument('id')
        status = self.get_argument('status')
        sta = self.to_status(status)

        role = self.db.get("SELECT role from users where token = %s", token)['role']
        if self.check_api(token) and role == 1:
            self.db.execute("update alltickets set status=%s where  ID=%s ", sta, ticket_id, )
            output = {'message': 'Ticket with ID-' + str(ticket_id) + '-changed successfully',
                      'code': '200',
                      }

            self.write(output)
        else:
            output = {'message': 'NotEnough Permissions',
                      'code': '401',
                      }
            self.write(output)


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
