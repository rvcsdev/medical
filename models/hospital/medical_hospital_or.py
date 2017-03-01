# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class MedicalHospitalOr(models.Model):
    _name = 'medical.hospital.or'
    _inherit = ['abstract.medical.hospital']
    _description = 'Medical Hospital Operating Room'

    @api.one
    @api.constrains('name', 'zone_id')
    def _check_unicity_name(self):
        domain = [
            ('name', '=', self.name),
            ('zone_id', '=', self.zone_id.id),
        ]
        if len(self.search(domain)) > 1:
            raise ValidationError('"name" Should be unique per Zone')

    name = fields.Char(required=True)
    label = fields.Char()
    active = fields.Boolean(default=True)
    zone_id = fields.Many2one(
        string='Zone', comodel_name='medical.hospital.zone', index=True)
    partner_id = fields.Many2one(
        string='Institution', comodel_name='res.partner',
        domain=[('is_institution', '=', True)], index=True)
    unit_id = fields.Many2one(
        string='Unit', comodel_name='medical.hospital.unit', index=True)
    notes = fields.Text()
