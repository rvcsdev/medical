from odoo import models, fields 

class MedicalInsurancePlan(models.Model):
    _name = 'medical.insurance.plan'
    _description = 'Medical Insurance Plan'

    name = fields.Char(required=True)
    extra_info = fields.Text(string='Extra Info')