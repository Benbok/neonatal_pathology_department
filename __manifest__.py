# Copyright 2020 Artem Kostromin  <https://www.it-projects.info/team/ufaks>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": """ОПН документация""",
    "summary": """Модуль для ведения историй патологии новорожденных""",
    "category": "",
    "images": ["static/description/OPN.png"],
    "version": "3.0.0.0.1",
    "application": False,

    "author": "IT, KostrominAV",
    "website": "",
    "license": "LGPL-3",
    # "price": 9.00,
    # "currency": "EUR",

    "depends": [
        'base',
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'views/pacient_view.xml',
        'views/pathology_department_view.xml',
        'date/date_file.xml',
        'security/ir.model.access.csv',


    ],
    "css": ['static/src/css/style.css'],
    "qweb": [
    ],
    "demo": [
    ],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,

    "auto_install": False,
    "installable": True,
}
