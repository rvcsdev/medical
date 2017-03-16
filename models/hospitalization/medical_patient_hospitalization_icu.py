from odoo import api, models, fields, _ 

class MedicalPatientHospitalizationIcu(models.Model):
    _name = 'medical.patient.hospitalization.icu'
    _description = 'Medical Patient Hospitalization ICU'

    name = fields.Char()
    hospitalization_id = fields.Many2one(string='Registration', comodel_name='medical.patient.hospitalization', ondelete='cascade', required=True, select=True)
    icu_admission_date = fields.Datetime(string='ICU Admission Date', default=fields.Datetime.now(), readonly=True)
    duration = fields.Char(string='Duration')
    is_admitted = fields.Boolean(string='Admitted')
    is_discharged = fields.Boolean(string='Discharged')
    is_current = fields.Boolean(string='Current')
    ventilation_ids = fields.One2many(comodel_name='medical.patient.hospitalization.icu.ventilation', inverse_name='icu_id', string='Mechanical Ventilation History')