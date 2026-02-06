variable "vms" {}

module "vm" {
  source = "./modules/compute"
  vms    = var.vms
}

# variable "buckets" {}

# module "bucket" {
#   source  = "./modules/bucket"
#   buckets = var.buckets
# }
