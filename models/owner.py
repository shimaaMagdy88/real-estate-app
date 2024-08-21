from odoo import fields, api, models


class Owner(models.Model):
    _name = 'owner'
    _inherit = ['mail.thread']

    name = fields.Char()
    user_id = fields.Many2one('res.users', string='Sales Person')
    phone = fields.Char(string='Phone')
    address = fields.Char(string='Address')
    property_ids = fields.One2many('property', 'owner_id')
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')])



    @api.model
    def create(self, vals):
        if not self.address:
            vals['address'] = 'egypt'
        return super(Owner, self).create(vals)

    def action_test(self):
        partners = self.env['res.partner'].search([('id', '=', self.user_id.partner_id.id)])

        self.message_post(body="Great Job Today ss", partner_ids=partners.ids)
