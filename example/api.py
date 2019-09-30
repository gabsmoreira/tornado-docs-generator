import tornado.ioloop
import tornado.web

class Client(tornado.web.RequestHandler):
    """
    /client
    """
    def post(self):
        """
        @Description
            Client creation route
        @Response
            200:
                name - string.
                age - int.
            401:
                message - hehehehe.
        @Parameters
            Header: Authorization - token.
                    Content-Type - application/json.
            Path: id - client id from db.

        """
        pass

    def get(self):
        """
        @Description
            Client creation route
        @Parameters
            Header: Authorization - token.
                    Content-Type - application/json.
            Path: id - client id from db.
            Body: file: ./schemas/client.json
        @Response
            200:
                name - string.
                age - int.
            401:
                message - hehehehe.

        """
        pass
    
    def patch(self):
        pass

    def delete(self):
        pass
    

class ChangePassword(tornado.web.RequestHandler):
    def post(self):
        pass


def make_app():
    return tornado.web.Application([
        (r"/client", Client),
        (r"/client/changePassword", ChangePasswordHelper),
        
    ],default_handler_class=BaseGatewayHandler)


if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()

