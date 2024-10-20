"""Top-level package for NetBox certificate Plugin."""

__author__ = """Eric Hester"""
__email__ = "hester1@clemson.edu"
__version__ = "0.1.0"


from netbox.plugins import PluginConfig


class certificateConfig(PluginConfig):
    name = "netbox_certificate_plugin"
    verbose_name = "NetBox Certificate Plugin"
    description = "NetBox plugin for certificate management."
    version = "0.1.0"
    base_url = "netbox_certificate_plugin"


config = certificateConfig
