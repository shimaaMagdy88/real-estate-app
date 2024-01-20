from odoo import fields, api, models

class Tag(models.Model):
    _name = 'tag'
    _description = 'tags of properties'

    name = fields.Char()
