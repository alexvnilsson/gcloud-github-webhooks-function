#!/usr/bin/env python3

import argparse
from sys import exit
import os
import os.path
import configparser

def str_to_bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description='Deploy Cloud Function.')
parser.add_argument("--dry-run", type=str_to_bool, nargs='?', const=True, default=False, help="print command to run")
args = parser.parse_args()

config = configparser.ConfigParser()

CWD=os.getcwd()
DEPLOYRC_PATH=os.path.join(CWD, ".deployrc")

def get_deployrc():
  _deployrc: dict = {
    'GCloudFunction': {}
  }

  config.read(DEPLOYRC_PATH)

  for s in config.sections():
    for k,v in config.items(s):
      _deployrc[s][k] = v

  return _deployrc

deployrc = get_deployrc()

gcloudfunction = deployrc["GCloudFunction"]

GCLOUD_FUNC_NAME=gcloudfunction["name"]
GCLOUD_FUNC_PROJECT=gcloudfunction["project"]
GCLOUD_FUNC_REGION=gcloudfunction["region"]
GCLOUD_FUNC_RUNTIME=gcloudfunction["runtime"]
GCLOUD_FUNC_SOURCE_URL=gcloudfunction["sourceurl"]
GCLOUD_FUNC_ARGS=gcloudfunction["args"]

CMD=f"gcloud functions deploy {GCLOUD_FUNC_NAME} "

CMD_OPTS = [
  f"--source {GCLOUD_FUNC_SOURCE_URL}",
  f"--runtime {GCLOUD_FUNC_RUNTIME}",
  f"--region={GCLOUD_FUNC_REGION}"
]

if len(GCLOUD_FUNC_ARGS) > 0:
  FUNC_ARGS = GCLOUD_FUNC_ARGS.split(",")
  for _arg in FUNC_ARGS:
    ARG = _arg.strip()
    CMD_OPTS.append(ARG)

CMD_OPTS_RAW = " ".join(CMD_OPTS)

CMD_RAW = f"{CMD} {CMD_OPTS_RAW}"

if args.dry_run == True:
    print(f"Will run: {CMD_RAW}")
    exit(0)

os.system(CMD_RAW)