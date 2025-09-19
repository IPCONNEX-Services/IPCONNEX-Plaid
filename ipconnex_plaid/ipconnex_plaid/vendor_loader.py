# plaid_integration/vendor_loader.py
import sys, os

def use_vendor():
    vendor_path = os.path.join(os.path.dirname(__file__), "vendor")
    """
    if os.path.dirname(__file__) not in sys.path:
        sys.path.insert(0, os.path.dirname(__file__))  """
    if  vendor_path not in sys.path:
        sys.path.insert(0,  vendor_path)










