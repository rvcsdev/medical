# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class MedicalLab(models.Model):
    _name = "medical.lab"
    _description = "Medical Labs"

    name = fields.Char(string='Request ID', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'), help='Unique identifier for lab.')

    request_sample_id = fields.Many2one(string='Select Sample', comodel_name='medical.lab.test.type.sample', required=True)

    test_type_id = fields.Many2one(string='Test Type', comodel_name='medical.test.type', help='Lab test type.', required=True)

    patient_id = fields.Many2one(string='Patient', comodel_name='medical.patient', ondelete='restrict', required=True)

    physician_id = fields.Many2one(string='Pathologist', comodel_name='medical.physician', help='Pathologist that performed the exam.')

    request_physician_id = fields.Many2one(string='Requesting Physician', comodel_name='medical.physician', help='Physician that requested the exam.')

    date_request = fields.Datetime(string='Date Requested', default=lambda s: fields.Datetime.now())

    date_perform = fields.Datetime(string='Date of Analysis', default=lambda s: fields.Datetime.now())

    date_receive = fields.Datetime(string='Received Date', default=lambda s: fields.Datetime.now())

    result_ids = fields.One2many(string='Test Results', comodel_name='medical.lab.test.result', inverse_name='lab_id')

    diagnosis_ids = fields.Many2many(string='Diagnoses', comodel_name='medical.pathology', help='Diagnosed pathologies as a result of this lab.')

    notes = fields.Text(string='Additional Notes')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Tested'),
        ('cancel', 'Cancelled'),
        ], readonly=True, default='draft')

    # visit_id = fields.Many2one(comodel_name='medical.visit', string='Visit', ondelete='cascade', index=True, copy=False)
    hospitalization_id = fields.Many2one(comodel_name='medical.hospitalization', string='Hospitalization', ondelete='cascade', index=True, copy=False)

    _sql_constraints = [('name_uniq', 'UNIQUE(name)', 'The test ID code must be unique')]

    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
        if values.get('name', 'New') == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code('medical.lab') or 'New'
    
        result = super(MedicalLab, self).create(values)
    
        return result

    # @api.multi
    # def action_done(self):
    #     for lab in self:
    #         lab.state = 'done'

    #     return True

    @api.multi
    def action_create_result(self):
        for record in self:
            if record.test_type_id:
                criterion_ids = self.env['medical.test.criteria'].search([('test_type_ids', '=', record.test_type_id.id)], order='sequence')
                for item in criterion_ids:
                    criteria = self.env['medical.test.criteria'].browse(item.id)
                    # criteria_id = self.env['medical.test.criteria'].browse(criteria.id)
                    if criteria.is_excluded == False: 
                        criteria_id = self.env['medical.lab.test.result'].create({
                            'criterion_id': criteria.id,
                            'name': criteria.name,
                            'sequence': criteria.sequence,
                            'lower_limit': criteria.lower_limit,
                            'upper_limit': criteria.upper_limit,
                            'uom_id': criteria.uom_id.id,
                            'is_warning': criteria.is_warning,
                            'lab_id': record.id,
                        })
                        # return True
        return True

    @api.multi
    def action_confirm_result(self):
        for record in self:
            record.state = 'done'

        return True

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancelled'})
