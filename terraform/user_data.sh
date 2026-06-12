#!/bin/bash
set -euo pipefail

dnf update -y
dnf install -y docker
systemctl enable docker
systemctl start docker

docker pull ${docker_image}
docker run -d --name nebula_maint_app -p 5000:5000 --restart unless-stopped ${docker_image}
