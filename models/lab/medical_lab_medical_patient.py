# -*- coding: utf-8 -*-

from odoo import fields, models


class MedicalPatient(models.Model):
    _inherit = "medical.patient"

    lab_test_ids = fields.One2many(
        string='Lab Tests',
        comodel_name='medical.lab.patient',
        inverse_name='patient_id',
    )
