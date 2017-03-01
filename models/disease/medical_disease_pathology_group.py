# -*- coding: utf-8 -*-

from odoo import fields, models


class MedicalPathologyGroup(models.Model):
    _name = 'medical.pathology.group'
    _descriptionription = 'Medical Pathology Group'

    name = fields.Char(required=True, translate=True)
    notes = fields.Text(translate=True)
    code = fields.Char(
        required=True, help='for example MDG6 code will contain'
        ' the Millennium Development Goals # 6 diseases : Tuberculosis, '
        'Malaria and HIV/AIDS')
    description = fields.Text(
        string='Short Description', required=True, translate=True)
