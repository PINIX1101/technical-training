# -*- coding: utf-8 -*-
{
    'name': "Fajar Academy",

    'summary': "An Academy Module",

    'description': """
This Module is use for Arkana Training
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts'],
    'installable': True,

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/course_data.xml',

        'views/menu.xml',
        'views/course.xml',
        'views/session.xml',
        'views/res_partner.xml',
        'views/partner_categories.xml',
        'views/views.xml',
        'views/templates.xml',

        'wizards/add_attendees.xml',

        'report/session_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

