# -*- coding: utf-8 -*-
from odoo import fields, models

class MedicalLabTestResult(models.Model):
    _name = 'medical.lab.test.result'
    _description = 'Medical Lab Test Results'
    _order = 'sequence'
    _inherits = {'medical.test.criteria': 'criterion_id'}

    criterion_id = fields.Many2one(
        string='Criterion',
        comodel_name='medical.test.criteria',
        # required=True,
        ondelete='restrict',
        domain="[('test_type_ids', '=', lab_id.test_type_id)]",
    )

    name = fields.Char(string='Test Name', size=128, required=True)
    sequence = fields.Integer(default=5, required=True)
    
    lower_limit = fields.Float(string='Lower Limit')
    upper_limit = fields.Float(string='Upper Limit')
    result_actual = fields.Float(string='Result')
    uom_id = fields.Many2one(string='Unit of Measure', comodel_name='product.uom')
    is_warning = fields.Boolean(string='Warning')
    # is_excluded = fields.Boolean(string='Excluded')

    lab_id = fields.Many2one(string='Lab', comodel_name='medical.lab', required=True)
    notes = fields.Text()
