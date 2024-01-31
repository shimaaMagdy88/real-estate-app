from odoo import fields, api, models


class Owner(models.Model):
    _name = 'owner'

    name = fields.Char()
    user_id = fields.Many2one('res.users', string='Sales Person')
    phone = fields.Char(string='Phone')
    address = fields.Char(string='Address')
    property_ids = fields.One2many('property', 'owner_id')



    @api.model
    def create(self, vals):
        if not self.address:
            vals['address'] = 'egypt'
        return super(Owner, self).create(vals)
