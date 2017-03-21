from odoo import models, fields 

class MedicalPatientFamily(models.Model):
    _name = 'medical.patient.family'
    _description = 'Medical Patient Family'

    name = fields.Char(required=True)
    extra_info = fields.Text(string='Extra Info')
    member_ids = fields.One2many(string='Members', comodel_name='medical.patient', inverse_name='family_id')