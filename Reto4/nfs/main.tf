# NFS server VM to be used by apps such as magento
module "nfs" {
    source = "."

    name_prefix = "${var.project_name}-nfs-${var.environment}"
    labels      = local.common_labels
    subnetwork  = module.vpc.public_subnetwork
    project     = var.project_id
    network     = local.vpc_name
    export_paths = [
    "/share/media",
    "/share/static",
    ]
    capacity_gb = "100"
}