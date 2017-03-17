from odoo import models, fields 

class MedicalSurgeryProcedure(models.Model):
    _name = 'medical.surgery.procedure'
    _description = 'Medical Surgery Procedure'

    surgery_id = fields.Many2one(string='Surgery', comodel_name='medical.surgery', required=True, select=True)
    procedure_id = fields.Many2one(string='Procedure', comodel_name='medical.procedure', required=True, select=True)
    notes = fields.Text(string='Notes')