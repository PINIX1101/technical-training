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
    partner_id = fields.Many2one('res.partner', string='Instructior', domain="['|',('is_instructor', '=', True), ('partner_category_id', '!=', False)]")
    course_id = fields.Many2one('course', string='Course')
    partner_ids = fields.Many2many('res.partner', string='partner')
    taken_seats = fields.Float(compute='_compute_taken_seats', string='Taken Seats')
    
    @api.depends('number_of_seats','partner_ids')
    def _compute_taken_seats(self):
        for rec in self:
            if rec.number_of_seats:
                rec.taken_seats = len(rec.partner_ids)/rec.number_of_seats*100
            else:
                rec.taken_seats = 0

    def action_confirm(self):
        self.state = 'running'

    def action_draft(self):
        self.state = 'draft'

    def action_done(self):
        self.state = 'closed'
