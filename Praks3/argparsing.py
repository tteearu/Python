import argparser

parser = argparse.ArgumentParser(Description='Apache2 log parser')
parser.add_argument("--path", help="Path to Apache2 log files", default="/var/log/apache2")

parser.add_argument("--top-urls", help="Find top URL-s", default="store_true")

parser.add_argument("--geoip", help="Resolve IP-s to country codes", default="store_true")
parser.add_argument("--verbose", help="Increase verbosity", default="store_true")
args = parser.parse_args()
