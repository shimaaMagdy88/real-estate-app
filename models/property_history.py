from odoo import models, fields, api


class PropertyHistory(models.Model):
    _name = 'property.history'
    _description = 'Property History'

    user_id = fields.Many2one('res.users')
    property_id = fields.Many2one('property')
    old_state = fields.Char()
    new_state = fields.Char()
    reason = fields.Text()
    property_history_line_ids = fields.One2many('property.history.line', 'property_history_id')
    # property_history_line_ids = fields.One2many('property.line', 'property_history_id', related='property_id.property_line_ids')


class PropertyHistoryLine(models.Model):
    _name = 'property.history.line'
    _description = 'Property History Line'

    description = fields.Char()
    area = fields.Float()
    property_history_id = fields.Many2one('property.history')
