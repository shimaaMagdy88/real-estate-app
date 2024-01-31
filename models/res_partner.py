from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_id = fields.Many2one('property')
    price = fields.Float(related='property_id.selling_price')
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)


