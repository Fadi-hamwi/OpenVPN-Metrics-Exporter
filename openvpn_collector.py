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

import time
from prometheus_client.core import GaugeMetricFamily

# ANSI color helper


class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'


class OpenVPNCollector:
    def __init__(self, vpn):
        self.vpn = vpn

    def collect(self):
        try:
            status = self.vpn.get_status()
            clients = list(status.client_list.values())
            real_to_virtual = {
                str(r.real_address): route
                for route, r in status.routing_table.items()
            }

            # Create metric families for client metrics
            bytes_received = GaugeMetricFamily(
                'openvpn_client_bytes_received_total',
                'Total bytes received by each VPN client',
                labels=['common_name', 'real_addr',
                        'virtual_addr']
            )
            bytes_sent = GaugeMetricFamily(
                'openvpn_client_bytes_sent_total',
                'Total bytes sent by each VPN client',
                labels=['common_name', 'real_addr',
                        'virtual_addr']
            )
            connected_since = GaugeMetricFamily(
                'openvpn_client_connected_since_seconds',
                'UNIX timestamp when each VPN client connected',
                labels=['common_name', 'real_addr',
                        'virtual_addr']
            )

            # Process each client
            for client in clients:
                cn = client.common_name
                real = str(client.real_address)
                virt = real_to_virtual.get(real, "unknown")
                ts = int(client.connected_since.timestamp())
                labels = [cn, real, virt]

                bytes_received.add_metric(labels, client.bytes_received)
                bytes_sent.add_metric(labels, client.bytes_sent)
                connected_since.add_metric(labels, ts)

            # Yield client metrics
            yield bytes_received
            yield bytes_sent
            yield connected_since
            # Yield exporter status metrics
            yield GaugeMetricFamily('openvpn_up', 'Exporter always returns 1 when running', value=1)
            yield GaugeMetricFamily('openvpn_status_last_timestamp_seconds', 'Unix timestamp of the last successful OpenVPN status update', value=int(time.time()))

        except Exception as e:
            print(f"{bcolors.WARNING}Error fetching metrics: {e}{bcolors.ENDC}")
            yield GaugeMetricFamily('openvpn_up', 'Exporter always returns 1 when running', value=0)
