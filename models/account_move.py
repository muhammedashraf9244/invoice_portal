from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _create_invoices_automatic(self):
        partner = self.env['res.partner'].search([
            ('id', '=', self.env.ref('base.partner_admin').id)
        ])
        current_date = date.today()
        product_a = self.env['product.product'].create({
            'name': 'product_a',
            'uom_id': self.env.ref('uom.product_uom_unit').id,
            'lst_price': 1000.0,
            'standard_price': 800.0,
        })
        product_b = self.env['product.product'].create({
            'name': 'product_b',
            'uom_id': self.env.ref('uom.product_uom_unit').id,
            'lst_price': 100550.0,
            'standard_price': 800522.0,
        })
        if partner:
            day = 1
            for _ in range(200):
                invoice_vals = ({
                    'move_type': 'out_invoice',
                    'partner_id': partner.id,
                    'invoice_date': current_date + relativedelta(days=day),
                    'invoice_line_ids': [
                        (0, None, {
                            'product_id': product_a.id,
                            'quantity': 3,
                            'price_unit': 750,
                        }),
                        (0, None, {
                            'product_id': product_b.id,
                            'quantity': 1,
                            'price_unit': 3000,
                        }),
                    ]
                })
                day += 1
                self.create(invoice_vals)
