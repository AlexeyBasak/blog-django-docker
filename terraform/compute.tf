data "yandex_compute_image" "ubuntu" {
  family = "ubuntu-2204-lts"
}

resource "yandex_compute_instance" "vm" {
  name                      = var.vm_name
  platform_id               = "standard-v3"
  zone                      = var.zone
  allow_stopping_for_update = true

  resources {
    cores         = 2
    memory        = 4
    core_fraction = 50
  }

  scheduling_policy {
    preemptible = var.preemptible
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.ubuntu.id
      size     = 20
      type     = "network-ssd"
    }
  }

  network_interface {
    subnet_id          = yandex_vpc_subnet.main.id
    nat                = true
    security_group_ids = [yandex_vpc_security_group.web.id]
  }

  metadata = {
    ssh-keys = "${var.admin_user}:${trimspace(file(pathexpand(var.ssh_public_key_path)))}"
  }
}