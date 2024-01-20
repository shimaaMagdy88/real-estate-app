from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Property'

    name = fields.Char(required=True, size=15, tracking=True)
    description = fields.Text(default='New')
    postcode = fields.Char()
    date_availability = fields.Date(tracking=True)
    expected_price = fields.Float(digits=(0, 4))
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff')
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'),
                                           ('south', 'South'),
                                           ('east', 'East'),
                                           ('west', 'West')])
    owner_id = fields.Many2one('owner')
    owner_phone = fields.Char(related='owner_id.phone', readonly=False)
    owner_address = fields.Char(related='owner_id.address', readonly=False)
    tag_ids = fields.Many2many('tag')
    state = fields.Selection([('draft', 'Draft'),
                              ('pending', 'Pending'),
                              ('sold', 'Sold'),
                              ('cancel', 'Cancel')], default='draft')
    property_line_ids = fields.One2many('property.line', 'property_id')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'this name is exist!')
    ]

    @api.constrains('bedrooms')
    def check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms <= 0:
                raise ValidationError(_('bedrooms must be greater than 0'))

    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        print('inside create method')
        return res

    def write(self, vals):
        res = super(Property, self).write(vals)
        print('inside write method')
        return res
    
    def unlink(self):
        res = super(Property, self).unlink()
        print('inside unlink method')

    def action_draft(self):
        for rec in self:
            self.state = 'draft'

    def action_pending(self):
        for rec in self:
            self.state = 'pending'

    def action_sold(self):
        for rec in self:
            self.state = 'sold'

    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price
            print('diff dependancy')

    # @api.model
    # def _sendone(self, channel, notification_type, message):
    #     self._sendmany([[channel, notification_type, message]])

    @api.onchange('description')
    def onchange_description(self):
        for rec in self:
            print('inside onchange description')
            return {
                'warning': {'type': 'notification', 'title': 'warning', 'message': 'description has been changed'}
            }

            # self.env['property']._sendone(self.env.user.partner_id, 'simple_notification', {
            #     'title': _('Missing Library'),
            #     'message': 'how are you',
            #     'sticky': True,
            #     'warning': True,
            # })


class PropertyLine(models.Model):
    _name = 'property.line'

    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one('property')
