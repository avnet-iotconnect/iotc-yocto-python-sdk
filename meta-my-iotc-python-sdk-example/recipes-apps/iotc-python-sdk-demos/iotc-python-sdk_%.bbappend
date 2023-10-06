FILESEXTRAPATHS_prepend := "${THISDIR}:"

APP_INSTALL_DIR = "${D}${bindir}/iotc"

SRC_URI += "file://files/json-device-demo/"
FILES_${PN} += "${bindir}/json-device-demo/*"

# Create /usr/bin in rootfs and copy program to it
do_install_append() {
    install -d ${APP_INSTALL_DIR}
    install -d ${APP_INSTALL_DIR}/json-device-demo
    cp -r --no-preserve=ownership ${WORKDIR}/files/json-device-demo/* ${APP_INSTALL_DIR}/json-device-demo/
    install -m 0755 ${WORKDIR}/files/json-device-demo/telemetry_demo.py ${APP_INSTALL_DIR}/json-device-demo/

}