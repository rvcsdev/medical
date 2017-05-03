from odoo import models, fields 

class MedicalLabTestTypeSample(models.Model):
    _name = 'medical.lab.test.type.sample'
    _description = 'Medical Lab Test Type Sample'

    name = fields.Char(string='Sample Name')
    abbreviation = fields.Char(string='Local Abbreviation')