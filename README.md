# Vehicle Route Planner for Scout Mulch Delivery

This is currently a very naive attempt at solving a CVRP problem for Boy Scouts delivering mulch.

## Dependencies

1. webkit2png - This is used to generate the map images used by the drivers to see the route, install from http://www.paulhammond.org/webkit2png/
2. fpdf - This is used to generate the PDF documents used by the drivers, install using: pip install fpdf 
3. googlemaps - This is used to geocode the addresses and optimize routes, install using: pip install googlemaps

You'll also need a Google Developers' API key which you can obtain from https://console.developers.google.com/apis

## Running

It expects a CSV file with the following columns: 'ID', 'Name', 'BagCount', 'Address1', 'Address2', 'City', 'State', 'Zip', 'Notes', Lat', 'Lng', 'OriginDist'.

```
$ ./mulchplanner.py orders.csv
```
