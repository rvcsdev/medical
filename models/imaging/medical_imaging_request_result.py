# -*- coding: utf-8 -*-

from odoo import models, fields, _ 

class MedicalImagingRequestResult(models.Model):
    _name = 'medical.imaging.request.result'
    _description = 'Medical Imaging Request Result'

    name = fields.Char(string='Result ID')
