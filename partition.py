from geopy.distance import great_circle
from collections import OrderedDict
from operator import itemgetter
import googlemaps
import csv

class Partitioner:
  def __init__(self, addresses, config):
    self.config = config
    self.client = googlemaps.Client(self.config['api_key'])
    self.res = self.geocode_addresses(addresses)
    self.save_csv(self.res, config['output_dir'])
    self.adjacencies = {}
    self.planned_deliveries = []

  def orders(self):
    return self.res

  def calculate_deliveries(self):
    deliveries = []
    for d in self.res:
      if not d['ID'] in self.adjacencies:
        self.adjacencies[d['ID']] = {}
      for n in self.res:
        if d['ID'] == n['ID']: continue
        distance = great_circle((d['Lat'],d['Lng']), (n['Lat'],n['Lng'])).miles
        self.adjacencies[d['ID']][n['ID']] = distance
    # Now that we've calculated all of the adjacencies, let's order them by distance
    for a in self.adjacencies:
      self.adjacencies[a] = sorted(self.adjacencies[a].items(), key=itemgetter(1))
    self.save_adjacencies(self.config['output_dir'])
    # Now that each adjacency list is ordered, let's work through the deliveries
    for a in self.res:
      # Look up the ID in self.res
      if not self.in_delivery_zone(a['Zip']): 
        print "Order %s (in %s) not in delivery zone, skipping." % (a['ID'], a['Zip'])
        continue
      if a['ID'] in self.planned_deliveries: continue
      deliveries.append(self.chunk_deliveries(a))
    return deliveries

  def chunk_deliveries(self, order):
    result = [order['ID']]
    # For now assume 200 bags per truck
    count = 200 - int(order['BagCount'])
    if count < 0:
      print "WARNING: Order %s is %d bags, which won't fit on one truck." % (order['ID'], int(order['BagCount']))
    for n in self.adjacencies[order['ID']]:
      if n[0] in self.planned_deliveries: continue
      other = self.find_order_by_id(n[0])
      if other == None:
        print "WTF?"
        continue
      if self.in_delivery_zone(other['Zip']):
        bags = int(other['BagCount'])
        if count - bags > 0:
          result.append(other['ID'])
          count = count - bags
        else:
          break
    self.planned_deliveries.extend(result)
    return result

  def find_order_by_id(self, id):
    for order in self.res:
      if order['ID'] == id:
        return order
    return None

  def geocode_addresses(self, addresses):
    results = []
    for row in addresses:
      if row['Zip'].startswith('\''):
        row['Zip'] = row['Zip'][1:]
      nrow = self.geocode(row)
      nrow['OriginDist'] = great_circle(self.config['origin'], (nrow['Lat'],nrow['Lng'])).miles
      results.append(nrow)
    return list(reversed(sorted(results, key=lambda x: x['OriginDist'])))

  def geocode(self, addr):
    if addr['Lat'] == '' or addr['Lng'] == '':
      geo_result = self.client.geocode(self.assemble_address(addr))
      # print geo_result
      addr['Lat'] = geo_result[0]['geometry']['location']['lat']
      addr['Lng'] = geo_result[0]['geometry']['location']['lng']
    return addr

  def assemble_address(self, addr):
    return "%s %s, %s, %s %s" % (addr['Address1'], addr['Address2'],
      addr['City'], addr['State'], addr['Zip'])

  def save_csv(self, data, outdir):
    with open(outdir + '/data.csv', 'wb') as f:
      w = csv.DictWriter(f, ['ID','Name','BagCount','Address1','Address2','City','State','Zip','Notes','Lat','Lng','OriginDist'],extrasaction='ignore')
      w.writeheader()
      w.writerows(data)

  def save_adjacencies(self, outdir):
    keys = sorted(self.adjacencies.keys())
    with open(outdir + '/adjacencies.csv', 'wb') as f:
      f.write("ID,%s\n" % (",".join(keys)))
      for a in self.adjacencies:
        f.write("%s," % (a))
        for key in keys:
          if a == key:
            f.write("0,")
          else:
            f.write("%s," % (self.find_adjacency(key,self.adjacencies[a])))
        f.write("\n")

  def find_adjacency(self,key,adjacencies):
    for f in adjacencies:
      if f[0] == key:
        return f[1]

  def in_delivery_zone(self, zipcode):
    return int(zipcode[:5]) in self.config['delivery_zone']