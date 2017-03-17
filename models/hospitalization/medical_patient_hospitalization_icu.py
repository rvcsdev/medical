from odoo import api, models, fields, _ 

class MedicalPatientHospitalizationIcu(models.Model):
    _name = 'medical.patient.hospitalization.icu'
    _description = 'Medical Patient Hospitalization ICU'

    name = fields.Char(string='ICU Code', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    hospitalization_id = fields.Many2one(string='Registration', comodel_name='medical.patient.hospitalization', ondelete='cascade', required=True, select=True)
    icu_admission_date = fields.Datetime(string='ICU Admission Date', default=fields.Datetime.now(), readonly=True)
    duration = fields.Char(string='Duration')
    is_admitted = fields.Boolean(string='Admitted')
    is_discharged = fields.Boolean(string='Discharged')
    is_current = fields.Boolean(string='Current')
    discharge_date = fields.Datetime(string='Date Discharged')
    ventilation_ids = fields.One2many(comodel_name='medical.patient.hospitalization.icu.ventilation', inverse_name='icu_id', string='Mechanical Ventilation History')

    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
        if values.get('name', 'New') == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code('medical.patient.hospitalization.icu') or 'New'
    
        result = super(MedicalPatientHospitalizationIcu, self).create(values)
    
        return result