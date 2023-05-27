# -*- coding: utf-8 -*-
{
    'name': "pdca",

    'summary': """
        PDCA MODULE
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Allal",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'pdca',
    'version': '0.1',
    'installable': True,
    # any module necessary for this one to work correctly
    'depends': ['base','mail','contacts'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/security_rules.xml',
        'views/direction_view.xml',
        'views/unite_view.xml',
        'views/processus_view.xml',
        'views/constat_view.xml',
        # 'views/origine_view.xml',
        # 'views/type_constat_view.xml',
        'views/templates.xml',
        'views/action_view.xml',
        'views/affectation_pilote_view.xml',
        'views/employe_view.xml',
        'data/constat_sequence.xml',
        'data/constat_mails.xml',
        'data/action_mails.xml',
        'data/affectation_pilote_mails.xml',
        'data/affectation_direction_pilote_mails.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
