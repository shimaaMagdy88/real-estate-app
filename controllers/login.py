from odoo import http, fields
from odoo.http import request


# class LoginApi(http.Controller):
#
#     @http.route('/api/login', method=["GET"], type='http', auth="none", csrf=False)
#     def api_login(self, **kwargs):
#         # 1- first way to make dict of kwargs parameters
#         # params = {
#         #     "db": kwargs.get("db"),
#         #     "login": kwargs.get("login"),
#         #     "password": kwargs.get("password")
#         # }
#
#         # 2- second way to make dict of kwargs parameters
#         params = ["db", "login", "password"]
#         params = {key: kwargs.get(key) for key in params if kwargs.get(key)}
#
#         # in case (db, username, password) parameters came from body
#
#         # db, username, password = (kwargs.get("db"), kwargs.get("login"), kwargs.get("password"))
#         db = kwargs.get("db")
#         username = kwargs.get("login")
#         password = kwargs.get("password")
#
#         _credential_includes_in_body = all([db, username, password])
#
#         # => if the request body is empty, the credentials maybe passed via headers
#         if not _credential_includes_in_body:
#
#             headers = request.httprequest.headers()
#             db = headers.get("db")
#             username = headers.get("login")
#             password = headers.get("password")
#
#             _credential_includes_in_header = all([db, username, password])
#
#             if not _credential_includes_in_header:
#                 print('invalid response')
#                 # return invalid_response(
#                 #     "missing error", "either of the following are missing [db, username, password]", 403,
#                 # )


