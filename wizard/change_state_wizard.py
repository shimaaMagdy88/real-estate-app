from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class ChangeState(models.TransientModel):
    _name = 'change.state'

    property_id = fields.Many2one('property', required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('pending', 'Pending')], default='draft')
    reason = fields.Text()

    def action_confirm(self):
        if self.property_id.state == 'closed':
            self.property_id.create_history_record(self.property_id.state, self.state, self.reason)
            self.property_id.state = self.state
        else:
            raise ValidationError(_('Closed State Only Can be Changed To %s' % self.state))


