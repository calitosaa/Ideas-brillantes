# Skill: DevOps and Linux System Administration

## Description and Purpose

This skill describes the native DevOps and Linux system administration capability of Ideas-brillantes. The model has been fine-tuned with operational knowledge spanning service management, containerization, CI/CD pipelines, package management, log analysis, backup strategies, and monitoring. This knowledge activates whenever the user needs to deploy, maintain, troubleshoot, or automate infrastructure.

---

## When This Skill Applies

- User needs to deploy an application or service
- User asks to configure or manage a Linux server
- User asks about Docker, containers, or Docker Compose
- User asks to set up CI/CD pipelines
- User needs to troubleshoot a service, process, or system issue
- User asks about backups, monitoring, or log management
- User asks to install or manage packages
- User asks to set up scheduled jobs or system tasks

---

## 1. systemd Service Management

### Common commands
```bash
# Status and logs
systemctl status nginx
systemctl status --no-pager nginx           # no pager, full output
journalctl -u nginx                         # all logs for service
journalctl -u nginx -n 100                  # last 100 lines
journalctl -u nginx --since "1 hour ago"    # recent logs
journalctl -u nginx -f                      # follow (live tail)
journalctl -u nginx --since today           # today's logs

# Control
systemctl start nginx
systemctl stop nginx
systemctl restart nginx
systemctl reload nginx                       # reload config without restart
systemctl enable nginx                       # start on boot
systemctl disable nginx                      # remove from boot
systemctl mask nginx                         # prevent any starting

# Listing
systemctl list-units --type=service
systemctl list-units --type=service --state=running
systemctl list-units --type=service --state=failed
systemctl list-timers                        # scheduled tasks
```

### Creating a systemd service
```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=myappuser
Group=myappuser
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/venv/bin/python /opt/myapp/main.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

# Environment
EnvironmentFile=/opt/myapp/.env
Environment=PYTHONUNBUFFERED=1

# Security hardening
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/opt/myapp/data

[Install]
WantedBy=multi-user.target
```

```bash
# After creating service file:
systemctl daemon-reload
systemctl enable --now myapp
systemctl status myapp
```

### Creating a systemd timer (cron replacement)
```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Daily backup timer
Requires=backup.service

[Timer]
OnCalendar=*-*-* 02:00:00    # every day at 2am
Persistent=true               # run if missed

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Daily backup

[Service]
Type=oneshot
ExecStart=/opt/scripts/backup.sh
User=backup
```

---

## 2. Docker and Docker Compose

### Docker fundamentals
```bash
# Images
docker pull nginx:alpine
docker images
docker image rm nginx:alpine
docker build -t myapp:latest .
docker build -t myapp:1.0.0 -f Dockerfile.prod .

# Containers
docker run -d --name myapp -p 8080:80 nginx:alpine
docker run -it --rm ubuntu:22.04 bash            # interactive, remove on exit
docker ps                                         # running containers
docker ps -a                                      # all containers
docker stop myapp
docker rm myapp
docker logs myapp
docker logs myapp -f --tail=100
docker exec -it myapp bash                        # shell into running container

# Cleanup
docker system prune                               # remove unused resources
docker system prune -a --volumes                  # aggressive cleanup
docker volume prune
```

### Dockerfile best practices
```dockerfile
# Multi-stage build — keeps final image small
FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

# Security: run as non-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy only built dependencies
COPY --from=builder /install /usr/local

# Copy application code
COPY --chown=appuser:appuser . .

USER appuser

# Document the port
EXPOSE 8000

# Use exec form (not shell form) — proper signal handling
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose patterns
```yaml
# docker-compose.yml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped
    volumes:
      - ./data:/app/data
    networks:
      - app-network

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    restart: unless-stopped
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - app
    restart: unless-stopped
    networks:
      - app-network

volumes:
  postgres-data:
  redis-data:

networks:
  app-network:
    driver: bridge
```

```bash
# Docker Compose commands
docker compose up -d                    # start all services
docker compose up -d --build           # rebuild images first
docker compose down                    # stop and remove containers
docker compose down -v                 # also remove volumes
docker compose logs -f app             # follow specific service logs
docker compose exec app bash           # shell into service
docker compose ps                      # service status
docker compose restart app             # restart one service
docker compose pull                    # pull latest images
```

---

## 3. CI/CD Pipeline Patterns

### GitHub Actions
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: pip install -r requirements.txt -r requirements-dev.txt

      - name: Run linter
        run: ruff check src/

      - name: Run type checker
        run: mypy src/

      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/testdb
        run: pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: myorg/myapp:latest,myorg/myapp:${{ github.sha }}
```

### GitLab CI
```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

test:
  stage: test
  image: python:3.11-slim
  services:
    - postgres:15-alpine
  variables:
    POSTGRES_DB: testdb
    POSTGRES_PASSWORD: testpass
    DATABASE_URL: postgresql://postgres:testpass@postgres:5432/testdb
  before_script:
    - pip install -r requirements.txt -r requirements-dev.txt
  script:
    - ruff check src/
    - pytest --cov=src --cov-report=term-missing
  coverage: '/TOTAL.*\s+(\d+%)$/'

build:
  stage: build
  image: docker:24
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  only:
    - main

deploy:
  stage: deploy
  script:
    - ssh user@server "docker pull $DOCKER_IMAGE && docker compose up -d"
  environment:
    name: production
  only:
    - main
```

---

## 4. Package Management

### apt (Debian/Ubuntu)
```bash
apt update                                      # update package index
apt upgrade -y                                  # upgrade all packages
apt install -y nginx python3-pip git            # install packages
apt remove nginx                                # remove (keep config)
apt purge nginx                                 # remove + config
apt autoremove                                  # remove unused deps
apt search nginx                                # search packages
apt show nginx                                  # package details
dpkg -l | grep nginx                            # check if installed
```

### pip (Python)
```bash
pip install package==1.2.3                      # specific version
pip install -r requirements.txt                 # from file
pip install -e .                                # install in editable mode
pip list --outdated                             # check for updates
pip freeze > requirements.txt                   # export installed
pip uninstall package

# Best practice: always use virtual environments
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### npm (Node.js)
```bash
npm install                                     # install from package.json
npm install express                             # add dependency
npm install --save-dev jest                     # dev dependency
npm update                                      # update all
npm audit                                       # check vulnerabilities
npm audit fix                                   # auto-fix vulnerabilities
npm run [script]                                # run package.json script
npx [package] [args]                            # run without installing
```

### cargo (Rust)
```bash
cargo build                                     # build
cargo build --release                           # optimized build
cargo run                                       # build and run
cargo test                                      # run tests
cargo add serde --features derive               # add dependency
cargo update                                    # update Cargo.lock
cargo audit                                     # security audit (cargo-audit)
```

---

## 5. Log Management

### journalctl (systemd logs)
```bash
journalctl                                      # all logs
journalctl -u nginx                             # service logs
journalctl -u nginx -f                          # follow live
journalctl -u nginx --since "2025-01-15 10:00" --until "2025-01-15 11:00"
journalctl -p err                               # errors only
journalctl -p err..warning                      # warning and error
journalctl --disk-usage                         # log disk usage
journalctl --vacuum-size=500M                   # trim to 500MB
journalctl --vacuum-time=30d                    # remove logs > 30 days
```

### logrotate
```
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    daily                   # rotate daily
    rotate 30               # keep 30 rotated files
    compress                # gzip rotated files
    delaycompress           # compress on next rotation (not current)
    missingok               # don't error if log is missing
    notifempty              # don't rotate if empty
    create 0640 myapp myapp # create new log with permissions
    postrotate
        systemctl reload myapp
    endscript
}
```

### Common log analysis patterns
```bash
# Count errors in log file
grep -c "ERROR" /var/log/myapp/app.log

# Find most recent errors
grep "ERROR" /var/log/myapp/app.log | tail -20

# Count by error type
grep "ERROR" /var/log/myapp/app.log | awk '{print $5}' | sort | uniq -c | sort -rn

# Show lines around an error
grep -n -A 3 -B 1 "Exception" /var/log/myapp/app.log

# Watch log file live
tail -f /var/log/myapp/app.log

# Search across all logs
journalctl --grep "connection refused"
```

---

## 6. Backup Strategies

### File backup with rsync
```bash
# Local backup
rsync -avz --delete /source/dir/ /backup/dir/

# Remote backup
rsync -avz -e "ssh -i ~/.ssh/backup_key" /source/ user@backup-server:/backup/

# Exclude patterns
rsync -avz --exclude=".git" --exclude="*.pyc" --exclude="node_modules/" \
    /project/ /backup/project/

# Dry run (preview without executing)
rsync -avzn /source/ /backup/
```

### Automated backup script
```bash
#!/bin/bash
# /opt/scripts/backup.sh

set -euo pipefail

BACKUP_DIR="/backup"
SOURCE_DIR="/opt/myapp/data"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/myapp_$DATE.tar.gz"
RETENTION_DAYS=30

# Create backup
tar -czf "$BACKUP_FILE" -C "$SOURCE_DIR" .

# Verify backup created
if [ ! -f "$BACKUP_FILE" ]; then
    echo "ERROR: Backup file not created" >&2
    exit 1
fi

echo "Backup created: $BACKUP_FILE ($(du -sh "$BACKUP_FILE" | cut -f1))"

# Remove old backups
find "$BACKUP_DIR" -name "myapp_*.tar.gz" -mtime +"$RETENTION_DAYS" -delete
echo "Cleaned up backups older than $RETENTION_DAYS days"
```

### PostgreSQL backup
```bash
# Dump single database
pg_dump -U postgres -d mydb > /backup/mydb_$(date +%Y%m%d).sql

# Dump with compression
pg_dump -U postgres -d mydb | gzip > /backup/mydb_$(date +%Y%m%d).sql.gz

# Dump all databases
pg_dumpall -U postgres > /backup/all_databases_$(date +%Y%m%d).sql

# Restore
psql -U postgres -d mydb < /backup/mydb_20250115.sql

# Docker-based backup
docker exec postgres-container pg_dump -U user mydb | gzip > /backup/mydb.sql.gz
```

---

## 7. Monitoring Setup

### Prometheus + Grafana basics
```yaml
# docker-compose monitoring stack
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
    depends_on:
      - prometheus

  node-exporter:
    image: prom/node-exporter:latest
    network_mode: host
    pid: host
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
```

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']

  - job_name: 'myapp'
    static_configs:
      - targets: ['myapp:8000']
    metrics_path: '/metrics'
```

### Key metrics to monitor:
| Metric | Tool | Alert threshold |
|---|---|---|
| CPU usage | node-exporter | > 90% for 5 min |
| Memory usage | node-exporter | > 85% |
| Disk usage | node-exporter | > 80% |
| Service health | blackbox-exporter | any DOWN |
| HTTP error rate | app metrics | > 1% 5xx |
| HTTP p99 latency | app metrics | > 2s |
| DB connections | postgres-exporter | > 80% of max |

---

## 8. Common Linux Troubleshooting Patterns

### Service won't start
```bash
systemctl status myapp           # check status and recent logs
journalctl -u myapp -n 50        # more log context
journalctl -u myapp -p err       # errors only
# Look for: permission denied, port already in use, missing file
```

### Port already in use
```bash
ss -tulpn | grep :8080
# OR
lsof -i :8080
# → Shows PID using the port
kill -15 <PID>
# OR to find what process: ps -p <PID> -o pid,cmd
```

### Disk full
```bash
df -h                            # which partition is full
du -sh /var/log/*                # largest directories
du -sh /home/*
ncdu /                           # interactive disk usage explorer
journalctl --vacuum-size=200M    # trim systemd logs
docker system prune              # remove unused Docker data
find /var/log -name "*.log" -size +100M   # find large log files
```

### High CPU
```bash
top                              # live process view
htop                             # better top
ps aux --sort=-%cpu | head -10   # top CPU processes
# Find the PID → check with: cat /proc/<PID>/cmdline
```

### Memory leak investigation
```bash
free -h                          # overall memory
ps aux --sort=-%mem | head -10   # top memory processes
cat /proc/<PID>/status | grep VmRSS   # memory for specific process
# If OOM: journalctl -k | grep -i "out of memory"
```

### SSH connection issues
```bash
ssh -v user@host                 # verbose connection debug
# Check on server:
systemctl status sshd
journalctl -u sshd -n 50
# Firewall check:
ufw status
iptables -L INPUT -n | grep 22
```

### Network troubleshooting
```bash
ping -c 4 8.8.8.8                # basic connectivity
traceroute 8.8.8.8               # route tracing
dig example.com                  # DNS lookup
nslookup example.com             # DNS (legacy)
curl -v https://example.com      # HTTP verbose
ss -tulpn                        # open sockets
ip route show                    # routing table
ip addr show                     # interface addresses
```
