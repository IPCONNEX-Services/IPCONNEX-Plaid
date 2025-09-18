# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "ipconnex_plaid"
app_title = "IPCONNEX Plaid"
app_publisher = "Frappe"
app_description = "A Plaid module created by IPCONNEX"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "voip@ipconnex.com"
app_license = "MIT"




# Scheduled Tasks
# ---------------

scheduler_events = {
    "hourly": [
        "ipconnex_plaid.ipconnex_plaid.payement.hourly_process_payment",
    ]
}

#app_install = "ipconnex_stripe_payment.ipconnex_stripe_payment.payement.setup_install"

