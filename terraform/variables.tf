variable "aws_region" {
  description = "AWS region for PE deployment"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name prefix for resources"
  type        = string
  default     = "nebula-maint-app-pe"
}

variable "docker_image" {
  description = "Docker Hub image to deploy"
  type        = string
  default     = "taig2k/nebula_maint_app:v0.1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}
