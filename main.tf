terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

variable "project_id" {
  type        = string
  description = "GCP Project ID"
  default     = "fde-agent-sandbox"
}

variable "region" {
  type        = string
  description = "Deployment region"
  default     = "us-central1"
}

resource "google_secret_manager_secret" "gemini_api_key" {
  project   = var.project_id
  secret_id = "gemini-api-key"
  replication {
    auto {}
  }
}

resource "google_cloud_run_v2_service" "fde_pulse_agent_service" {
  name     = "fde-chat-pulse-agent"
  location = var.region
  project  = var.project_id

  template {
    containers {
      image = "gcr.io/${var.project_id}/fde-pulse-agent:latest"
      env {
        name  = "CHAT_SPACE_ID"
        value = "spaces/AAQAlvoeMDA"
      }
    }
  }
}
