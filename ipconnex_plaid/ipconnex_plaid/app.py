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
def getTransactions(client_id, client_secret, access_token, days, mode="sandbox"):
    # choose environment
    hosts = {
        "sandbox": "https://sandbox.plaid.com",
        "development": "https://development.plaid.com",
        "production": "https://production.plaid.com",
    }
    host = hosts.get(mode.lower(), "https://sandbox.plaid.com")  # fallback sandbox
    # init client
    configuration = Configuration(
        host=host,
        api_key={
            "clientId": client_id,
            "secret": client_secret
        }
    )
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
    start_date = end_date - timedelta(days=int(days))

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

    return all_transactions

@frappe.whitelist() 
def loadTransactions(doc,method):
    days_count = (date.today() - date(2020, 1, 1)).days
    plaid_account=frappe.get_doc("Plaid Account",doc.name)
    transactions =getTransactions(
            client_id=plaid_account.get_password("client_id"), 
            client_secret=plaid_account.get_password("client_secret"), 
            access_token=plaid_account.get_password("access_token"), 
            days=days_count, 
            mode=plaid_account.account_type)
    for transaction in transactions :
        try:
            t_date=date.today()
            if transaction["date"]:
                t_date=transaction["date"]
            t_confidence = "UNKNOWN"
            t_detailed = ""
            t_icon=""
            if transaction["personal_finance_category"]:
                if transaction["personal_finance_category"]["confidence_level"]:
                    t_confidence=transaction["personal_finance_category"]["confidence_level"]
                if transaction["personal_finance_category"]["detailed"]:
                    t_detailed=transaction["personal_finance_category"]["detailed"]
            if len(transaction["counterparties"]):
                if transaction["counterparties"][0]["logo_url"]:
                    t_icon=transaction["counterparties"][0]["logo_url"]
            data={
                "account":pa["name"],
                "account_id":transaction["account_id"],
                "transaction_id":transaction["transaction_id"],
                "transaction_type":"Debit" if  transaction["amount"] < 0 else "Credit",
                "transaction_icon":t_icon,
                "category":",".join(transaction["category"]),
                "amount":transaction["amount"],
                "currency":transaction["iso_currency_code"],
                "date":t_date.strftime("%Y-%m-%d") , 
                "merchant_entity_id":transaction["merchant_entity_id"],
                "merchant_name":transaction["merchant_name"],
                "confidence_level":t_confidence,
                "detailed":t_detailed, 
                "pending":transaction["pending"],
                "website":transaction["website"]
            }
            if frappe.db.exists("Plaid Transaction", transaction["transaction_id"]):
                for field, value in data.items():
                    frappe.db.set_value("Plaid Transaction", transaction["transaction_id"], field, value)
            else:
                data["doctype"]="Plaid Transaction"
                doc = frappe.get_doc(data)
                doc.insert()
        except :
            pass




def autoUpdatePlaid():
    plaid_accounts=frappe.get_all("Plaid Account",fields=["name"],filters={"status": "Active"})
    for pa in plaid_accounts : 
        try :
            plaid_account=frappe.get_doc("Plaid Account",pa["name"])
            transactions =getTransactions(
                    client_id=plaid_account.get_password("client_id"), 
                    client_secret=plaid_account.get_password("client_secret"), 
                    access_token=plaid_account.get_password("access_token"), 
                    days=plaid_account.refresh_days, 
                    mode=plaid_account.account_type)
            for transaction in transactions :
                
                try :
                    t_date=date.today()
                    if transaction["date"]:
                        t_date=transaction["date"]
                    t_confidence = "UNKNOWN"
                    t_detailed = ""
                    t_icon=""
                    if transaction["personal_finance_category"]:
                        if transaction["personal_finance_category"]["confidence_level"]:
                            t_confidence=transaction["personal_finance_category"]["confidence_level"]
                        if transaction["personal_finance_category"]["detailed"]:
                            t_detailed=transaction["personal_finance_category"]["detailed"]
                    if len(transaction["counterparties"]):
                        if transaction["counterparties"][0]["logo_url"]:
                            t_icon=transaction["counterparties"][0]["logo_url"]
                    data={
                        "account":pa["name"],
                        "account_id":transaction["account_id"],
                        "transaction_id":transaction["transaction_id"],
                        "transaction_type":"Debit" if  transaction["amount"] < 0 else "Credit",
                        "transaction_icon":t_icon,
                        "category":",".join(transaction["category"]),
                        "amount":transaction["amount"],
                        "currency":transaction["iso_currency_code"],
                        "date":t_date.strftime("%Y-%m-%d") , 
                        "merchant_entity_id":transaction["merchant_entity_id"],
                        "merchant_name":transaction["merchant_name"],
                        "confidence_level":t_confidence,
                        "detailed":t_detailed, 
                        "pending":transaction["pending"],
                        "website":transaction["website"]
                    }
                    if frappe.db.exists("Plaid Transaction", transaction["transaction_id"]):
                        for field, value in data.items():
                            frappe.db.set_value("Plaid Transaction", transaction["transaction_id"], field, value)
                    else:
                        data["doctype"]="Plaid Transaction"
                        doc = frappe.get_doc(data)
                        doc.insert()        
                except :
                    pass
        except :
            pass

