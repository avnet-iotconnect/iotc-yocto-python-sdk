SUMMARY = "iotc-demo-service"
DESCRIPTION = "Systemd service for the iotc-demo"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

inherit systemd-user

# SYSTEMD_AUTO_ENABLE_${PN} = "enable"
# SYSTEMD_SERVICE_${PN} = "iotc-demo.service"

# SRC_URI = "file://iotc-demo.service"
# USER_SERVICE_NAME = "evcharger.service"

# FILES:${PN} += "${systemd_system_unitdir}/system/iotc-demo.service"
# REQUIRED_DISTRO_FEATURES= "systemd"

# do_install() {
#     install -d ${D}/${systemd_system_unitdir}/system
#     install -m 0644 ${WORKDIR}/${BP}/iotc-demo.service ${D}/${systemd_system_unitdir}/system/
# }

SRC_URI = "file://iotc-demo.service"

USER_SERVICE_NAME = "iotc-demo.service"

REQUIRED_DISTRO_FEATURES= "systemd"

RDEPENDS:${PN}:append = "iotc-demo"

