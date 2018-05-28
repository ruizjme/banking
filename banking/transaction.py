
class Transaction(object):

  def __init__(self, date, amount, description, card):
    self.date = date
    self.amount = amount
    self.description = description
    self.card = card
