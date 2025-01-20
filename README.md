# IP Info Discord Webhook

A simple service that collects network interface information from a host and sends it to Discord via webhooks. This is useful for monitoring network changes and keeping track of IP addresses across multiple systems.

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for Python package management and Docker for containerization.

### Prerequisites

- Python 3.x
- Docker
- uv (`pip install uv`)

### Environment Variables

The following environment variables are required:

| Variable | Description | Example |
|----------|-------------|---------|
| DISCORD_WEBHOOK_URL | Discord webhook URL for sending notifications | https://discord.com/api/webhooks/... |
| CHECK_INTERVAL | Time in seconds between IP checks (optional) | 300 |

You can set these using a `.env` file for local development:
```bash
DISCORD_WEBHOOK_URL=your_webhook_url_here
CHECK_INTERVAL=300
```

For Docker, pass them using the `-e` flag:
```bash
docker run -e DISCORD_WEBHOOK_URL=your_webhook_url_here -e CHECK_INTERVAL=300 ipinfo
```

### Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

### Docker Build

Build the Docker image:
```bash
docker build -t ipinfo .
```

Run the container:
```bash
docker run ipinfo
```

## CI/CD

This project uses GitHub Actions for continuous integration. The workflow:
- Builds the Docker image on every push to main and pull requests
- Uses Docker Buildx for efficient caching
- Validates the build process

The workflow configuration can be found in `.github/workflows/docker-build.yml`.
