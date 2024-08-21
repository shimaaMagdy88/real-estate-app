import math

from odoo import http
from odoo.http import request, Response
import json
from urllib.parse import parse_qs


def valid_response(property_data, pagination_info: 1, status):  # method for handling response structure (http response)
    response_body = {
        'Page Info': pagination_info if pagination_info else {'no info'},
        'result': property_data,
        'message': 'success'
    }
    return Response(json.dumps(response_body), content_type='application/json', status=status)


def invalid_response(message, status):
    response_body = {
        'result': message,
        'message': 'failed'
    }
    return Response(json.dumps(response_body), content_type='application/json', status=status)


class PropertyApi(http.Controller):

    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        print('inside post_property method')
        args = request.httprequest.data.decode()
        vals = json.loads(args)

        try:
            # property_id = request.env['property'].sudo().create(vals)                # using ORM methods
            cr = request.env.cr
            columns = ", ".join(vals.keys())
            values = ", ".join(['%s'] * len(vals))       # %s, %s, %s, %s
            query = f"""insert into property ({columns}) values ({values}) returning id, name"""
            cr.execute(query, tuple(vals.values()))                                    # using SQL queries
            result = cr.fetchone()
            response = {
                    'message': 'created successfully',
                    'id is': result[0],
                    'name': result[1]
                }
            return valid_response(property_data=response, pagination_info=1, status=200)

        except Exception as error:
            return invalid_response(f'{error}', 400)

    @http.route("/v1/property/json", methods=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        print('inside post_property using json method')
        args = request.httprequest.data.decode()
        vals = json.loads(args)

        if not vals.get('name'):
            return {
                'message': 'Name is required!',
            }

        try:
            property_id = request.env['property'].sudo().create(vals)
            if property_id:
                return {  # we can return here dict, list, just a msg or anything
                    'message': 'created successfully',
                    'id is': property_id.id
                }

        except Exception as error:
            return {
                'message': error
            }

    @http.route("/v1/property/update/<int:property_id>", methods=["PUT"], type="json", auth="none", csrf=False)
    def update_property(self, property_id):
        print('inside update property')

        try:
            property_id = request.env['property'].search([('id', '=', property_id)])
            posted_data = request.httprequest.data.decode()
            vals = json.loads(posted_data)

            if not property_id:
                return({
                    'message': 'property id not exist!'
                })

            property_id.write(vals)
            return {
                'message': 'the property has been updated successfully',
                'id': property_id.id,
                'name': property_id.name
            }
        except Exception as error:
            return {
                'error': error
            }

    @http.route("/v1/property/get/<int:property_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property(self, property_id):
        print('inside get property')
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])

            if not property_id:
                # return Response("Property ID Doesn't Exist !", content_type='application/json', status=400)
                message = "The Property ID Doesn't Exist !"
                return invalid_response(message, 400)

            property_data = {
                "property_id": property_id.id,
                "property_name": property_id.name,
                "bedrooms": property_id.bedrooms,
                "description": property_id.description
            }
            # return Response(json.dumps(property_data), content_type='application/json', status=200)
            return valid_response(property_data, 1, 200)

        except Exception as error:
            return invalid_response(f'{error}', 400)

        # note 1 => we can use type='http' and use json in postman (but sometimes not working)
        # note 2 => we can use Response method to return data, but should take json to work correctly

    @http.route("/v1/property/get_all", methods=["GET"], type='http', auth="none", csrf=False)
    def get_all_properties(self):
        print('inside get all properties')
        try:
            properties = request.env['property'].search([])

            if not properties:
                return invalid_response("There is no properties", 400)

            data = [{
                    'id': propertyy.id,
                    "name": propertyy.name,
                } for propertyy in properties]

            return valid_response(data, 1, status=200)
        except Exception as e:
            return Response(e)


    @http.route("/v1/property/delete/<int:property_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_property(self, property_id):
        print('inside delete property')
        try:
            property_id = request.env['property'].search([('id', '=', property_id)])
            if not property_id:
                return Response('Message: This Property ID Doesn\'t Exist !')

            property_id.sudo().unlink()
            return Response("The Property Has Been Deleted Successfully !")

        except Exception as error:
            return Response(f'Error: {error}')

    @http.route('/v1/property/get_some', methods=['GET'], type='http', auth='none', csfr=False)
    def get_some_properties(self):                # to get list of records with filtration
        print('inside get some properties')

        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            domain = []
            my_offset = 0
            my_limit = 5
            my_page = 1
            if params.get('limit'):
                my_limit = int(params.get('limit')[0])
            if params.get('page'):
                my_page = int(params.get('page')[0])
                my_offset = my_limit * (my_page - 1)

            if params.get('state') and params.get('id'):
                domain = [('state', '=', params.get('state')[0]), ('id', '=', int(params.get('id')[0]))]
                property_ids = request.env['property'].sudo().search(domain)
            elif params.get('state'):
                domain = [('state', '=', params.get('state')[0])]
                property_count = request.env['property'].sudo().search_count(domain)
                property_ids = request.env['property'].sudo().search(domain, offset=my_offset, limit=my_limit, order='id asc')
            elif params.get('id'):
                domain = [('id', '=', int(params.get('id')[0]))]
                property_ids = request.env['property'].sudo().search([('id', '=', int(params.get('id')[0]))])
            else:
                property_ids = request.env['property'].sudo().search([])

            if not property_ids:
                message = 'There are no properties'
                return invalid_response(message, 400)
            data = [
                {
                    "property id": property_id.id,
                    "name": property_id.name,
                    "description": property_id.description,
                    'state': property_id.state
                } for property_id in property_ids
            ]
            return valid_response(property_data=data, pagination_info={
                'page': my_page if my_page else 1,
                'limit': my_limit,
                'pages': math.ceil(property_count/my_limit)}, status=200)

        except Exception as error:
            return {
                "Message": error
            }

         # to make pagination => offset=4, limit=2, order='id asc'
         # means skip first 4 records, get just 2 records and order ascending with id






