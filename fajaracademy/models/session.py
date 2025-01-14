from odoo import _, api, fields, models


class Session(models.Model):
    _name = 'session'
    _description = 'Session'

    name = fields.Char('Name', required=True)
    start_date = fields.Date('Start Date', default=fields.Date.today())
    duration = fields.Float('Duration')
    number_of_seats = fields.Float('Number of Seats')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('closed', 'Closed'),
    ], string='State',default="draft")
    description = fields.Text('Description')

    def action_confirm(self):
        self.state = 'running'

    def action_draft(self):
        self.state = 'draft'

    def action_done(self):
        self.state = 'closed'
