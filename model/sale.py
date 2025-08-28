from odoo import models, api, fields, _
from odoo.exceptions import UserError



class Producto (models.Model):
    _inherit = "sale.order.line"
    _description = "Ventas"


    def view_wizard_purchase(self):
        purchases = self.env["purchase.order"].search([
            ("order_line.product_id.product_tmpl_id", "=", self.product_template_id.id)
        ])
        lines = []
        for po in purchases:
            rec = self.env["wizard.compras"].create({
                "product_id": self.product_template_id.id,
                "purchase_id": po.id,
            })
            lines.append(rec.id)

        return {
            "name": f"Información de {self.product_template_id.default_code}",
            "type": "ir.actions.act_window",
            "res_model": "wizard.compras",
            "view_mode": "tree,form",
            "target": "new",
            "domain": [("id", "in", lines)],
        }