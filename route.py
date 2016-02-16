import googlemaps

class Router:
  def __init__(self, orders, deliveries, config):
    self.config = config
    self.client = googlemaps.Client(config['api_key'])
    self.orders = orders
    self.deliveries = deliveries

  def routes(self):
    routes = []
    for d in self.deliveries:
      for idx, val in enumerate(d):
        order = self.find_order_by_id(val)
        d[idx] = order
      routes.append(d)
    return routes

  def find_order_by_id(self, id):
    for order in self.orders:
      if order['ID'] == id:
        return order
    return None
