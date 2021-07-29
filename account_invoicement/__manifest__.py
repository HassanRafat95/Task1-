{
    "name":"account invorcement",
    "author":"hassan raafat ",
    "summary":"this module update purchase",
    "depends":['purchase'],
    "data":
        [
            "security/ir.model.access.csv",
            "security/partner_invoice_total_group.xml",
            "views/purchase_order.xml",
            "views/product_category.xml",
            "views/product_template.xml",
            "views/res_partner.xml",
            "data/cron_total_invoice.xml",
            "data/call_cron_functions.xml",

        ],
}
