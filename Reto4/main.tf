provider "google" {
credentials = file("kauth/reto4-moodle-bb7d3ecc0972.json")
project = "reto4-moodle"
region = "us-central1"
zone = "us-central1-c"
}

resource "google_compute_network" "reto4_network" {
name = "reto4-network"
}

resource "google_compute_autoscaler" "reto4_autoscaler" {
    name = "reto4-autoscaler"
    project = "reto4-moodle"
    zone = "us-central1-c"
    target = google_compute_instance_group_manager.reto_4_group_manager.self_link

    autoscaling_policy {
    max_replicas = 5
    min_replicas = 1
    cooldown_period = 60

        cpu_utilization {
        target = 0.5    
        }
    }
}

resource "google_compute_instance_template" "reto4_moodle_template" {
name = "reto4-instance-template"
machine_type = "e2-micro"
can_ip_forward = false
project = "reto4-moodle"
tags = ["allow-lb-service"]

    disk {
        source_image = data.google_compute_image.reto4_moodle_image.self_link
    }

    network_interface {
        network = google_compute_network.reto4_network.name
    }

    service_account {
        scopes = ["userinfo-email", "compute-ro", "storage-ro"]
    }
}

resource "google_compute_target_pool" "reto4_target_pool" {
    name = "reto4-target-pool"
    project = "reto4-moodle"
    region = "us-central1"
}

resource "google_compute_instance_group_manager" "reto_4_group_manager" {
    name = "reto4-igm"
    zone = "us-central1-c"
    project = "reto4-moodle"
    version {
        instance_template = google_compute_instance_template.reto4_moodle_template.self_link
        name = "primary"
    }

    target_pools = [google_compute_target_pool.reto4_target_pool.self_link]
    base_instance_name = "terraform"
}

data "google_compute_image" "reto4_moodle_image" {
    name = "reto4-moodle"
    project = "reto4-moodle"
}

module "lb" {
    source = "GoogleCloudPlatform/lb/google"
    version = "2.2.0"
    region = "us-central1"
    name = "load-balancer"
    service_port = 80
    target_tags = ["reto4-target-pool"]
    network = google_compute_network.reto4_network.name
}

resource "google_sql_database_instance" "moodle_db_primary" {
    name             = "moodle-db-primary"
    database_version = "POSTGRES_14"
    region           = "us-central1"

    settings {
        # Second-generation instance tiers are based on the machine
        # type. See argument reference below.
        tier = "db-f1-micro"
    }
}

resource "google_sql_database" "moodle_db" {
  name     = "bitnami_moodle"
  instance = google_sql_database_instance.moodle_db_primary.name
}

resource "google_sql_user" "users" {
  name     = "bn_moodle"
  instance = google_sql_database_instance.moodle_db_primary.name
  password = "password"
}

module "nfs" {
    source      = "DeimosCloud/nfs/google"
    name_prefix = "moodle-nfs"
    labels      = {}
    project     = "reto4-moodle"
    network     = google_compute_network.reto4_network.name
    export_paths = [
        "/mnt/moodle",
        "/mnt/moodledata"
    ]
    capacity_gb = "10"
}