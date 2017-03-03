# -*- coding: utf-8 -*-
from odoo import api, models, fields, _

class MedicalVisit(models.Model):
    _name = 'medical.visit'
    _description = 'Medical Visit'
    
    name = fields.Char(string='Visit ID', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    appointment_id = fields.Many2one('medical.appointment', string = "Appointment ID", ondelete="restrict", required=True)
    patient_id = fields.Many2one('medical.patient', string = "Patient", ondelete="restrict", required=True)
    physician_id = fields.Many2one('medical.physician', string = "Physician", ondelete="restrict", required=True)
    institution_id = fields.Many2one('res.partner', string='Health Center', help='Medical Center', domain="[('is_institution', '=', True)]")
    actual_start  = fields.Datetime(string="Date and Time Start", required=True)
    actual_end  = fields.Datetime(string="Date and Time End")
    extra_information = fields.Char(string="Extra Information")
    is_invoice_exempt = fields.Boolean()
    complaints = fields.Text(string='Complaints')
    observations = fields.Text(string='Observations')
    urgency = fields.Selection([('a', 'Normal'), ('b', 'Urgent'), ('c', 'Medical Emergency'), ], string='Urgency Level')

    vital_ids = fields.One2many(string='Vital Signs', comodel_name='medical.visit.vital', inverse_name='visit_id', copy=True)
    
    medication_prescription_ids = fields.One2many(string='Medication Prescriptions', comodel_name='medical.prescription.order', inverse_name='visit_id', copy=True)

    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
        if values.get('name', 'New') == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code('medical.visit') or 'New'
    
        result = super(MedicalVisit, self).create(values)
    
        return result
