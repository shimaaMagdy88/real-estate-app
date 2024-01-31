from odoo import api, models, fields

class ChangeState(models.TransientModel):
    _name = 'change.state'

    property_id = fields.Many2one('property')
    state = fields.Selection([('draft', 'Draft'),
                              ('pending', 'Pending')], default='draft')
    reason = fields.Char()
