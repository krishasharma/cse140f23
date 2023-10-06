#!/usr/bin/env python3

"""
Based off of: http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

To run this script, type:

  python3 buyLotsOfFruit.py

Once you have correctly implemented the buyLotsOfFruit function,
the script should produce the output:

Cost of [('apples', 2.0), ('pears', 3.0), ('limes', 4.0)] is 12.25
"""

"""
------------------------------------------------------------------------
Krisha Sharma 
CRUZ ID: krvsharm
CSE 140 Prof. Leilani Gilpin 
PA0 
buyLotsOfFruit.py
------------------------------------------------------------------------
CREDIT: Please note, many of the online resources linked by Prof. Gilpin 
were refrenced throughout this programming assignment. The below code 
also makes use of starter code provided by Prof. Gilpin
------------------------------------------------------------------------
"""



FRUIT_PRICES = {
    'apples': 2.00,
    'oranges': 1.50,
    'pears': 1.75,
    'limes': 0.75,
    'strawberries': 1.00
}

# defining function buyLotsOfFruit
def buyLotsOfFruit(orderList):
    """
    orderList: List of (fruit, weight) tuples

    Returns cost of order
    """
    
    # *** Your Code Here ***

    # function will take in a list of (fruit, weight) tuples and returns
    # the cost of that list. 
    # should there be fruit on the list that does not appear, the 
    # function prints an error msg and will then return NONE. 
    # DO NOT MODIFY THE FRUIT_PRICES DICT. 
    # under FRUIT_PRICES, we see fruits and their prices 

    """""
    pusedocode outline: 
    ------------------------------------------------------------------------
    initialize an order cost var to return at the end of func. 
        if the fruit is in the orderList
            then the weight per fruit is equal to the price of the fruit
            need to add to the total cost somehow to track 
        else 
        print out some type of error message becuase the fruit is not
        in the FRUIT_PRICES list
        return NONE 
    return the cost of all the fruit 
    ------------------------------------------------------------------------
    """""
    
    order_cost = 0.0 

    for fruit, weight in orderList: # looks at orderList to see fruit and weight
        if fruit in FRUIT_PRICES: # checks if fruit in orderList is also in FRUIT_PRICES 
            cost = FRUIT_PRICES[fruit] # if it is, then set the cost of fruit equal to fruit based off of FRUIT_PRICES
            order_cost += cost * weight # update order_cost by mulitplying the cost by the weight of the fruit to get the total price for the fruit
        else: # otherwise (if any fruit is not in the FRUIT_PRICES list)
            print(f"Error! {fruit} is not in the FRUIT_PRICES list!") # print out an error message
            return None # return NONE

    return order_cost # return the cost of the orderList 

# driver function 
def main():
    orderList = [
        ('apples', 2.0),
        ('pears', 3.0),
        ('limes', 4.0)
    ]

    print("Cost of %s is %s." % (orderList, buyLotsOfFruit(orderList)))

if __name__ == '__main__':
    main()