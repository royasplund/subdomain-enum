#!/usr/bin/env python3
import sys
import signal
import argparse
import requests
from multiprocessing import Pool

parser = argparse.ArgumentParser()
parser.add_argument("domain", metavar="domain", type=str, help="domain to be enumerated for subdomains")
args = parser.parse_args()

sub_list = open("subdomains.txt").read()
subdomains = sub_list.splitlines()
lista = []

for each in subdomains:
    lista.append(f"http://{each}.{args.domain}")


def sub_enum(sub_domains):
        try:
            requests.get(sub_domains)
        except requests.ConnectionError:
            pass
        else:
            print(sub_domains)

def signal_handler(sig, frame):
  print('Received interrupt')
  sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    with Pool(2) as p:
      try:
          p.map(sub_enum, lista)
      except KeyboardInterrupt:
          print('Received keyboard interrupt, closing')
