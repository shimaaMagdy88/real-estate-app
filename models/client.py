from odoo import models, fields, api


class Client(models.Model):
    _name = 'client'
    _inherit = 'owner'


