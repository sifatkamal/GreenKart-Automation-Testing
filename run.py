from order.order import Order


with Order() as bot:

    bot.land_first_page()

    bot.cart()

    bot.placeorder()

