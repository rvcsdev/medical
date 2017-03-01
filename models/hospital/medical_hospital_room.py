# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MedicalHospitalRoom(models.Model):
    _name = 'medical.hospital.room'
    _inherit = ['abstract.medical.hospital']
    _description = 'Medical Hospital Room'
    _rec_name = 'display_name'

    @api.one
    @api.constrains('name', 'zone_id')
    def _check_unicity_name(self):
        domain = [
            ('name', '=', self.name),
            ('zone_id', '=', self.zone_id.id),
        ]
        if len(self.search(domain)) > 1:
            raise ValidationError('"name" Should be unique per Zone')

    @api.one
    @api.depends('name', 'zone_id', 'zone_id.name',
                 'zone_id.display_name')
    def _compute_display_name(self):
        self.display_name =\
            '%s/%s' % (self.zone_id.display_name, self.name)

    name = fields.Char(required=True)
    display_name = fields.Char(compute='_compute_display_name', store=True)
    label = fields.Char()
    phone = fields.Char()
    notes = fields.Text()
    capacity = fields.Integer()
    state = fields.Selection([
        ('free', 'Free'),
        ('beds_available', 'Beds available'),
        ('full', 'Full'), ], default='free')
    private = fields.Boolean()
    active = fields.Boolean(default=True)

    unit_id = fields.Many2one(
        string='Unit', comodel_name='medical.hospital.unit', index=True)
    zone_id = fields.Many2one(
        string='Zone', comodel_name='medical.hospital.zone', index=True,
        required=True)
    # bed_ids = fields.One2many(
    #     string='Beds', comodel_name='medical.hospital.bed',
    #     inverse_name='room_id')
