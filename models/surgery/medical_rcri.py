from odoo import api, models, fields, _ 

class MedicalRcri(models.Model):
    _name = 'medical.rcri'
    _description = 'Revised Cardiac Risk Index (RCRI)'

    name = fields.Char(string='Code', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one(string='Patient', comodel_name='medical.patient', required=True, help='Patient Name')
    rcri_date = fields.Datetime(string='RCRI Date', default=fields.Datetime.now())
    physician_id = fields.Many2one(string='Health Professional', comodel_name='medical.physician')
    
    high_risk_surgery = fields.Boolean(string='High Risk Surgery')
    congestive_heart_disease = fields.Boolean(string='History of Congestive Heart Disease')
    cerebrovascular_disease = fields.Boolean(string='History of Cerebrovascular Disease')
    ischemic_heart_disease = fields.Boolean(string='History of Ischemic Heart Disease')
    preoperative_diabetes = fields.Boolean(string='Preoperative Diabetes')
    preoperative_kidney_disease = fields.Boolean(string='Preoperative Kidney Disease')
    score = fields.Integer()
    rcri_class = fields.Selection([
        ('1', 'I'),
        ('2', 'II'),
        ('3', 'III'),
        ('4', 'IV'),
    ], string='RCRI Class')

    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
        if values.get('name', 'New') == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code('medical.rcri') or 'New'
    
        result = super(MedicalRcri, self).create(values)
    
        return result