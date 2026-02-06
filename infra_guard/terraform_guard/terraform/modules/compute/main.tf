resource "google_compute_instance" "vm" {
  for_each = var.vms

  name         = each.key
  machine_type = each.value.machine_type
  zone         = each.value.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  dynamic "attached_disk" {
  for_each = each.value.data_disks

  content {
    source      = google_compute_disk.data_disk[each.key].id
    device_name = attached_disk.value.name
  }
}


  network_interface {
    network = "default"
    access_config {}
  }
}

resource "google_compute_disk" "data_disk" {
  for_each = {
    for vm_name, vm in var.vms :
    vm_name => vm
    if length(vm.data_disks) > 0
  }

  name = "${each.key}-data-disk"
  type = "pd-standard"
  zone = each.value.zone
  size = each.value.data_disks[0].size
}
