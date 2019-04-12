# -*- coding: utf-8 -*-

{
    'name': 'Almacén con Kits',
    'version': '1.0',
    'category': 'Stock',
    "": "'sequence': ''",
    'summary': 'Almacén, Productos',
    'description': """""",
    'website': 'https://desiteg.com/portal/',
    'author': 'Desiteg-Tinny',
    'depends': ['base', 'stock', 'esferica'],
    'data': [
        'views/product_kits_views.xml',
        'views/inherit_stock_location_form.xml',
        'wizard/kit_do_stock_wizard.xml',
        'wizard/kit_move_stock_wizard.xml',
        'wizard/kit_remove_stock_wizard.xml'
    ],
    "": "'test': []",
    "": "'demo': []",
    'installable': True,
    'auto_install': False,
    'application': True
}
