from odoo import api, fields, models
from datetime import date

class SchoolStudents(models.Model):
    _inherit = "school.subjects"

    # subjects = fields.Many2one('school.subjects', string='Subjects')
    # stage = fields.Many2many()
