{
    "name":"purchase request",
    "author":"hassan raafat ",
    "summary":"this module update purchase",
    "depends":['purchase'],
    "data":[
        "security/ir.model.access.csv",
        'views/Purchase_Request.xml',
        'views/Purchase_Request_line.xml',
        'views/purchase_order.xml',
        'wizard/wizard_reject_view.xml',
        'data/request_template_mail.xml',
        'data/purchase_request_data.xml',
        'reports/purchase_request_report.xml',
        'reports/purchase_request_template_report.xml',
    ],


}
