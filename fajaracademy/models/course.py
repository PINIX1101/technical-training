from odoo import _, api, fields, models


class Course(models.Model):
    _name = 'course'
    _description = 'Course'

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')