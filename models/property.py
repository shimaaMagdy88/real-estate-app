from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class Property(models.Model):
    _name = 'property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Property'

    name = fields.Char(required=True, size=15, tracking=True)
    description = fields.Text(default='New')
    postcode = fields.Char()
    date_availability = fields.Date(tracking=True)
    date_expected_selling = fields.Date(tracking=True)
    is_late = fields.Boolean()
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
                              ('closed', 'Closed')], default='draft')
    property_line_ids = fields.One2many('property.line', 'property_id')
    active = fields.Boolean(default=True)

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
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'

    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price
            print('diff dependancy')

    @api.onchange('description')
    def onchange_description(self):
        for rec in self:
            print('inside onchange description')
            return {
                'warning': {'type': 'notification', 'title': 'warning', 'message': 'description has been changed'}
            }

    def expected_selling_date(self):
        print('inside check expected selling date')
        property_ids = self.search([])

        for rec in property_ids:
            if rec.date_expected_selling and date.today() > rec.date_expected_selling and rec.state in ['draft', 'pending']:
                rec.is_late = True


class PropertyLine(models.Model):
    _name = 'property.line'

    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one('property')
