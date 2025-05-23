# OpenVPN Exporter

A Prometheus exporter for OpenVPN, written in Python. It connects to the OpenVPN management interface to collect and expose metrics for monitoring your VPN server's performance and client connections.
 Collects per-client session data from the management interface — including traffic stats, connection times, and IP addresses.

## Features

- Collects standard OpenVPN metrics, including client connections, traffic statistics, and server status
- Exposes metrics in Prometheus format
- Supports graceful shutdown on SIGINT and SIGTERM
- Dockerized for easy deployment

## Installation

### Prerequisites

- Docker
- Docker Compose (for docker-compose deployment)
- Management interface enabled in your openVPN server configuration

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

You can import it from [Grafana Dashboards](https://ideone.com/RbfDkO) as a json format.


## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.
