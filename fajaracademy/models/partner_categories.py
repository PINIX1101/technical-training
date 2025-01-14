from odoo import _, api, fields, models


class PartnerCategories(models.Model):
    _name = 'partner.categories'
    _description = 'Partner Categories'

    name = fields.Char('Name')