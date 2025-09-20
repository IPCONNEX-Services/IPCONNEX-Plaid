from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt 
from datetime import date
import json
from ipconnex_plaid.ipconnex_plaid.vendor_loader import use_vendor
use_vendor()
from plaid.api import plaid_api
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.products import Products
from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from plaid.model.transactions_get_request import TransactionsGetRequest



@frappe.whitelist(allow_guest=True) 
def plaid_test(client_id,client_secret,access_token):
    # init client (dummy credentials just for example)
    configuration = Configuration(
        host="https://sandbox.plaid.com",
        api_key={
            "clientId": client_id ,
            "secret": client_secret
        }
    )
    api_client = ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)
    # Build request
    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=date(2020, 9, 1),   
        end_date=date(2025, 9, 15),   
    )
    # Call API
    response = client.transactions_get(request)
    # Parse transactions
    transactions = response['transactions']
    return [t.to_dict() for t in transactions ]
