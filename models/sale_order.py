from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    property_id = fields.Many2one('property')

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        print('hello from inheriting action_confirm method')
        return res

    # @api.model
    # def create(self, vals):
    #     result = super(SaleOrder, self).create(vals)
    #     result.name = result.name + ' (draft)'
    #     return result

