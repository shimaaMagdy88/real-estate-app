from odoo import api, fields, models


class Building(models.Model):
    _name = 'building'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Building'
    # _rec_name = 'code'

    no = fields.Integer()
    code = fields.Char()
    description = fields.Text()
    name = fields.Char()
    active = fields.Boolean(default=True)
