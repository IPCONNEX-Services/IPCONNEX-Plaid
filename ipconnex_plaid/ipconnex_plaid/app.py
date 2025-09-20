from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt 
from datetime import date, timedelta
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

def plaid_test(client_id, client_secret, access_token, days):
    # init client
    configuration = Configuration(
        host="https://sandbox.plaid.com",
        api_key={
            "clientId": client_id,
            "secret": client_secret
        }
    )
    api_client = ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)

    # calculate date range
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    # list to hold all transactions
    all_transactions = []
    offset = 0
    count = 100  # Plaid max allowed per page

    while True:
        # Build request with pagination
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date,
            options={"count": count, "offset": offset}
        )

        # Call API
        response = client.transactions_get(request).to_dict()

        # Extract transactions
        transactions = response.get("transactions", [])
        all_transactions.extend(transactions)

        # Stop if we’ve fetched everything
        if len(all_transactions) >= response.get("total_transactions", 0):
            break

        # Move to next batch
        offset += count

    return all_transactions, len(all_transactions)
