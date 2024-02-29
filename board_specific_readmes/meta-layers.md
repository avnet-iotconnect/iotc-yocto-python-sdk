## Build Instructions

These instructions are designed to get a Yocto image up and running for a specific board, First of all you will have to follow the instructions for each specific board you are using and then continue on from this guide.

1. Adding Yocto Python SDK layers

    ```bash
    # You will need to clone the repository to a directory where all the other meta-layers exist, this different for each board
    
    git clone https://github.com/avnet-iotconnect/iotc-yocto-python-sdk.git -b dunfell ./meta-iotconnect

    make env

    echo -e '\n' >> conf/bblayers.conf
    
    # the path is relative from the yocto build folder, this may be different from board to board

    bitbake-layers add-layer ../../meta-iotconnect/meta-iotc-python-sdk/
    
    bitbake-layers add-layer ../../meta-iotconnect/meta-my-iotc-python-sdk-example/
    
    echo -e '\nCORE_IMAGE_EXTRA_INSTALL += " iotc-demo-dev iotc-demo-service"' >> ./conf/local.conf
    
    echo -e '\nDISTRO_FEATURES:append = " systemd"\nDISTRO_FEATURES_BACKFILL_CONSIDERED += " sysvinit"\nVIRTUAL-RUNTIME_init_manager = " systemd"\nVIRTUAL-RUNTIME_initscripts = " systemd-compat-units"\n' >> ./conf/local.conf
    
    echo -e '\n\nEXTRA_IMAGE_FEATURES=""\nINHERIT += "extrausers"\nEXTRA_USER_PARAMS = "usermod -P avnet root;"' >> conf/local.conf 

    exit

    make build
    ```
