resource "google_service_account" "vm_sa" {
  account_id   = "vm-service-account"
  display_name = "VM Service Account "
}

resource "google_project_iam_member" "sa_logging" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.vm_sa.email}"
}
