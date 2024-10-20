from netbox.plugins import PluginMenuButton, PluginMenuItem, PluginMenu

items = (
    PluginMenuItem(
        link="plugins:netbox_certificate_plugin:certificate_list",
        link_text="Certificates",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_certificate_plugin:certificate_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_certificate_plugin:certificate_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    PluginMenuItem(
        link="plugins:netbox_certificate_plugin:certificateauthority_list",
        link_text="Certificate Authorities",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_certificate_plugin:certificateauthority_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_certificate_plugin:certificateauthority_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
    PluginMenuItem(
        link="plugins:netbox_certificate_plugin:hostname_list",
        link_text="Hostnames",
        buttons=[
            PluginMenuButton(
                link="plugins:netbox_certificate_plugin:hostname_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
            PluginMenuButton(
                link="plugins:netbox_certificate_plugin:hostname_import",
                title="Import",
                icon_class="mdi mdi-upload",
            ),
        ]
    ),
)

menu = PluginMenu(
    label="Certificate Management",
    groups=(("CERTIFICATE MANAGEMENT", items),),
    icon_class="mdi mdi-domain",
)
