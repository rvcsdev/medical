from odoo import api, models, fields, _

class MedicalPatientHospitalizationDiet(models.Model):
    _name = 'medical.patient.hospitalization.diet'
    _description = 'Medical Patient Hospitalization Diet'

    name = fields.Char(string='Name', required=True)
    type = fields.Char(string='Diet Type', required=True)
    description = fields.Text()