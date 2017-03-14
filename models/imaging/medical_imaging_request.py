from odoo import api, models, fields, _

class MedicalImagingRequest(models.Model):
    _name = 'medical.imaging.request'
    _description = 'Medical Imaging Request'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    # name = fields.Char(string='Order Reference')
    test_date = fields.Datetime(string='Test Date', required=True)
    patient_id = fields.Many2one(string='Patient', comodel_name='medical.patient', required=True, select=True, help='Patient Name')
    physician_id = fields.Many2one(string='Physician', comodel_name='medical.physician', required=True, select=True, help='Physician Name')
    is_urgent = fields.Boolean(string='Urgent', default=False)
    test_ids = fields.Many2many(string='Tests', comodel_name='medical.imaging.test', help='Tests to be conducted.')
    state = fields.Selection([
        ('draft', 'Draft'), 
        ('confirmed', 'Confirmed'), 
        ('done', 'Done'), 
        ('cancelled', 'Cancelled')
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    notes = fields.Text(string='Notes')

    # visit_id = fields.Many2one(comodel_name='medical.visit', string='Visit', ondelete='cascade', index=True, copy=False)
    hospitalization_id = fields.Many2one(comodel_name='medical.hospitalization', string='Hospitalization', ondelete='cascade', index=True, copy=False)

    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
        if values.get('name', 'New') == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code('medical.imaging.request') or 'New'
    
        result = super(MedicalImagingRequest, self).create(values)
    
        return result

    @api.multi
    def action_confirm(self):
        for imaging in self:
            imaging.state = 'confirmed'

        return True

    @api.multi
    def action_create_result(self):
        for imaging in self:
            imaging.state = 'done'

        return True

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancelled'})
    

class MedicalImagingRequestResult(models.Model):
    _name = 'medical.imaging.request.result'
    _description =  'Medical Imaging Request Result'

    name = fields.Char(string='Result Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    result_date = fields.Char(string='Result Date', required=True, copy=False, readonly=True, index=True, default=fields.Datetime.now)
    imaging_request_id = fields.Many2one(string='Test Request', comodel_name='medical.imaging.request', required=True, select=True)
    # attachment_ids = fields.One2many(string='Images', comodel_name='medical.imaging.request.result.attachment', inverse_name='request_result_id', help='Attach files/images for test result reference')

# class MedicalImagingRequestResultAttachment(models.Model):
#     _name = 'medical.imaging.request.result.attachment'
#     _description = 'Medical Imaging Request Result Attachment'

#     name = fields.Char(string='Attachment Name')
#     attachment_file = fields.Binary(string='Upload File/Image', attachment=True)
#     request_result_id = fields.Many2one(string='Request Result', comodel_name='medical.imaging.request.result', ondelete='cascade')

