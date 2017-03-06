from odoo import api, models, fields, _ 

class MedicalVisitInvoice(model.Model):
    _name = 'medical.visit.invoice'
    _description = 'Medical Visit Invoice'

    name = fields.Char()
    partner_invoice_id = fields.Many2one('res.partner', string='Invoice Address', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Invoice address for current visit.")
    partner_shipping_id = fields.Many2one('res.partner', string='Delivery Address', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Delivery address for current visit.")

    @api.multi
    def _create_invoice(self):
        visit = self.env['medical.visit'].browse(self._context.get('active_ids', []))
        inv_obj = self.env['account.invoice']
        ir_property_obj = self.env['ir.property']

        invoice = inv_obj.create({
            'name': self.name,
            'origin': self.name,
            'type': 'out_invoice',
            'reference': False,
            'account_id': self.patient_id.property_account_receivable_id.id,
            'partner_id': self.patient_id.partner_invoice_id.id,
            'partner_shipping_id': self.patient_id.partner_shipping_id.id,
            # 'invoice_line_ids': [(0, 0, {
            #     'name': name,
            #     'origin': order.name,
            #     'account_id': account_id,
            #     'price_unit': amount,
            #     'quantity': 1.0,
            #     'discount': 0.0,
            #     'uom_id': self.product_id.uom_id.id,
            #     'product_id': self.product_id.id,
            #     'sale_line_ids': [(6, 0, [so_line.id])],
            #     'invoice_line_tax_ids': [(6, 0, tax_ids)],
            #     'account_analytic_id': order.project_id.id or False,
            # })],
            'currency_id':self.patient_id.pricelist_id.currency_id.id,
            'payment_term_id': self.patient_id.payment_term_id.id,
            'fiscal_position_id': self.patient_id.fiscal_position_id.id or self.patient_id.partner_id.property_account_position_id.id,
            'team_id': self.patient_id.team_id.id,
            'comment': self.patient_id.note,
        })
        invoice.compute_taxes()
        invoice.message_post_with_view('mail.message_origin_link',
                    values={'self': invoice, 'origin': order},
                    subtype_id=self.env.ref('mail.mt_note').id)
        return invoice