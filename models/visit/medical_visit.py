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

    invoice_ids = fields.Many2many("account.invoice", string='Invoices', compute="_get_invoiced", readonly=True, copy=False)
    # invoice_ids = fields.Many2many("account.invoice", string='Invoices', readonly=True, copy=False)
    # invoice_lines = fields.Many2many('account.invoice.line', 'sale_order_line_invoice_rel', 'order_line_id', 'invoice_line_id', string='Invoice Lines', copy=False)


    @api.depends('state')
    def _get_invoiced(self):
    #     for visit in self:
    #         invoice_ids = visit.consultations.mapped('invoice_lines').mapped('invoice_id').filtered(lambda r: r.type in ['out_invoice', 'out_refund'])
    #         # Search for invoices which have been 'cancelled' (filter_refund = 'modify' in
    #         # 'account.invoice.refund')
    #         # use like as origin may contains multiple references (e.g. 'SO01, SO02')
    #         refunds = invoice_ids.search([('origin', 'like', order.name)])
    #         invoice_ids |= refunds.filtered(lambda r: order.name in [origin.strip() for origin in r.origin.split(',')])
    #         # Search for refunds as well
    #         refund_ids = self.env['account.invoice'].browse()
    #         if invoice_ids:
    #             for inv in invoice_ids:
    #                 refund_ids += refund_ids.search([('type', '=', 'out_refund'), ('origin', '=', inv.number), ('origin', '!=', False), ('journal_id', '=', inv.journal_id.id)])

    #         line_invoice_status = [line.invoice_status for line in order.order_line]

    #         if order.state not in ('sale', 'done'):
    #             invoice_status = 'no'
    #         elif any(invoice_status == 'to invoice' for invoice_status in line_invoice_status):
    #             invoice_status = 'to invoice'
    #         elif all(invoice_status == 'invoiced' for invoice_status in line_invoice_status):
    #             invoice_status = 'invoiced'
    #         elif all(invoice_status in ['invoiced', 'upselling'] for invoice_status in line_invoice_status):
    #             invoice_status = 'upselling'
    #         else:
    #             invoice_status = 'no'

    #         order.update({
    #             'invoice_count': len(set(invoice_ids.ids + refund_ids.ids)),
    #             'invoice_ids': invoice_ids.ids + refund_ids.ids,
    #             'invoice_status': invoice_status
    #         })
        for visit in self:
            invoice_ids = self.env['account.invoice'].search([('origin', 'like', visit.name)])
            invoices = self.env['account.invoice'].browse()
            visit.update({
                'invoice_ids': invoices.ids,
            })

    
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
    def action_create_invoice(self):
        if self.is_invoice_exempt == True:
            raise UserError(_("The appointment/visit is invoice exempt."))
        else:
            for record in self:
                if record.consultations:
                    if not record.consultations.property_account_income_id:
                        raise UserError(_("Please define income account for this product."))
                    else:
                        invoice_id = self.env['account.invoice']
                        invoice_id.create({
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
                        self.is_invoiced = True
                        # self.invoice_ids = invoice_id.id
                        invoice_id.compute_taxes()
                        invoice_id.message_post_with_view('mail.message_origin_link',
                            values={'self': invoice_id, 'origin': record},
                            subtype_id=self.env.ref('mail.mt_note').id)
                        return self.action_view_invoice()
                else:
                     raise UserError(_("There is no invoicable line."))
                # invoice_id_line = self.env['account.invoice.line']
                # if record.consultations:
                #     if not record.consultations.property_account_income_id:
                #         raise UserError(_("Please define income account for this product."))
                #     else:
                #         invoice_id_line.create({
                #             'invoice_id' : invoice_id,
                #             'name' : record.consultations.name,
                #             'product_id' : record.consultations.id,
                #             'price_unit' : record.consultations.price,
                #             'quantity' : 1,
                #             'account_id' : record.consultations.property_account_income_id.id,
                #         })

                #         invoice_id.update({
                #             'id': invoice_id, 
                #             'invoice_line_ids': invoice_id_line, 
                #             })

                #         for line in invoice_id.invoice_line_ids:
                #             line._set_additional_fields(invoice_id)
                        
                #         self.is_invoiced = True
                #         self.invoice_ids = invoice_id

                #         invoice_id.compute_taxes()
                #         invoice_id.message_post_with_view('mail.message_origin_link',
                #             values={'self': invoice_id, 'origin': record},
                #             subtype_id=self.env.ref('mail.mt_note').id)
                #         return self.action_view_invoice()
                # else:
                #     raise UserError(_("There is no invoicable line."))
        return True

    @api.multi
    def action_view_invoice(self):
        # # for visit in self:
        # #     visit.state = 'done'

        # # return True
        # visit = self.env['medical.visit'].browse(self._context.get('active_ids', []))
        # return visit.action_view_invoice()
        invoices = self.mapped('invoice_ids')
        action = self.env.ref('account.action_invoice_tree1').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            action['views'] = [(self.env.ref('account.invoice_form').id, 'form')]
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.multi
    def action_print_prescription(self):
        if self.medication_prescription_ids:
            return self.env['report'].get_action(self, 'medical.report_prescriptionorder')
        else:
            raise UserError(_("No prescription available for printing."))

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancelled'})


