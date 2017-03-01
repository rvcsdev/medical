# -*- coding: utf-8 -*-

from odoo import models, fields


class MedicalDrugForm(models.Model):
    _name = 'medical.drug.form'
    _description = 'Medical Drug Form'

    name = fields.Char(required=True, translate=True)
    code = fields.Char()

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Drug name must be unique!'),
    ]
