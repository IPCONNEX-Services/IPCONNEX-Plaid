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
def plaid_test(client_id,client_secret):
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
    # Call a simple Plaid method (e.g., categories)
    sandbox_request = SandboxPublicTokenCreateRequest(
        institution_id="ins_109508",  # Example sandbox institution
        initial_products=[Products("transactions")]  # ✅ Use Products enum instead of string
    )
    public_response = client.sandbox_public_token_create(sandbox_request)
    public_token=public_response["public_token"]
    return public_token

