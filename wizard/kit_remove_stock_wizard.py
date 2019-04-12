# -*- coding: utf-8 -*-

from odoo import models, fields, api


class KitRemoveStockWizard(models.TransientModel):
    _name = "kit.remove.stock.wizard"

    kit_id = fields.Many2one("product.kits", string="Kit")
    location_id = fields.Many2one("stock.location")

    def kit_remove_stock_wizard(self):
        moves = []
        move_products = self.env["stock.move"].create(dict(
            name=self.kit_id.description,
            product_id=self.kit_id.product_type_id.id,
            product_uom_qty=1,
            location_id=self.location_id.id,
            location_dest_id=self.kit_id.partner_id.property_stock_supplier.id,
            product_uom=self.kit_id.product_type_id.uom_id.id,
            origin=self.kit_id.description
        ))

        moves.append((4, move_products.id, False))

        move_products.force_assign()
        move_products.action_done()

        for acc in self.kit_id.accessory_ids:
            move_acc = self.env["stock.move"].create(dict(
                name=acc.description,
                product_id=acc.product_type_id.id,
                product_uom_qty=1,
                location_id=self.location_id.id,
                location_dest_id=self.kit_id.partner_id.property_stock_supplier.id,
                product_uom=acc.product_type_id.uom_id.id,
                origin=self.kit_id.description
            ))

            moves.append((4, move_acc.id, False))

            move_acc.force_assign()
            move_acc.action_done()

        self.kit_id.stock_move_ids = moves
        self.kit_id.state = "delivered"
        self.kit_id.location_id = self.kit_id.partner_id.property_stock_supplier.id
