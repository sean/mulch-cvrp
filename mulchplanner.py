#!/usr/bin/env python

import partition
import os.path
import urllib
import route
import mypdf
import json
import csv
import sys

def ensure_file_exists(filename):
  if not os.path.isfile(filename):
    print "No such file! " + filename
    sys.exit(-1)

class MulchPlanner:
  def __init__(self, filename, config):
    self.data   = self.load_csv(filename)
    self.config = self.load_config(config)

  def process(self):
    # First calculate the deliveries based on distance
    p = partition.Partitioner(self.data, self.config)
    groups = p.calculate_deliveries()
    # Second calculate the routes based on the deliveries
    r = route.Router(p.orders(), groups, self.config)
    routes = r.routes()
    # TODO process the routes and write them to files
    for idx, d in enumerate(routes):
      self.generate_pdf("Route-%d" % (idx+1), d)

  # private functions

  def generate_pdf(self, title, r):
    url  = self.url_for_route(r)
    bags = self.total_bags(r)
    os.system("webkit2png -D %s -o %s -F -W 1440 -H 900 \"%s\"" % (self.config['output_dir'], title, url))
    filename = "%s/%s-full.png" % (self.config['output_dir'], title)
    pdf = mypdf.MyFPDF()
    pdf.add_page()
    pdf.write_html(self.gen_html(title, bags, r, filename))
    pdf.output("%s/%s.pdf" % (self.config['output_dir'], title),'F')
    print title,"(",bags,"):",url

  def gen_html(self, title, bags, r, img):
    html = """
    <h1 align="center">%s (%s bags)</h1>
    <center>
    <img src="%s" width="480" height="320">
    </center>
    <hr />
    <ol>""" % (title, bags, img)
    for order in r:
      html += "<li>%s (%s bags)</li>" % (self.address_for_order(order), order['BagCount'])
    html += "</ol>"
    return html

  def url_for_route(self, route):
    url = "http://maps.google.com/maps?f=d&source=s_d&saddr="
    for idx, order in enumerate(route):
      if idx == 0:
        url += urllib.quote_plus(self.address_for_order(order))
        url += "&daddr="
      else:
        if idx != 1:
          url += "%20to:"
        url += urllib.quote_plus(self.address_for_order(order))
    return url

  def address_for_order(self, order):
    return "%s %s %s, %s %s" % (order['Address1'],order['Address2'],order['City'],order['State'],order['Zip'])

  def total_bags(self, route):
    bags = 0
    for order in route:
      bags = bags + int(order['BagCount'])
    return bags

  def load_csv(self, filename):
    addresses = []
    ensure_file_exists(filename)
    with open(filename, "rU") as data_file:
      for row in csv.DictReader(data_file):
        addresses.append(row)
    return addresses

  def load_config(self, filename):
    cfg = {}
    ensure_file_exists(filename)
    with open(filename) as config_file:
      cfg = json.load(config_file)
    # Fix origin
    cfg['origin'] = (cfg['origin'][0],cfg['origin'][1])
    return cfg

if __name__ == '__main__':
  data_file = sys.argv[1]
  mp = MulchPlanner(data_file, 'config.json')
  mp.process()
