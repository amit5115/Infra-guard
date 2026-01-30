variable "vms" {
  type = map(object({
    machine_type = string
    zone         = string
  }))
}
