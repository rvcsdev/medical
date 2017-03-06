# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from odoo import osv

class MedicalVisit(models.Model):
    _name = 'medical.visit'
    _description = 'Medical Visit'
    
    name = fields.Char(string='Visit ID', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    appointment_id = fields.Many2one('medical.appointment', string = "Select Appointment", ondelete="restrict", domain="[('appointment_type', '=', 'outpatient')]", help='Select if an appointment is made prior to visit.')
    patient_id = fields.Many2one('medical.patient', string = "Patient", ondelete="restrict", required=True, select=True, help="Patient Name")
    physician_id = fields.Many2one('medical.physician', string = "Physician", ondelete="restrict", required=True)
    institution_id = fields.Many2one('res.partner', string='Health Center', help='Medical Center', domain="[('is_institution', '=', True)]")
    consultations = fields.Many2one(string='Consultation Service', comodel_name='product.product', required=True, ondelete="cascade", domain="[('type', '=', 'service')]")
    scheduled_start  = fields.Datetime(string="Scheduled Start", required=True)
    scheduled_end  = fields.Datetime(string="Scheduled End")
    actual_start  = fields.Datetime(string="Actual Start", required=True)
    actual_end  = fields.Datetime(string="Actual End")
    extra_information = fields.Char(string="Extra Information")
    is_invoice_exempt = fields.Boolean()
    is_invoiced = fields.Boolean(string='Invoiced?', default=False, readonly=True)
    complaints = fields.Text(string='Complaints')
    observations = fields.Text(string='Observations')
    urgency = fields.Selection([('a', 'Normal'), ('b', 'Urgent'), ('c', 'Medical Emergency'), ], string='Urgency Level')
    state = fields.Selection([
        ('draft', 'Draft'), 
        ('confirmed', 'Confirmed'), 
        ('done', 'Done'), 
        ('cancelled', 'Cancelled')
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    vital_ids = fields.One2many(string='Vital Signs', comodel_name='medical.visit.vital', inverse_name='visit_id', copy=True)
    
    medication_prescription_ids = fields.One2many(string='Medication Prescriptions', comodel_name='medical.prescription.order', inverse_name='visit_id', copy=True)

    diagnosis_ids = fields.One2many(string='Diagnosis', comodel_name='medical.diagnosis', inverse_name='visit_id', copy=True)


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

    @api.onchange('appointment_id')
    def _get_appointment_details(self):
        for r in self:
            if r.appointment_id:
                r.patient_id = r.appointment_id.patient_id
                r.physician_id = r.appointment_id.physician_id
                r.institution_id = r.appointment_id.institution_id
                r.urgency = r.appointment_id.urgency
                r.consultations = r.appointment_id.consultations
                r.scheduled_start = r.appointment_id.appointment_date
                r.scheduled_end = r.appointment_id.date_end

    @api.multi
    def action_confirm(self):
        for visit in self:
            visit.state = 'confirmed'

        return True

    @api.multi
    def action_done(self):
        for visit in self:
            visit.state = 'done'

        return True

    @api.multi
    def action_create_invoice(self, cr, uid):
        if self.is_invoice_exempt == True:
            raise UserError(_("The appointment/visit is invoice exempt."))
        else:
            self.is_invoiced = True
            for record in self:
                invoice_id = self.pool.get('account.invoice').create(cr, uid,{
                    'name' : record.name,
                    'date_invoice' : record.create_date,
                    })
                for line in record.consultations:
                    self.pool.get('account.invoice.line').create(cr, uid,{
                        'invoice_id' : invoice_id,
                        'name' : line.name,
                        'product_id' : line.id,
                        })
        return True

    @api.multi
    def action_view_invoice(self):
        # for visit in self:
        #     visit.state = 'done'

        # return True
        visit = self.env['medical.visit'].browse(self._context.get('active_ids', []))
        return visit.action_view_invoice()

    @api.multi
    def action_print_prescription(self):
        if self.medication_prescription_ids:
            return self.env['report'].get_action(self, 'medical.report_prescriptionorder')
        else:
            raise UserError(_("No prescription available for printing."))

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancelled'})


