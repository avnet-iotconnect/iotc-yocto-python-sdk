LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE_${PN} = "ota-demo.service"

SRC_URI_append = " file://ota-demo.service "
FILES_${PN} += "${systemd_unitdir}/system/ota-demo.service"

do_install_append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/ota-demo.service ${D}/${systemd_unitdir}/system
}
