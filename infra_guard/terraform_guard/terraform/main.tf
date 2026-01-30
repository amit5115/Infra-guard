variable "vms" {}

module "vm" {
  source = "./modules/compute"
  vms    = var.vms
}
