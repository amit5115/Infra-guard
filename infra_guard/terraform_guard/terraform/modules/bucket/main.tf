resource "google_storage_bucket" "this" {
  name          = var.name
  location      = var.location
  storage_class = var.storage_class
}
