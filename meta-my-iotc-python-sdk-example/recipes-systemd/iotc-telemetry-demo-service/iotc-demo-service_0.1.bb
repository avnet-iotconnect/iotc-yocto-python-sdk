SUMMARY = "iotc-demo-service"
DESCRIPTION = "Systemd service for the iotc-demo"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

inherit systemd

SYSTEMD_AUTO_ENABLE_${PN} = "enable"
SYSTEMD_SERVICE_${PN} = "iotc-demo.service"

SRC_URI = "file://iotc-demo.service;subdir=${BP};\
"

FILES:${PN} += "${systemd_unitdir}/system/iotc-demo.service"

do_install() {
    install -d ${D}/${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/${BP}/iotc-demo.service ${D}/${systemd_unitdir}/system/
}
