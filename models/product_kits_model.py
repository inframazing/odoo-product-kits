# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning
# import logging


class InheritProductProduct(models.Model):
    _inherit = "product.product"

    is_kit_item = fields.Boolean(default=False)


class ProductKit(models.Model):
    _name = "product.kits"
    _rec_name = "description"

    _sql_constraints = [
        ('serial_number_unique',
         'unique(serial_number)',
         'No pueden existir IDs iguales'
         )
    ]
    serial_number = fields.Char(string="Num. de Serie / ID")

    product_type_id = fields.Many2one(
        "product.product",
        domain="[('is_kit_item', '=', True)]",
        required=True)  # Software, Equipo, Accesorio, etc
    description = fields.Char(string="Descripción", required=True)
    category = fields.Selection([
        ('software', 'Software'),
        ('equipment', 'Equipo Médico'),
        ('accessory', 'Accesorio')
    ], required=True)
    accessory_ids = fields.One2many("product.kits", "parent_id", string="Accesorios")
    parent_id = fields.Many2one("product.kits")
    tracking = fields.Selection(related="product_type_id.tracking")
    state = fields.Selection([
        ('draft', 'Capturado'),
        ('on_hand', 'En Almacén'),
        ('external', 'Ubicación Externa'),
        ('transit', 'En Tránsito'),
        ('delivered', 'Entregado'),
        ('sale', 'Vendido')
    ], default="draft", required=True)
    partner_id = fields.Many2one("res.partner")
    stock_move_ids = fields.Many2many("stock.move")
    warehouse_hall = fields.Char(string="Pasillo")
    warehouse_rack = fields.Char(string="Estante")

    location_id = fields.Many2one("stock.location")

    reference_number = fields.Char(string="Número de Referencia:")
    entry_date = fields.Datetime(string="Fecha de Ingreso:")

    @api.multi
    def do_stock(self):
        return{
            'type': 'ir.actions.act_window',
            'res_model': 'kit.do.stock.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': False,
            'target': 'new',
            'context': {
                'default_kit_id': self.id
            }
        }

    @api.multi
    def move_stock(self):
        return{
            'type': 'ir.actions.act_window',
            'res_model': 'kit.move.stock.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': False,
            'target': 'new',
            'context': {
                'default_kit_id': self.id,
                'default_location_id': self.location_id.id
            }
        }

    @api.multi
    def remove_stock(self):
        return{
            'type': 'ir.actions.act_window',
            'res_model': 'kit.remove.stock.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': False,
            'target': 'new',
            'context': {
                'default_kit_id': self.id,
                'default_location_id': self.location_id.id
            }
        }

    @api.multi
    def unlink(self):
        for kits in self:
            if kits.state != 'draft':
                raise Warning('No se puede eliminar el Kit')
        return super(ProductKit, self).unlink()


class InheritStockLocation(models.Model):
    _inherit = "stock.location"

    is_demo_location = fields.Boolean(default=False)
