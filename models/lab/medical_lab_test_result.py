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
    result_actual = fields.Char(
        string='Result',
    )
    lab_id = fields.Many2one(
        string='Lab',
        comodel_name='medical.lab',
        required=True,
    )
    sequence = fields.Integer(
        default=5,
        required=True,
    )
    notes = fields.Text()
