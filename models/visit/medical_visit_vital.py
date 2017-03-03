# -*- coding: utf-8 -*-

from odoo import models, fields, _

class MedicalVisitVital(models.Model):
    _name = 'medical.visit.vital'
    _description = 'Medical Visit Vital'

    name = fields.Char(string='Vital Code')
    
