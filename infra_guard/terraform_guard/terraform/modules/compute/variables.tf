variable "vms" {
  type = map(object({
    machine_type = string
    zone         = string

    data_disks = optional(list(object({
      name = string
      size = number
      type = string
    })), [])
  }))
}
