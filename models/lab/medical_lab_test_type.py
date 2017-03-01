# -*- coding: utf-8 -*-

from odoo import fields, models


class MedicalLabTestType(models.Model):
    _name = "medical.test.type"
    _description = "Medical Lab Test Types"

    name = fields.Char(
        help='Name of test type, such as X-Ray, Hemogram, Biopsy, etc.',
        required=True,
    )
    code = fields.Char(
        size=128,
        help='Short name or code for test type.',
        required=True,
    )
    description = fields.Text()
    product_id = fields.Many2one(
        string='Service',
        comodel_name='product.product',
        required=True,
        domain="[('type', '=', 'service')]",
    )
    criterion_ids = fields.Many2many(
        string='Criteria',
        comodel_name='medical.test.criteria',
    )

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'The lab test name must be unique'),
        ('code_uniq', 'UNIQUE(code)', 'The lab test code must be unique'),
    ]
