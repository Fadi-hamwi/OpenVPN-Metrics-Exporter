# OpenVPN Exporter (Official Prometheus Exporter for openVPN can be seen in Official Prometheus page [here](https://prometheus.io/docs/instrumenting/exporters/#miscellaneous))

A Prometheus exporter for OpenVPN, written in Python. It connects to the OpenVPN management interface to collect and expose metrics for monitoring your VPN server's performance and client connections.  
Collects per-client session data from the management interface — including traffic stats, connection times, and IP addresses.

## Features

- Collects standard OpenVPN metrics, including client connections, traffic statistics, and server status
- Exposes metrics in Prometheus format
- Supports graceful shutdown on SIGINT and SIGTERM
- Dockerized for easy deployment

## Exposed Metrics

The exporter collects and exposes the following key metrics:

- **Per-client connection metrics**:
  - `openvpn_client_bytes_received`: Total bytes received by each VPN client connection
  - `openvpn_client_bytes_sent`: Total bytes sent by each VPN client connection
  - `openvpn_client_connected_since`: UNIX timestamp when each VPN client connected
- **Exporter status**:
  - `openvpn_up`: Always 1, indicating the exporter is running
- **Status update timestamp**:
  - `openvpn_status_last_timestamp_seconds`: UNIX timestamp of the last successful OpenVPN status update

Each client connection is uniquely identified by labels such as `real_addr`, `virtual_addr`, and `connection_time`.

### Example Metrics

Below is an example of the metrics exposed by the exporter:

```plaintext
# HELP openvpn_client_bytes_received Total bytes received by each VPN client
# TYPE openvpn_client_bytes_received gauge
openvpn_client_bytes_received{real_addr="172.23.0.1:33492",virtual_addr="10.66.77.5",connection_time="1748023728"} 3285.0
openvpn_client_bytes_received{real_addr="172.23.0.1:33494",virtual_addr="10.66.77.3",connection_time="1748023728"} 3285.0
# HELP openvpn_client_bytes_sent Total bytes sent by each VPN client
# TYPE openvpn_client_bytes_sent gauge
openvpn_client_bytes_sent{real_addr="172.23.0.1:33492",virtual_addr="10.66.77.5",connection_time="1748023728"} 3304.0
openvpn_client_bytes_sent{real_addr="172.23.0.1:33494",virtual_addr="10.66.77.3",connection_time="1748023728"} 3304.0
# HELP openvpn_client_connected_since UNIX timestamp when each VPN client connected
# TYPE openvpn_client_connected_since gauge
openvpn_client_connected_since{real_addr="172.23.0.1:33492",virtual_addr="10.66.77.5",connection_time="1748023728"} 1748023728
openvpn_client_connected_since{real_addr="172.23.0.1:33494",virtual_addr="10.66.77.3",connection_time="1748023728"} 1748023728
# HELP openvpn_up Exporter always returns 1 when running
# TYPE openvpn_up gauge
openvpn_up 1.0
# HELP openvpn_status_last_timestamp_seconds Unix timestamp of the last successful OpenVPN status update
# TYPE openvpn_status_last_timestamp_seconds gauge
openvpn_status_last_timestamp_seconds 1748023751
```

## Installation

### Prerequisites

- Docker
- Docker Compose (for docker-compose deployment)
- Management interface enabled in your OpenVPN server configuration

### Building the Docker Image

To build the Docker image, navigate to the project directory and run:

```bash
docker build -t openvpn_exporter .
```

### Using Docker Compose

Alternatively, you can use the provided `docker-compose.yml` file to run the exporter:

```yaml
docker-compose up -d
```

Make sure to adjust the `-host` and `-p` arguments to match your OpenVPN management interface host and port.

## Usage

To run the exporter manually with Docker, use the following command:

```bash
docker run -p 9176:9176 openvpn_exporter -host <openvpn_host> -p <openvpn_port> -l <listen_port>
```

### Command-Line Arguments

- `-host`: OpenVPN management interface host (default: `localhost`)
- `-p`: OpenVPN management interface port (default: `7505`)
- `-l`: Exporter listen port (default: `9176`)

Once running, the exporter will serve metrics at `http://<host>:<listen_port>/metrics`.

## Integrating with Prometheus

To scrape metrics from the exporter, add the following job to your Prometheus configuration file (e.g., `prometheus.yml`):

```yaml
scrape_configs:
  - job_name: 'openvpn'
    static_configs:
      - targets: ['<exporter_host>:<exporter_port>']
```

Replace `<exporter_host>` and `<exporter_port>` with the host and port where the exporter is running (e.g., `localhost:9176`).

## 📈 Grafana Dashboard

A prebuilt dashboard is available.  
You can import it from [Grafana Dashboards](https://ideone.com/RbfDkO) as a JSON format.

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.
