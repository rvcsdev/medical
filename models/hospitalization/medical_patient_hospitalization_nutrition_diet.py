from odoo import api, models, fields, _

class MedicalPatientHospitalizationNutritionDiet(models.Model):
    _name = 'medical.patient.hospitalization.nutrition.diet'
    _description = 'Medical Patient Hospitalization Nutrition Diet'

    name = fields.Char()
    hospitalization_id = fields.Many2one(comodel_name='medical.patient.hospitalization', string='Hospitalization', ondelete='cascade', required=True, select=True, default=lambda self: self._context.get('hospitalization_id'))
    diet = fields.Many2one(string='Diet', comodel_name='medical.patient.hospitalization.diet', select=True)
    remarks = fields.Text(string='Remarks / Direction')