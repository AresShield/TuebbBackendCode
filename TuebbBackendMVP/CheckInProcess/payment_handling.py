
def check_if_enough_funds(ticket, wallet):
    if ticket.price <= wallet.balance:
        return True
    return False


def buy_ticket(ticket, consumer_wallet, venue_wallet, consumer):
    consumer_wallet.balance -= ticket.price
    venue_wallet.balance += ticket.price
    ticket.owner = consumer
    ticket.paid = True
    consumer_wallet.save()
    venue_wallet.save()
    ticket.save()
