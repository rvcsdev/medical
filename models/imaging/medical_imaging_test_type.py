from odoo import models, fields

class MedicalImagingTestType(models.Model):
    _name = 'medical.imaging.test.type'
    _description = 'Medical Imaging Test Type'

    name = fields.Char(size=256, string='Name', required=True, translate=True)
    code = fields.Char(size=256, string='Code', required =True)