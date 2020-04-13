import logging
import boto3
from datetime import date

import botocore
from botocore.exceptions import ClientError

from utils import ThreadSafeCache

registered_plots = {}
__html_cache = ThreadSafeCache()
__image_cache = ThreadSafeCache()

def register_plot_for_embedding(name):
    def inside(f):
        f.name = name
        f.get_html_link = lambda: __html_cache.get(name, lambda: __gen_html(name, f))
        f.get_image_link = lambda: __image_cache.get(name, lambda: __gen_image(name, f))
        registered_plots[name] = f
        return f
    return inside


def s3_get_link_and_create_if_needed(filename, content_gen, content_type):
    s3_client = boto3.resource('s3')
    obj = s3_client.Object("covidatabe", filename)

    try:
        # Check if file exists
        obj.load()
        print(f"Object {filename} already exists on s3")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"Uploading {filename} to s3")
            obj.put(Body=content_gen(), Metadata={"Content-Type": content_type})
        else:
            raise

    return f"http://covidatabe.s3-website.eu-central-1.amazonaws.com/{filename}"


def __gen_html(name, f):
    d = date.today()
    key = f"{d}/{name}.html"
    return s3_get_link_and_create_if_needed(key, lambda: f().to_html().encode(), "text/html")


def __gen_image(name, f):
    d = date.today()
    key = f"{d}/{name}.png"
    return s3_get_link_and_create_if_needed(key, lambda: f().to_image(format="png", width=600, height=350), "image/png")
