# -*- coding: utf-8 -*-

from odoo import fields, models


class MedicalPatient(models.Model):
    _inherit = 'medical.patient'

    medication_ids = fields.One2many(
        comodel_name='medical.patient.medication', inverse_name='patient_id',
        string='Medications')
