from odoo import models, fields 

class MedicalInsurance(models.Model):
    _name = 'medical.insurance'
    _description = 'Medical Insurance'

    name = fields.Char(required=True, string='Number')
    type = fields.Selection([
        ('state','State'),
        ('labour', 'Labour Union/Syndical'),
        ('private', 'Private'),
    ], string='Insurance Type')

    patient_id = fields.Many2one('medical.patient', string='Patient', required=True, select=True, help='Patient Name')
    insurance_company = fields.Many2one(
        comodel_name='res.partner',
        domain="[('is_insurance_company', '=', True)]",
        string='Insurance Company'
    )

    plan = fields.Many2one('medical.insurance.plan', select=True)
    category = fields.Char()
    member_since = fields.Datetime(string='Member Since')
    expiration_date = fields.Datetime(string='Expiration Date')
    extra_info = fields.Text(string='Extra Info')