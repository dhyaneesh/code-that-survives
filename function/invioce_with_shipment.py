# Small, Single-Responsibility Functions

def calculate_tax(price, rate=0.05):
    """Only calculates tax."""
    return price * rate

def calculate_discount(price, is_premium=False):
    """Only calculates discount logic."""
    if is_premium and price > 500:
        return price * 0.1
    return 0

def calculate_shipping(total_price):
    """Only handles shipping rules."""
    return 0 if total_price > 1000 else 40

# The Orchestrator

def get_final_invoice(price, is_premium=False):
    """Coordinates the other functions to build a result."""
    
    tax = calculate_tax(price)
    discount = calculate_discount(price, is_premium)
    
    # Sub-total before shipping
    sub_total = price + tax - discount
    
    shipping = calculate_shipping(sub_total)
    
    return sub_total + shipping

# Execution
print(f"Standard Total: {get_final_invoice(800, is_premium=False)}")
print(f"Premium Total: {get_final_invoice(800, is_premium=True)}")