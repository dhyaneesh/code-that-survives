
# Problem: Global Variables 
is_premium_member = True
location = "USA"
items_in_cart = [800, 150, 40] 

def calculate_everything():
    global is_premium_member
    total = 0
    
    for price in items_in_cart:
        # Problem : Hardcoded Logic
        tax = price * 0.05 
        
        # Problem : Hidden Dependencies 
        if location == "USA":
            tax = price * 0.08
            
        # Problem : Tangled Logic 
        if is_premium_member and price > 500:
            discount = price * 0.1
        else:
            discount = 0
            
        # Problem : Side Effects 
        #(Modifying variables outside the loop)
        total += (price + tax - discount)

    # Problem 5: Lack of Flexibility 
    #(What if we add shipping?)
    if total < 1000:
        total += 40 
        
    print(f"Final Amount: {total}")

calculate_everything()