{
    'name': 'Budget',
    'version': '17.0.1.0.0',
    'author': 'Piyush Sharma',
    'category': 'Budget',
    'depends': ['account_accountant'],  
    'data': [
        'security/ir.model.access.csv',
        'views/budget_view.xml',
        'views/budget_menu.xml',
        'wizard/wizard.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
