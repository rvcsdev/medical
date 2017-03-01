# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AbstractHospital(models.AbstractModel):
    _name = 'abstract.medical.hospital'
    _description = 'Abstract Medical Hospital'

    @api.one
    @api.depends('active')
    def _compute_expire_date(self):
        if self.active:
            self.expire_date = False
        else:
            self.expire_date = fields.Datetime.now()

    active = fields.Boolean(default=True)
    expire_date = fields.Datetime(
        compute='_compute_expire_date', store=True)

    @api.one
    def action_invalidate(self):
        self.active = False

    @api.one
    def action_revalidate(self):
        self.active = True
