from odoo import _, api, fields, models


class Course(models.Model):
    _name = 'course'
    _description = 'Course'

    _sql_constraints = [
        ("name_description_check", "check(name != description)", "Name and Description must be different"),
        ("name_unique", "unique(name)", "Name must be unique"),
    ]

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')

    user_id = fields.Many2one('res.users', string='Responsible User')
    session_ids = fields.One2many('session', 'course_id', string='Session')

    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', 'Copy of {}%'.format(self.name))]
        )

        if not copied_count:
            new_name = 'Copy of {}'.format(self.name)
        else:
            new_name = 'Copy of {} ({})'.format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)