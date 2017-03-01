# -*- coding: utf-8 -*-
from odoo import http

# class CapstoneMedical(http.Controller):
#     @http.route('/capstone_medical/capstone_medical/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/capstone_medical/capstone_medical/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('capstone_medical.listing', {
#             'root': '/capstone_medical/capstone_medical',
#             'objects': http.request.env['capstone_medical.capstone_medical'].search([]),
#         })

#     @http.route('/capstone_medical/capstone_medical/objects/<model("capstone_medical.capstone_medical"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('capstone_medical.object', {
#             'object': obj
#         })