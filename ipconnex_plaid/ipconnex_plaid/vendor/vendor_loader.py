# plaid_integration/vendor_loader.py
import sys, os

def use_vendor():
    """Ensure vendor libraries (like plaid v3.2.0) are loaded first"""
    vendor_path = os.path.join(os.path.dirname(__file__), "vendor")
    print(vendor_path)
    if os.path.dirname(__file__) not in sys.path:
        sys.path.insert(0, os.path.dirname(__file__))  
    if  vendor_path not in sys.path:
        sys.path.insert(0,  vendor_path)










