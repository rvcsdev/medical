# -*- coding: utf-8 -*-

from odoo import models, fields


class MedicalDrugRoute(models.Model):
    _name = 'medical.drug.route'
    _description = 'Medical Drug Route'

    name = fields.Char(required=True, translate=True)
    code = fields.Char()

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Drug Route name must be unique!'),
    ]
