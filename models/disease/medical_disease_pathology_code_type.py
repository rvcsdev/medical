# -*- coding: utf-8 -*-

from odoo import models, fields


class MedicalPathologyCodeType(models.Model):
    _name = 'medical.pathology.code.type'
    _description = 'Medical Pathology Code Type'

    name = fields.Char(
        required=True,
    )
