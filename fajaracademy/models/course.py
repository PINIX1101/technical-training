from odoo import _, api, fields, models


class Course(models.Model):
    _name = 'course'
    _description = 'Course'

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')

    user_id = fields.Many2one('res.users', string='Responsible User')
    session_ids = fields.One2many('session', 'course_id', string='Session')