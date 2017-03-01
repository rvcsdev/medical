# -*- coding: utf-8 -*-

from odoo import api, fields, models


class MedicalPatient(models.Model):
    _inherit = 'medical.patient'

    @api.one
    def action_invalidate(self):
        super(MedicalPatient, self).action_invalidate()
        self.disease_ids.action_invalidate()

    @api.one
    def compute_count_disease_ids(self):
        self.count_disease_ids = len(self.disease_ids)

    disease_ids = fields.One2many(
        comodel_name='medical.patient.disease', inverse_name='patient_id',
        string='Diseases')
    count_disease_ids = fields.Integer(
        compute='compute_count_disease_ids', string='NB. Disease')
