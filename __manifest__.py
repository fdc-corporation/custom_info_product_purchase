{
    'name': 'Informacion de Compras en Productos',
    'version': '1.0',
    'description': 'Con el modulo podemos acceder a la informacion de compras por productos denreo del modulo de Inventario',
    'author': 'Kauza Digital',
    'website': 'https://kauzadigital.pe/',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'base', "sale", "product", "purchase"
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/view_kanban_product.xml',
        "view/view_wizard_compras.xml",
        "view/view_form_sale_inherit.xml",
    ],
    'auto_install': False,
    'application': False,
}