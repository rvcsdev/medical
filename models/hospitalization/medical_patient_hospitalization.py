from odoo import api, models, fields, _

class MedicalPatientHospitalization(models.Model):
    _name = 'medical.patient.hospitalization'
    _description = 'Medical Patient Hospitalization'
    _order = 'priority desc, create_date desc'

    name = fields.Char(string='Registration Code', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one(string='Patient', comodel_name='medical.patient', required=True, select=True, help='Patient Name')
    hospital_bed_id = fields.Many2one(string='Hospital Bed', comodel_name='medical.hospital.bed', select=True, help='Assign bed to patient.')
    admission_date = fields.Datetime(string='Admission Date', default=fields.Datetime.now)
    expected_discharge_date = fields.Datetime(string='Expected Discharge Date')
    attending_physician = fields.Many2one(string='Attending Physician', comodel_name='medical.physician', select=True, help='Select attending physician.')
    operating_physician = fields.Many2one(string='Operating Physician', comodel_name='medical.physician', select=True, help='Select operating physician.')
    admission_type = fields.Selection([
        ('routine', 'Routine'),
        ('maternity', 'Maternity'),
        ('elective', 'Elective'),
        ('urgent', 'Urgent'),
        ('emergency', 'Emergency'),
        ], string='Admission Type', default='routine',required=True)
    # admission_reason = fields.Char(string='Admission Reason')
    priority = fields.Integer()
    admission_reason = fields.Many2one(string='Admission Reason', comodel_name='medical.pathology', select=True)
    extra_info = fields.Text(string='Extra Info')
    transfer_history_ids = fields.One2many(string='Transfer History', comodel_name='medical.patient.hospitalization.transfer', inverse_name='hospitalization_id', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'), 
        ('confirmed', 'Confirmed'), 
        ('hospitalized', 'Hospitalized'), 
        ('discharged', 'Discharged'), 
        ('cancelled', 'Cancelled')
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    belief = fields.Many2one(comodel_name='medical.patient.hospitalization.belief', select=True)
    vegetarian = fields.Selection([
        ('none', 'None'), 
        ('vegetarian', 'Vegetarian'), 
        ('lacto', 'Lacto Vegetarian'), 
        ('lactoovo', 'Lacto-Ovo Vegetarian'), 
        ('pescetarian', 'Pescetarian'),
        ('vegan', 'Vegan'),
        ], string='Vegetarian')

    nutrition_notes = fields.Text(string='Nutrition Notes/Direction')
    therapeutic_diets = fields.One2many(string='Therapeutic Diets', comodel_name='medical.patient.hospitalization.nutrition.diet', inverse_name='hospitalization_id')

    is_icu = fields.Boolean(string='ICU')

    medication_ids = fields.Many2many(comodel_name='medical.medication.template', string='Medications')

    is_invoice_exempt = fields.Boolean()
    is_invoiced = fields.Boolean(string='Invoiced?', default=False, readonly=True)
    invoice_ids = fields.Many2many("account.invoice", string='Invoices', readonly=True, copy=False)

    laboratory_ids = fields.One2many(string='Laboratory Requests', comodel_name='medical.lab', inverse_name='hospitalization_id')
    imaging_ids = fields.One2many(string='Imaging Requests', comodel_name='medical.imaging.request', inverse_name='hospitalization_id')
    icu_ids = fields.One2many(string='ICU Admission', comodel_name='medical.patient.hospitalization.icu', inverse_name='hospitalization_id')
    
    #Care Plan
    nursing_plan = fields.Text(string='Nursing Plan')
    discharge_plan = fields.Text(string='Discharge Plan')

    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
        if values.get('name', 'New') == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code('medical.patient.hospitalization') or 'New'
    
        result = super(MedicalPatientHospitalization, self).create(values)
    
        return result

    @api.onchange('admission_type')
    def _set_priority(self):
        if self.admission_type == 'routine':
            self.priority = 1
        if self.admission_type == 'maternity':
            self.priority = 2
        if self.admission_type == 'elective':
            self.priority = 3
        if self.admission_type == 'urgent':
            self.priority = 4
        if self.admission_type == 'emergency':
            self.priority = 5

    @api.multi
    def action_confirm(self):
        for hospitalization in self:
            hospitalization.state = 'confirmed'

        return True

    @api.multi
    def action_admission(self):
        for hospitalization in self:
            hospitalization.state = 'hospitalized'

        return True

    @api.multi
    def action_transfer(self):
        for hospitalization in self:
            vals = {}
            vals['hospitalization_id'] = hospitalization.id
            vals['current_bed'] = hospitalization.hospital_bed_id.id
            transfer = {
                'type': 'ir.actions.act_window',
                'name': 'Transfer Bed',
                'view_type': 'form',    
                'view_mode': 'form',
                'res_model': 'medical.patient.hospitalization.transfer',
                # 'res_id': invoice.id,
                'view_id': self.env.ref('medical.medical_patient_hospitalization_transfer_form').id,
                # 'domain': "[('type','in',('out_invoice', 'out_refund'))]",
                'context': vals,
                # 'data': vals,
                'target': 'new',
            }
            return transfer

    @api.multi
    def action_discharge(self):
        for hospitalization in self:
            hospitalization.state = 'discharged'

        return True

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancelled'})

    @api.multi
    def action_create_invoice(self):
        if self.is_invoice_exempt == True:
            raise UserError(_("This record is invoice exempt."))
        else:
            for record in self:
                if record.medication_ids:
                    if not record.medication_ids.medicament_id.property_account_income_id:
                        raise UserError(_("Please define income account for this product."))
                    else:
                        invoice_id = self.env['account.invoice'].create({
                            'name' : record.name,
                            'origin' : record.name,
                            'type': 'out_invoice',
                            'date_invoice' : fields.Datetime.now(),
                            'partner_id' : record.patient_id.partner_id.id,
                            'invoice_line_ids': [(0, 0, {
                                'name' : record.medication_ids.medicament_id.name,
                                'product_id' : record.medication_ids.medicament_id.id,
                                'price_unit' : record.medication_ids.medicament_id.list_price,
                                'quantity' : 1,
                                'account_id' : record.medication_ids.medicament_id.property_account_income_id.id,
                                'invoice_line_tax_ids' : [(6, 0, record.medication_ids.medicament_id.taxes_id.ids)],
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
        for record in self:
            for invoice in record.invoice_ids:
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