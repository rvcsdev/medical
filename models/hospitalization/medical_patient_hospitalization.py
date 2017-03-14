from odoo import api, models, fields, _

class MedicalPatientHospitalization(models.Model):
    _name = 'medical.patient.hospitalization'
    _description = 'Medical Patient Hospitalization'

    name = fields.Char(string='Registration Code', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one(string='Patient', comodel_name='medical.patient', required=True, select=True, help='Patient Name')
    hospital_bed_id = fields.Many2one(string='Hospital Bed', comodel_name='medical.hospital.bed', required=True, select=True, help='Assign bed to patient.')
    admission_date = fields.Datetime(string='Admission Date')
    expected_discharge_date = fields.Datetime(string='Expected Discharge Date')
    attending_physician = fields.Many2one(string='Attending Physician', comodel_name='medical.physician', select=True, help='Select attending physician.')
    operating_physician = fields.Many2one(string='Operating Physician', comodel_name='medical.physician', selcte=True, help='Select operating physician.')
    admission_type = fields.Selection([
        ('routine', 'Routine'),
        ('maternity', 'Maternity'),
        ('elective', 'Elective'),
        ('urgent', 'Urgent'),
        ('emergency', 'Emergency'),
        ], string='Admission Type')
    admission_reason = fields.Char(string='Admission Reason')
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
            return {
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

    @api.multi
    def action_discharge(self):
        for hospitalization in self:
            hospitalization.state = 'discharged'

        return True

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancelled'})