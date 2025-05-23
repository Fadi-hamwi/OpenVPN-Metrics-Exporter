# Copyright 2025 Fadi Hamwi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import signal
import sys
import time
import threading
from prometheus_client import start_http_server, CollectorRegistry
from openvpn_api import VPN
from openvpn_collector import OpenVPNCollector, bcolors


def handle_exit(signum, frame):
    print(f"{bcolors.WARNING}\nShutting down exporter…{bcolors.ENDC}")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)


def main():
    parser = argparse.ArgumentParser(
        description='OpenVPN exporter for Prometheus')
    parser.add_argument('-host', default='localhost',
                        help='OpenVPN management host')
    parser.add_argument('-p', default=7505, type=int,
                        help='OpenVPN management port')
    parser.add_argument('-l', default=9176, type=int,
                        help='Exporter listen port')
    args = parser.parse_args()

    registry = CollectorRegistry()
    vpn = VPN(args.host, args.p)
    while True:
        try:
            with vpn.connection():
                print(
                    f"{bcolors.OKGREEN}Connected to OpenVPN management interface.{bcolors.ENDC}")
                collector = OpenVPNCollector(vpn)
                registry.register(collector)
                start_http_server(port=args.l, registry=registry)
                print(
                    f"{bcolors.OKGREEN}Serving metrics on http://{args.host}:{args.l}/metrics{bcolors.ENDC}")
                threading.Event().wait()  # Block main thread
        except Exception as e:
            print(
                f"{bcolors.WARNING}Connection to OpenVPN failed: {e}. Retrying in 10 seconds...{bcolors.ENDC}")
            time.sleep(10)


if __name__ == '__main__':
    main()
