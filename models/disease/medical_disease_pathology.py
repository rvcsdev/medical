# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MedicalPathology(models.Model):
    _name = 'medical.pathology'
    _description = 'Medical Pathology'

    @api.one
    @api.constrains('code')
    def _check_unicity_name(self):
        domain = [
            ('code', '=', self.code),
        ]
        if len(self.search(domain)) > 1:
            raise ValidationError('"code" Should be unique per Pathology')

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)
    notes = fields.Text(translate=True)
    protein = fields.Char(string='Protein involved')
    chromosome = fields.Char(string='Affected Chromosome')
    gene = fields.Char()
    category_id = fields.Many2one(
        comodel_name='medical.pathology.category',
        string='Category of Pathology', index=True)
    medical_pathology_group_m2m_ids = fields.Many2many(
        comodel_name='medical.pathology.group', column1='pathology_id',
        colmun2='pathology_group_id', string='Medical Pathology Groups',
        relation="pathology_id_pathology_group_id_rel")
