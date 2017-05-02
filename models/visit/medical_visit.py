# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

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
    actual_start  = fields.Datetime(string="Actual Start")
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
    
    # laboratory_ids = fields.One2many(string='Laboratory', comodel_name='medical.lab', inverse_name='visit_id', copy=True)

    # imaging_ids = fields.One2many(string='Imaging', comodel_name='medical.imaging', inverse_name='visit_id', copy=True)

    medication_prescription_ids = fields.One2many(string='Medication Prescriptions', comodel_name='medical.prescription.order', inverse_name='visit_id', copy=True)

    diagnosis_ids = fields.One2many(string='Diagnosis', comodel_name='medical.diagnosis', inverse_name='visit_id', copy=True)

    # invoice_ids = fields.Many2many("account.invoice", string='Invoices', compute="_get_invoiced", readonly=True, copy=False)
    invoice_ids = fields.Many2many("account.invoice", string='Invoices', readonly=True, copy=False)
    # invoice_lines = fields.Many2many('account.invoice.line', 'sale_order_line_invoice_rel', 'order_line_id', 'invoice_line_id', string='Invoice Lines', copy=False)
    
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
    def action_create_hospitalization(self):
        for record in self:
            hospitalization_id = self.env['medical.patient.hospitalization'].create({
                'patient_id': self.patient_id.id,
                'attending_physician': self.physician_id.id,
            })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Patient Hospitalization',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'medical.patient.hospitalization',
            'res_id': hospitalization_id.id,
            'view_id': self.env.ref('medical.medical_appointment_view_form').id,
            # 'domain': "[('type','in',('out_invoice', 'out_refund'))]",
            # 'context': "{'type':'out_invoice', 'journal_type': 'sale'}",
            'target': 'current',
        }

    @api.multi
    def action_create_invoice(self):
        if self.is_invoice_exempt == True:
            raise UserError(_("The appointment/visit is invoice exempt."))
        else:
            for record in self:
                if record.consultations:
                    if not record.consultations.property_account_income_id:
                        raise UserError(_("Please define income account for this product."))
                    else:
                        invoice_id = self.env['account.invoice'].create({
                            'name' : record.name,
                            'origin' : record.name,
                            'type': 'out_invoice',
                            'date_invoice' : fields.Datetime.now(),
                            'partner_id' : record.patient_id.partner_id.id,
                            'invoice_line_ids': [(0, 0, {
                                'name' : record.consultations.name,
                                'product_id' : record.consultations.id,
                                'price_unit' : record.consultations.list_price,
                                'quantity' : 1,
                                'account_id' : record.consultations.property_account_income_id.id,
                                'invoice_line_tax_ids' : [(6, 0, record.consultations.taxes_id.ids)],
                            })],  
                            # 'company_id': record.company_id.id,
                            # 'user_id': record.user_id and record.user_id.id,
                            # 'team_id': record.team_id.id
                        })
                        # self.is_invoiced = True
                        # self.invoice_ids = invoice_id.id
                        # invoice_created_id = invoice_id
                        # raise Warning(invoice_created_id.id)
                        invoice_id.compute_taxes()
                        invoice_id.message_post_with_view('mail.message_origin_link',
                            values={'self': invoice_id, 'origin': record},
                            subtype_id=self.env.ref('mail.mt_note').id)
                        invoice_created_id = invoice_id
                        # raise Warning(invoice_created_id.id)
                        self.is_invoiced = True
                        self.invoice_ids = invoice_created_id
                        return {
                            'type': 'ir.actions.act_window',
                            'name': 'Invoice',
                            'view_type': 'form',
                            'view_mode': 'form',
                            'res_model': 'account.invoice',
                            'res_id': invoice_created_id.id,
                            'view_id': self.env.ref('account.invoice_form').id,
                            # 'domain': "[('type','in',('out_invoice', 'out_refund'))]",
                            # 'context': "{'type':'out_invoice', 'journal_type': 'sale'}",
                            'target': 'current',
                        }
                        # return self.action_view_invoice()
                else:
                     raise UserError(_("There is no invoicable line."))
        return True

    @api.multi
    def action_view_invoice(self):
        for visit in self:
            for invoice in visit.invoice_ids:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Invoice',
                    'view_type': 'form',    
                    'view_mode': 'form',
                    'res_model': 'account.invoice',
                    'res_id': invoice.id,
                    'view_id': self.env.ref('account.invoice_form').id,
                    # 'domain': "[('type','in',('out_invoice', 'out_refund'))]",
                    # 'context': "{'type':'out_invoice', 'journal_type': 'sale'}",
                    'target': 'current',
                }        

    @api.multi
    def action_print_prescription(self):
        if self.medication_prescription_ids:
            return self.env['report'].get_action(self, 'medical.report_prescriptionorder')
        else:
            raise UserError(_("No prescription available for printing."))

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancelled'})


