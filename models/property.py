import json

import requests
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, timedelta


class Property(models.Model):
    _name = 'property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Property'

    name = fields.Char(required=True, size=40, tracking=True, translate=True)
    # currency_id = fields.Many2one('res.currency', compute='_get_company_currency')
    ref = fields.Char(default='New', readonly=True)
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
                              ('closed', 'Closed')], default='draft', tracking=True,)
    property_line_ids = fields.One2many('property.line', 'property_id')
    active = fields.Boolean(default=True)
    creation_time = fields.Datetime(readonly=True, default=fields.Datetime.now)
    next_time = fields.Datetime(compute='_compute_next_time')
    owner_gender = fields.Selection(related='owner_id.gender')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'this name is exist!')
    ]

    # @api.onchange('state')
    # def onchange_state(self):
    #     print('state changed')

    # def _get_company_currency(self):
    #     for rec in self:
    #         rec.currency_id = self.env.ref('base.USD').

    def get_properties(self):
        print('get properties')
        try:
            payload = dict()
            response = requests.get('http://127.0.0.1:8015/v1/property/get_all', data=payload)
            result = json.loads(response.content)
            print(result)
            if response.content.status_code == 200:
                print('succssfull')
            else:
                print('failed or not found')
        except Exception as error:
            raise ValidationError(str(error))

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = self.name + ' (copy)'

        return super(Property, self).copy(default)

    @api.constrains('bedrooms')
    def check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms <= 0:
                raise ValidationError(_('bedrooms must be greater than 0'))

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('property_seq')
        return super(Property, self).create(vals)

    def write(self, vals):
        res = super(Property, self).write(vals)
        print('inside write method')
        return res
    
    def unlink(self):
        res = super(Property, self).unlink()
        print('inside unlink method')

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft')
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
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

    def action(self):
        pass

    def create_history_record(self, old_state, new_state, reason=''):
        for rec in self:
            history_dict = {
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'property_history_line_ids': [(0, 0, {'description': line.description, 'area': line.area}) for line in rec.property_line_ids]
            }
            history_id = self.env['property.history'].create(history_dict)

    def action_open_change_state_wizard(self):
        action = self.env.ref('app_one.change_state_wizard_action').read()[0]
        action['context'] = {'default_property_id': self.id}
        return action

    @api.depends('creation_time')
    def _compute_next_time(self):
        for rec in self:
            if rec.creation_time:
                rec.next_time = rec.creation_time + timedelta(hours=6)
            else:
                rec.next_time = False

    def open_related_owner_button(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form').id

        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]

        return action


class PropertyLine(models.Model):
    _name = 'property.line'

    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one('property')
