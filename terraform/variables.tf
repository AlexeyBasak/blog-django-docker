variable "cloud_id" {
  description = "ID облака Yandex Cloud"
  type        = string
}

variable "folder_id" {
  description = "ID каталога Yandex Cloud"
  type        = string
}

variable "zone" {
  description = "Зона доступности"
  type        = string
  default     = "ru-central1-a"
}

variable "name_prefix" {
  description = "Префикс имён ресурсов"
  type        = string
  default     = "blog"
}

variable "vm_name" {
  description = "Имя виртуальной машины"
  type        = string
  default     = "blog-vm"
}

variable "admin_user" {
  description = "Имя администратора на ВМ"
  type        = string
  default     = "deploy"
}

variable "ssh_public_key_path" {
  description = "Путь к публичному SSH-ключу"
  type        = string
  default     = "~/.ssh/blog_ed25519.pub"
}

variable "ssh_allowed_cidrs" {
  description = "С каких адресов разрешён SSH, например [\"203.0.113.10/32\"]"
  type        = list(string)

  validation {
    condition     = length(var.ssh_allowed_cidrs) > 0 && !contains(var.ssh_allowed_cidrs, "0.0.0.0/0")
    error_message = "ssh_allowed_cidrs не должен быть пустым и не должен содержать 0.0.0.0/0."
  }
}

variable "preemptible" {
  description = "Прерываемая ВМ (дешевле, облако может её остановить)"
  type        = bool
  default     = true
}