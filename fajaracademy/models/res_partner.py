from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_instructor = fields.Boolean('Instructor')
    session_ids = fields.Many2many('session', string='Session')