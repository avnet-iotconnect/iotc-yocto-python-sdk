FILESEXTRAPATHS_prepend := "${THISDIR}:"

APP_INSTALL_DIR = "${D}${bindir}/iotc"

SRC_URI += "file://files/iotconnect-sdk-1.0-firmware-python_msg-2_1.py"

FILES_${PN} += "${bindir}/iotconnect-sdk-1.0-firmware-python_msg-2_1.py"

SRC_URI += "file://files/test.py"
SRC_URI += "file://files/models/device_model.py"

# Create /usr/bin in rootfs and copy program to it
do_install_append() {
    install -d ${APP_INSTALL_DIR}
    install -m 0755 ${WORKDIR}/files/iotconnect-sdk-1.0-firmware-python_msg-2_1.py ${APP_INSTALL_DIR}/
    install -d ${APP_INSTALL_DIR}/models
    install -m 0755 ${WORKDIR}/files/models/device_model.py ${APP_INSTALL_DIR}/models/
    install -m 0755 ${WORKDIR}/files/test.py ${APP_INSTALL_DIR}/
}