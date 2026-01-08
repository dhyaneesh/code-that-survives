# Small, Single-Responsibility Functions ---

def calculate_tax(price, rate=0.05):
    """Only calculates tax."""
    return price * rate

def calculate_discount(price, is_premium=False):
    """Only calculates discount logic."""
    if is_premium and price > 500:
        return price * 0.1
    return 0

# The Orchestrator

def get_final_invoice(price, is_premium=False):
    """Coordinates the other functions to build a result."""
    
    tax = calculate_tax(price)
    discount = calculate_discount(price, is_premium)
    
    # total
    total = price + tax - discount
    
    return total 

# Execution
print(f"Standard Total: {get_final_invoice(800, is_premium=False)}")
print(f"Premium Total: {get_final_invoice(800, is_premium=True)}")