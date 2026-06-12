output "ec2_public_ip" {
  description = "Public IP address of the PE EC2 instance"
  value       = aws_instance.app.public_ip
}

output "app_url" {
  description = "URL to access the Nebula Maintenance App"
  value       = "http://${aws_instance.app.public_ip}:5000"
}
