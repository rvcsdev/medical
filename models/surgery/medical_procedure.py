from odoo import api, models, fields, _ 

class MedicalProcedure(models.Model):
    _name = 'medical.procedure'
    _description = 'Medical Procedures'

    name = fields.Char(string='Code', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    details = fields.Text(string='Procedure Details')

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

    