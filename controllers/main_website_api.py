from odoo import http, fields
from odoo.http import request


class SaleOrderApi(http.Controller):

    @http.route("/sale_order_details", type="http", auth="public", website=True)
    def get_sale_orders(self, **kwargs):
        sale_order_details = request.env['sale.order'].sudo().search([])
        return request.render("app_one.sale_order_template", {'my_details': sale_order_details})

    # make this method for student not sale.order
    @http.route("/new_request_submit", type="http", auth="public", website=True, csrf=True)
    def request_submit(self, **kwargs):
        student = kwargs                   # dict of values (in post method)
        student_name = kwargs.get('name')
        student_id = request.env['school.students'].sudo().create({
            'name': student_name,
            'address': 'London',
        })




    # type => http: render data in another web page, json return data in same method
    # auth => public, users, none


