import sys
import json
import pymysql
import argparse
import pandas as pd

def ssc_link(appid, instance_id, config):
    link = config['ssc_url']
    link += f"/html/ssc/version/{appid}/audit?q="
    link += f"%5Binstance%20id%5D%3A{instance_id}%20"
    link += f"%5Banalysis%20type%5D%3ASCA&filterset={config['filterset']}&"
    link += f"groupingtype={config['groupingtype']}&"
    link += f"orderby={config['orderby']}&"
    link += f"issue={instance_id}&"
    link += "enginetype=SCA&viewTab=code"
    return link
