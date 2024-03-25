LICENSE = "GPL-3.0-only"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/GPL-3.0-only;md5=c79ff39f19dfec6d293b95dea7b07891"

# DEPENDS = "iotc-demo-service"
RDEPENDS:${PN} = "python3-iotconnect-sdk bash"

SRC_URI = "file://iotc-demo.py \
    file://model \
    file://eg-private-repo-data \
    file://scripts \
    file://iotc-application.sh \
"


APP_INSTALL_DIR = "/app/bin/iotc/"
PRIVATE_DATA_DIR = "/var/iotc/"

# FILES:${PN}-dev = "${PRIVATE_DATA_DIR}/* \
# "

FILES:${PN} += "${APP_INSTALL_DIR}* ${PRIVATE_DATA_DIR}*"

do_install() {
    install -d ${D}${APP_INSTALL_DIR}
    for f in ${WORKDIR}/model/*
    do
        if [ -f $f ]; then
            if [ ! -d ${D}${APP_INSTALL_DIR}/model ]; then
                install -d ${D}${APP_INSTALL_DIR}/model
            fi
            install -m 0755 $f ${D}${APP_INSTALL_DIR}/model/
        fi
    done

    # Add command scripts
    for f in ${WORKDIR}/scripts/*
    do
        if [ -f $f ]; then
            if [ ! -d ${D}${APP_INSTALL_DIR}/scripts ]; then
                install -d ${D}${APP_INSTALL_DIR}/scripts
            fi
            install -m 0755 $f ${D}${APP_INSTALL_DIR}/scripts/
        fi
    done

    # Install main app
    install -m 0755 ${WORKDIR}/iotc-demo.py ${D}${APP_INSTALL_DIR}/

    # install -d ${D}/${ROOT_HOME}/
    install -m 0755 ${WORKDIR}/iotc-application.sh ${D}${APP_INSTALL_DIR}/

    if [ ! -d ${D}${PRIVATE_DATA_DIR} ]; then
        install -d ${D}${PRIVATE_DATA_DIR}
    fi
    cp -R --no-preserve=ownership ${WORKDIR}/eg-private-repo-data/* ${D}${PRIVATE_DATA_DIR}/

        # Add command scripts
    # for f in ${WORKDIR}/eg-private-repo-data/*
    # do
    #     if [ -f $f ]; then
    #         if [ ! -d ${D}${PRIVATE_DATA_DIR} ]; then
    #             install -d ${D}${PRIVATE_DATA_DIR}/
    #         fi
    #         install -m 0755 $f ${D}${PRIVATE_DATA_DIR}/
    #     fi
    # done

    # Add dummy sensor files
    echo 1 > ${D}${APP_INSTALL_DIR}/dummy_sensor_power
    echo 2 > ${D}${APP_INSTALL_DIR}/dummy_sensor_level
}
