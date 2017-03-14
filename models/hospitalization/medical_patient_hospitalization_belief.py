from odoo import api, models, fields, _

class MedicalPatientHospitalizationBelief(models.Model):
    _name = 'medical.patient.hospitalization.belief'
    _description = 'Medical Patient Hospitalization Belief'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    description = fields.Text()
