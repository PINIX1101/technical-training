from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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
    partner_ids = fields.Many2many('res.partner', string='Attendees')
    taken_seats = fields.Float(compute='_compute_taken_seats', string='Taken Seats')
    active = fields.Boolean('Active', default=True)
    number_of_attendees = fields.Float(compute='_compute_number_of_attendees', string='Number of Attendees',store=True)
    
    @api.depends('partner_ids')
    def _compute_number_of_attendees(self):
        for rec in self:
            rec.number_of_attendees = len(rec.partner_ids)
    
    @api.depends('number_of_seats','partner_ids')
    def _compute_taken_seats(self):
        for rec in self:
            if rec.number_of_seats:
                rec.taken_seats = len(rec.partner_ids)/rec.number_of_seats*100
            else:
                rec.taken_seats = 0

    @api.onchange('number_of_seats', 'partner_ids')
    def _onchange_participants(self):
        if self.number_of_seats < 0:
            return {
                'warning': {
                    'title': "Invalid Value",
                    'message': "Cannot input negative value on Number of Seats"
                }
            }
        if self.number_of_seats < len(self.partner_ids):
            return {
                'warning': {
                    'title': "Invalid Value",
                    'message': "Participants more than seats"
                }
            }
        
    @api.constrains('partner_id', 'partner_ids')
    def _constrains_instructor_attendes(self):
        for rec in self:
            if rec.partner_id in rec.partner_ids:
                raise ValidationError('Instructor cannot be Attendee: {}'.format(rec.partner_id.name))

    def action_confirm(self):
        self.state = 'running'

    def action_draft(self):
        self.state = 'draft'

    def action_done(self):
        self.state = 'closed'
