# -*- coding: utf-8 -*-
# from odoo import http


# class Fajaracademy(http.Controller):
#     @http.route('/fajaracademy/fajaracademy', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fajaracademy/fajaracademy/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('fajaracademy.listing', {
#             'root': '/fajaracademy/fajaracademy',
#             'objects': http.request.env['fajaracademy.fajaracademy'].search([]),
#         })

#     @http.route('/fajaracademy/fajaracademy/objects/<model("fajaracademy.fajaracademy"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fajaracademy.object', {
#             'object': obj
#         })

