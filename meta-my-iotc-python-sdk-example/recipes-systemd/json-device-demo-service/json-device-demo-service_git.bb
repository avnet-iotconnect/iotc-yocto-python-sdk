LICENSE = "CLOSED"
inherit systemd


SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE_${PN} = "json-device-demo.service"

SRC_URI_append = " file://json-device-demo.service "
FILES_${PN} += "${systemd_unitdir}/system/json-device-demo.service"

do_install_append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/json-device-demo.service ${D}/${systemd_unitdir}/system
}
