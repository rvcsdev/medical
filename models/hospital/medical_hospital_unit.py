# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class MedicalHospitalUnit(models.Model):
    _name = 'medical.hospital.unit'
    _inherit = ['abstract.medical.hospital']
    _description = 'Medical Hospital Unit'

    @api.one
    @api.constrains('name')
    def _check_unicity_name(self):
        domain = [
            ('name', '=', self.name),
        ]
        if len(self.search(domain)) > 1:
            raise ValidationError('"name" Should be unique')

    name = fields.Char(required=True)
    label = fields.Char()
    notes = fields.Text()
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Institution',
        domain=[('is_institution', '=', True)], index=True)
    parent_id = fields.Many2one(
        string='Parent Unit', comodel_name='medical.hospital.unit', index=True)
