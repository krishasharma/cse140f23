#!/usr/bin/env python3

"""
Based of of: http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders: [('apples', 1.0), ('oranges', 3.0)] best shop is shop1.
For orders: [('apples', 3.0)] best shop is shop2.
"""

"""
------------------------------------------------------------------------
Krisha Sharma 
CRUZ ID: krvsharm
CSE 140 Prof. Leilani Gilpin 
PA0 
shopSmart.py
------------------------------------------------------------------------
CREDIT: Please note, many of the online resources linked by Prof. Gilpin 
were refrenced throughout this programming assignment. The below code 
also makes use of starter code provided by Prof. Gilpin
------------------------------------------------------------------------
"""
# importing shop.py
import shop

# defining function shopSmart
def shopSmart(orderList, fruitShops):
    """
    orderList: List of (fruit, numPound) tuples
    fruitShops: List of FruitShops
    """
    # *** Your Code Here ***

    # the shopSmart function will have two arguments, orderList, the
    # one passed into buyLotsOfFruit, as well as fruitShops which is
    # a list of fruit shops. 
    # the function needs to return the shop where the orderList costs
    # the least amount of money. 

    """""
    pusedocode outline: 
    ------------------------------------------------------------------------
    define a var to track the cheapest shop- initialize to None
    initialize a var for the minimum cost of the order
    if there is a shop in the list fruitShops 
        initialize and set the cost equal to the cost of the orderList 
        if cost is less than the min cost and cost is not equal to NONE
            set min_cost equal to cost 
            set the cheapest shop equal to the shop being looked at 
    return the cheapest shop  
    ------------------------------------------------------------------------
    """""

    cheapest_shop = None # initialize var for the cheapest shop 
    minimium_order_cost = float('inf') # initialize var for the minimum order cost, float inf to account for bigger numbers 

    for shop in fruitShops: # for the shop in fruitShop list 
        total_cost = shop.getPriceOfOrder(orderList) # take the current shops price of the orderList and set equal to total cost 
        if total_cost < minimium_order_cost and total_cost is not None: # if the total cost is less than the minimum order cost and not none, 
            minimium_order_cost = total_cost # then, initialize minimum_order_cost with the total cost of the current shop, calculated line above 
            cheapest_shop = shop # initialize the cheapest_shop var with the current shop 

    return cheapest_shop # returns cheapest_shop in fruitShop list 


    return None

# driver function 
def main():
    dir1 = {
        'apples': 2.0,
        'oranges': 1.0
    }

    dir2 = {
        'apples': 1.0,
        'oranges': 5.0
    }

    shop1 =  shop.FruitShop('shop1', dir1)
    shop2 = shop.FruitShop('shop2', dir2)

    shops = [shop1, shop2]

    orders = [('apples', 1.0), ('oranges', 3.0)]
    print("For orders: %s the best shop is %s." % (orders, shopSmart(orders, shops).getName()))

    orders = [('apples', 3.0)]
    print("For orders: %s the best shop is %s." % (orders, shopSmart(orders, shops).getName()))

if __name__ == '__main__':
    main()