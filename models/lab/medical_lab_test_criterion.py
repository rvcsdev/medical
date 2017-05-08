# -*- coding: utf-8 -*-

from odoo import fields, models

class MedicalLabTestCriterion(models.Model):
    _name = 'medical.test.criteria'
    _description = 'Medical Lab Test Criteria'
    _order = 'sequence'

    name = fields.Char(string='Test Name', size=128, required=True)
    sequence = fields.Integer(
        default=5,
        required=True,
    )
    # description = fields.Text()
    result_expect = fields.Char(string='Normal Range')
    lower_limit = fields.Float(string='Lower Limit')
    upper_limit = fields.Float(string='Upper Limit')
    uom_id = fields.Many2one(string='Unit of Measure', comodel_name='product.uom')
    test_type_ids = fields.Many2many(
        string='Test Types',
        comodel_name='medical.test.type',
        ondelete='restrict',
        help='This criterion is related to these test types.',
    )
    is_warning = fields.Boolean(string='Warning')
    is_excluded = fields.Boolean(string='Excluded')
    
