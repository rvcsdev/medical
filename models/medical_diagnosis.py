from odoo import api, models, fields, _ 

class MedicalDiagnosis(models.Model):
    _name = 'medical.diagnosis'
    _description = 'Medical Diagnosis'

    name = fields.Char(string='Code', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    pathology_id = fields.Many2one('medical.pathology', string='Pathology', ondelete='restrict', required=True, select=True)
    notes = fields.Text(string='Notes')

    visit_id = fields.Many2one(comodel_name='medical.visit', string='Visit', ondelete='cascade', index=True, copy=False)

    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
        if values.get('name', 'New') == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code('medical.diagnosis') or 'New'
    
        result = super(MedicalDiagnosis, self).create(values)
    
        return result