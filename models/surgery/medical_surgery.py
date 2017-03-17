from odoo import api, models, fields, _ 

class MedicalSurgery(models.Model):
    _name = 'medical.surgery'
    _description = 'Medical Surgery'

    name = fields.Char(string='Code', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one(string='Patient', comodel_name='medical.patient', required=True, select=True, help='Patient Name')
    # code = fields.Char()
    description = fields.Char()
    base_condition = fields.Many2one(string='Admission Reason', comodel_name='medical.pathology', select=True)
    surgery_classification = fields.Selection([
        ('optional', 'Optional'),
        ('required', 'Required'),
        ('urgent', 'Urgent'), 
        ('emergency', 'Emergency'),
    ])
    surgery_date_start = fields.Datetime(string='Date of Surgery')
    surgeon = fields.Many2one(string='Surgeon', comodel_name='medical.physician', select=True, help='Select surgeon.')
    anesthetist = fields.Many2one(string='Anesthetist', comodel_name='medical.physician', select=True, help='Select anesthetist.')
    operating_room = fields.Char()
    surgery_date_end = fields.Datetime(string='End of Surgery')
    duration = fields.Char()
    signed_by = fields.Many2one(string='Anesthetist', comodel_name='medical.physician', select=True)

    # Surgical Safety Checklist
    massive_bleeeding = fields.Boolean(string='Risk of Massive Bleeding')
    site_marking = fields.Boolean(string='Surgical Site Marking')
    sterility_confirmed = fields.Boolean(string='Sterility Confirmed')
    pulse_oximeter = fields.Boolean(string='Pulse Oximeter in Place')
    antibiotic_prophylaxis = fields.Boolean(string='Antibiotic Prophylaxis')

    mallampati_score = fields.Selection([
        ('class1', 'Class 1: Full visibilty of tonsils, uvula and soft palate'),
        ('class2', 'Class 2: Visibility of hard and soft palate, upper portion of tonsils and uvula'),
        ('class3', 'Class 3: Soft and hard palate and base of the uvula are visible'),
        ('class4', 'Only hard palate is visible')
    ])
    rcri = fields.Char()
    asa_ps = fields.Selection([
        ('ps1', 'PS 1: Normal healty patient'), 
        ('ps2', 'PS 2: Patients with mild systemic disease'),
        ('ps3', 'PS 3: Patients with severe systemic disease'),
        ('ps4', 'PS 4: Patients with severe systemic disease that is a constant threat to life'),
        ('ps5', 'PS 5: Moribund patients who are not expectedd to survive without the operation'),
        ('ps6', 'PS 6: A declared brain-dead patient who organs are being removed for donor purposes')
    ])

    procedure_ids = fields.One2many(string='Procedures', comodel_name='medical.surgery.procedure', inverse_name='surgery_id')

    details = fields.Text(string='Details/Incidents')
    anesthesia_report = fields.Text(string='Anesthesia Report')

    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
        if values.get('name', 'New') == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code('medical.procedure') or 'New'
    
        result = super(MedicalProcedure, self).create(values)
    
        return result
    


