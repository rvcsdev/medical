# -*- coding: utf-8 -*-

from odoo import api, models, fields, _

class MedicalVisitVital(models.Model):
    _name = 'medical.visit.vital'
    _description = 'Medical Visit Vital'

    # name = fields.Char(string='Vital Code')

    name = fields.Char(string='Vital ID', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))    
    visit_id = fields.Many2one(comodel_name='medical.visit', string='Visit', ondelete='cascade', index=True, copy=False)
    date_conducted = fields.Datetime(string='Date', default=fields.Datetime.now, readonly=True)

    temperature = fields.Float(string='Temperatue')
    heart_rate = fields.Integer(string='Heart Rate')
    systolic_pressure = fields.Integer(string='Systolic Pressure')
    respiratory_rate = fields.Integer(string='Respiratory Rate')
    diastolic_pressure = fields.Integer(string='Diastolic Pressure')
    oxygen_saturation = fields.Integer(string='Oxygen Saturation')
    notes = fields.Text(string='Additional Notes')

    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
        if values.get('name', 'New') == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code('medical.visit.vital') or 'New'
    
        result = super(MedicalVisitVital, self).create(values)
    
        return result