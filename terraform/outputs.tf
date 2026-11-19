output "vm_public_ip" {
  description = "Публичный IP виртуальной машины"
  value       = yandex_compute_instance.vm.network_interface[0].nat_ip_address
}

output "ssh_command" {
  description = "Команда для подключения по SSH"
  value       = "ssh -i ~/.ssh/blog_ed25519 ${var.admin_user}@${yandex_compute_instance.vm.network_interface[0].nat_ip_address}"
}

output "sslip_domain" {
  description = "Домен на основе IP для Let's Encrypt"
  value       = "${replace(yandex_compute_instance.vm.network_interface[0].nat_ip_address, ".", "-")}.sslip.io"
}