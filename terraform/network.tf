resource "yandex_vpc_network" "main" {
  name = "${var.name_prefix}-network"
}

resource "yandex_vpc_subnet" "main" {
  name           = "${var.name_prefix}-subnet-${var.zone}"
  zone           = var.zone
  network_id     = yandex_vpc_network.main.id
  v4_cidr_blocks = ["10.10.0.0/24"]
}

resource "yandex_vpc_security_group" "web" {
  name        = "${var.name_prefix}-sg"
  description = "SSH only from allowed CIDRs, HTTP/HTTPS from anywhere"
  network_id  = yandex_vpc_network.main.id

  ingress {
    description    = "SSH from allowed addresses"
    protocol       = "TCP"
    port           = 22
    v4_cidr_blocks = var.ssh_allowed_cidrs
  }

  ingress {
    description    = "HTTP"
    protocol       = "TCP"
    port           = 80
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description    = "HTTPS"
    protocol       = "TCP"
    port           = 443
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description    = "All outbound traffic"
    protocol       = "ANY"
    v4_cidr_blocks = ["0.0.0.0/0"]
  }
}