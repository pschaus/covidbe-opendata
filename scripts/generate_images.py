import gzip
import os
import sys
from datetime import date

import boto3
import botocore
import boto3.session
import pandas as pd
from multiprocessing import Pool

os.chdir(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append('./')
import graphs
import graphs.cases_age_groups
import graphs.cases_per_million
import graphs.cases_per_municipality
import graphs.cases_per_province
import graphs.deaths_age_groups
import graphs.deaths_per_million
import graphs.hopitals
import graphs.obituary
import graphs.overmortality
import graphs.testing


def s3_get_link_and_create_if_needed(filename, content_gen, content_type):
    sess = boto3.session.Session()
    s3_client = sess.resource('s3')
    obj = s3_client.Object("covidatabe", filename)

    try:
        # Check if file exists
        obj.load()
        print(f"Object {filename} already exists on s3")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"Uploading {filename} to s3")
            content = gzip.compress(content_gen())
            print(f"Content generated for {filename}")
            obj.put(Body=content, ContentType=content_type, ContentEncoding="gzip")
            print(f"Done uploading {filename}")
        else:
            raise

    return f"https://covidatabe.s3.eu-central-1.amazonaws.com/{filename}"


def update(name, f):
    def htmlgen():
        plot = f()
        plot.layout.height = None
        plot.layout.autosize = True
        return plot.to_html().encode()

    link_image = s3_get_link_and_create_if_needed(f"{date.today()}/{name}-800-500.png", lambda: f().to_image(format="png", width=800, height=500), "image/png")
    link_html = s3_get_link_and_create_if_needed(f"{date.today()}/{name}.html", htmlgen, "text/html")
    return name, link_image, link_html


pool = Pool(20)
out = list(pool.starmap(update, graphs.registered_plots.items()))

print(out)
pd.DataFrame(out, columns=['name', 'link_image', 'link_html']).to_csv("static/csv/last_plots.csv")
