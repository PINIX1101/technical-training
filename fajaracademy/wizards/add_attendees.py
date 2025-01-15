from odoo import _, api, fields, models


class AddAttendees(models.TransientModel):
    _name = 'add.attendees'
    _description = 'Add Attendees'

    session_ids = fields.Many2many('session', string='Session')
    partner_ids = fields.Many2many('res.partner', string='Partner')

    def confirm(self):
        for session in self.session_ids:
            session.partner_ids |= self.partner_ids