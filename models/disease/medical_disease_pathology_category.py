# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MedicalPathologyCategory(models.Model):
    _name = 'medical.pathology.category'
    _description = 'Medical Pathology Category'

    @api.one
    @api.constrains('parent_id')
    def _check_recursion_parent_id(self):
        if not self._check_recursion():
            raise ValidationError('Error! You can not create recursive zone.')

    name = fields.Char(required=True, translate=True)
    child_ids = fields.One2many(
        comodel_name='medical.pathology.category', inverse_name='parent_id',
        string='Children Categories')
    parent_id = fields.Many2one(
        comodel_name='medical.pathology.category', string='Parent Category',
        index=True)
