# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class MedicalPrescriptionOrder(models.Model):
    _name = 'medical.prescription.order'
    _description = 'Medical Prescription Order'

    # @api.model
    # def _get_default_name(self):
    #     return self.env['ir.sequence'].get('medical.prescription.order')

    # name = fields.Char(required=True, default=_get_default_name)
    name = fields.Char(string='Prescription ID', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one(comodel_name='medical.patient', string='Patient', required=True)
    physician_id = fields.Many2one('medical.physician', string='Physician', required=True, select=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Pharmacy')
    prescription_order_line_ids = fields.One2many(
        comodel_name='medical.prescription.order.line',
        inverse_name='prescription_order_id', string='Prescription Order Line')
    notes = fields.Text()
    is_pregnant = fields.Boolean()
    is_verified = fields.Boolean()
    date_prescription = fields.Datetime(default=fields.Datetime.now())

    visit_id = fields.Many2one(comodel_name='medical.visit', string='Visit', ondelete='cascade', index=True, copy=False)

    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
        if values.get('name', 'New') == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code('medical.prescription.order') or 'New'
    
        result = super(MedicalPrescriptionOrder, self).create(values)
    
        return result
