from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from io import BytesIO
import base64, xlsxwriter


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
    stop_date = fields.Date(compute='_compute_stop_date', string='Stop Date')
    excel_report = fields.Binary('Excel Report')
    
    @api.depends('start_date','duration')
    def _compute_stop_date(self):
        for rec in self:
            rec.stop_date = rec.start_date + relativedelta(days=+rec.duration)
    
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

    def action_excel_report(self):
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)

        worksheet = workbook.add_worksheet(self.name)
        worksheet.merge_range('A1:D1', 'Session')
        worksheet.write('A2', 'Start Date')
        worksheet.write('B2', self.start_date.strftime('%d/%m/%Y'))
        worksheet.write('A3', 'End Date')
        worksheet.write('B3', self.stop_date.strftime('%d/%m/%Y'))

        row, col = 4, 0
        headers = ('no', 'name', 'phone', 'email')
        for header in headers:
            worksheet.write(row, col, header.title())
            col += 1

        col = 0
        row += 1
        number = 1
        for partner in self.partner_ids:
            for header in headers:
                if header == 'no':
                    worksheet.write(row, col, number)
                else:
                    worksheet.write(row, col, partner[header])
                col += 1
            
            row += 1
            col = 0
        
        workbook.close()
        self.excel_report = base64.encodebytes(fp.getvalue())
        fp.close()

        return {
            "type": "ir.actions.act_url",
            "url": "web/content/?model={}&field={}&download=true&id={}&filename={}".format(
                self._name, 'excel_report', self.id, self.name
            ),
            "target": "new",
        }