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
    transfer_history_ids = fields.One2many(string='Transfer History', comodel_name='medical.patient.hospitalization.transfer.history', inverse_name='hospitalization_id', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'), 
        ('confirmed', 'Confirmed'), 
        ('hospitalized', 'Hospitalized'), 
        ('discharged', 'Discharged'), 
        ('cancelled', 'Cancelled')
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

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
    def action_discharge(self):
        for hospitalization in self:
            hospitalization.state = 'discharged'

        return True

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancelled'})

    class MedicalPatientHospitalizationTransferHistory(models.Model):
        _name = 'medical.patient.hospitalization.transfer.history'
        _description = 'Medical Patient Hospitalization Transfer History'

        hospitalization_id = fields.Many2one(comodel_name='medical.patient.hospitalization', string='Hospitalization', ondelete='cascade')
        transfer_history_date = fields.Datetime(string='Date', default=fields.Datetime.now)
        transfer_from = fields.Char(string='From')
        transfer_to = fields.Char(string='To')
        transfer_reason = fields.Text(string='Reason')