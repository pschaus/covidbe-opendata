import hashlib
import locale

import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
import pandas as pd
import os
import argparse
import netanalysis.traffic.data.fetch_google_traffic

import argparse
import csv
import datetime
import logging
import os
import sys


from netanalysis.traffic.data import model
import netanalysis.traffic.data.api_repository as api

logging.getLogger().setLevel(logging.INFO)


os.system('rm -rf ../../static/csv/traffic')

countries = ['BE','GB','FR','NL','DE','US','SE','ES']
services= "MAPS"

def fetch(args):
    if not args.output_dir:
        logging.error("Need to specify output directory")
        return 1
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    report = api.ApiTrafficRepository()  # type: modelTrafficRepository
    if args.products:
        product_id_list = [model.ProductId[ps.strip().upper()] for ps in args.products.split(",")]
    else:
        product_id_list = [p for p in model.ProductId if p.value != model.ProductId.UNKNOWN]
    region_code_list = countries #report.list_regions()
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=2*365)
    for region_code in region_code_list:
        logging.info("Processing region %s", region_code)
        output_region_directory = os.path.join(args.output_dir, region_code)
        if not os.path.exists(output_region_directory):
            os.makedirs(output_region_directory)

        for product_id in product_id_list:
            logging.info("Fetching traffic data for region %s product %s", region_code, product_id.name)
            csv_filename = os.path.join(output_region_directory, "%s.csv" % product_id.name)
            if os.path.exists(csv_filename):
                logging.info("Traffic data already available for %s in %s. Skipping...",
                    product_id.name, region_code)
                continue
            try:
                traffic_series = report.get_traffic(region_code, product_id, start_time, end_time)
                if traffic_series.empty:
                    logging.info("No traffic for product %s in region %s", product_id.name, region_code)
                    continue
                with open(csv_filename, "w") as csv_file:
                    writer = csv.writer(csv_file)
                    for entry in traffic_series.iteritems():
                        writer.writerow((entry[0].isoformat(), entry[1]))
            except Exception as error:
                logging.warning("Failed to get traffic for %s %s: %s", \
                    region_code, product_id.name, str(error))
    return 0



parser = argparse.ArgumentParser(
        description='Fetches traffic data from the Google Transparency Report as CSV')
parser.add_argument("--output_dir", type=str, required=True, help='The base directory for the output')
parser.add_argument("--products", type=str,
help="Comma-separated list of the products to get traffic for")

fetch(args = parser.parse_args(["--output_dir","../../static/csv/traffic","--products",services]))


def cut(csvpath):
    start = '03-01'
    df = pd.read_csv(csvpath,header=None, names=["date","value"])
    mask = (df['date'] >= f'2020-{start}')
    df = df.loc[mask]
    df.to_csv(csvpath,index=False)

for c in countries:
    cut(f'../../static/csv/traffic/{c}/MAPS.csv')
