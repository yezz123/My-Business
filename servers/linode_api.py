from configparser import ConfigParser
from linode_api4 import LinodeClient
from linode_api4.objects.linode import Instance
from django.conf import settings

config = ConfigParser(interpolation=None)
config.read(settings.CONFIG_FILE)

STATUS_COLORS = {
    "running": "success",
    "offline": "danger",
    "booting": "primary",
    "rebooting": "careful",
    "shutting_down": "danger",
    "provisioning": "primary",
    "deleting": "danger",
    "migrating": "warning",
    "rebuilding": "careful",
    "cloning": "warning",
    "restoring": "warning",
    "stopped": "danger",
}

client = LinodeClient(config.get("servers", "LINODE_API_TOKEN"))


def get_linode(id):
    linode = client.linode.instances(Instance.id == id)
    if linode:
        return linode[0]
    return None


def get_linodes():
    return client.linode.instances()


def get_bootstrap_colored_status(status):
    return STATUS_COLORS[status]
