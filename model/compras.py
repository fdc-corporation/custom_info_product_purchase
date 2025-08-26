from odoo import models, fields, api, _
from odoo.exceptions import UserError





class WizardCompras(models.TransientModel):
    _name = "wizard.compras"
    _description = "Wizard info compras"

    product_id = fields.Many2one("product.template", string="Producto")
    purchase_id = fields.Many2one("purchase.order", string="Compra", readonly=True)

    partner_id = fields.Many2one("res.partner", string="Proveedor", related="purchase_id.partner_id", store=False)
    user_id = fields.Many2one("res.users", string="Comprador", related="purchase_id.user_id", store=False)
    date_approve = fields.Datetime(string="Fecha de confirmación", related="purchase_id.date_approve", store=False)

    currency_id = fields.Many2one("res.currency", string="Moneda", related="purchase_id.currency_id", store=False)
    amount_total = fields.Monetary(string="Monto Total", related="purchase_id.amount_total", currency_field="currency_id", store=False)
    state = fields.Selection(string="Estado", related="purchase_id.state", store=False)
    company_id = fields.Many2one("res.company", string="Compañía", related="purchase_id.company_id", store=False)

    @api.model
    def default_get(self, fields_list):
        """Cuando se abre el wizard, crear registros con todas las compras del producto"""
        res = super().default_get(fields_list)
        product = self.env.context.get("default_product_id")
        print("⚡ default_get disparado, context=%s", self.env.context)
        if product:
            print("🔎 Producto recibido: %s", product)
            purchases = self.env["purchase.order"].search([
                ("order_line.product_id.product_tmpl_id", "=", product),
                # ("state", "in", "")
            ])
            print("📦 Compras encontradas: %s", purchases.ids)

            # Crear un registro por cada compra encontrada
            lines = []
            for po in purchases:
                rec = self.create({
                    "product_id": product,
                    "purchase_id": po.id,
                })
                print("✅ Creado wizard.compras con id=%s para purchase=%s", rec.id, po.id)
                lines.append(rec.id)

            # (nota: esto no se retorna desde default_get, sino desde la acción)
        else:
            print("⚠️ No se recibió default_product_id en el contexto")

        return res



    def action_view_compra(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Compras",
            "view_mode": "form",
            "res_model": "purchase.order",
            "res_id": self.purchase_id.id,
            "context": "{'create' : False}",
        }
