variable "buckets" {
  type = map(object({
    location       = string
    storage_class  = string
  }))
}
