* Notes:
	* Based on the [meta-rzboard](https://github.com/Avnet/meta-rzboard/tree/rzboard_dunfell_5.10_v2) repository
    * Flashing instructions based on [Build, Deploy, & Run a Qt Enabled Image on the RZBoard V2L](https://www.hackster.io/lucas-keller/build-deploy-run-a-qt-enabled-image-on-the-rzboard-v2l-de6c41#toc-hardware-configuration-11)

## Build Instructions

These instructions are designed to get a Yocto image up and running for a specific board, these are simplified to get you to a similar point on each board and then you return to the main instructions of adding the IOTConnect layers to your build.

These instructions leverage the power of Docker to create a reproducible build that works across different OS environments, one of the main ideas is to avoid problems caused by having a too old/new version of Linux being used the Yocto build system, as those can cause build failures.

Provided in the folder are both the `Dockerfile` and `Makefile` to simplify the build process.

Tested on Ubuntu 22.04

# Requirements
- Docker - https://docs.docker.com/engine/install/ubuntu/ + https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user
- git name and email added to global scope

# Method
1. Create a work directory, for example ~/work
    ```bash
    cd ~/work
    ```

2. Create project directory and enter it
    ```bash
    mkdir rzboardv2l && cd $_
    ```

3. Download the following packages manually and place inside `rzboardv2l` directory

| Package Name                  | Version                    | Download File                               |
| ----------------------------- | -------------------------- | ------------------------------------------- |
| RZ/V Verified Linux Package   | V3.0.2             | [RTK0EF0045Z0024AZJ-v3.0.2.zip](https://www.renesas.com/us/en/document/swo/rzv-verified-linux-package-v302rtk0ef0045z0024azj-v302zip?r=1628526) |
| RZ MPU Graphics Library       | Evaluation Version V1.4 | [RTK0EF0045Z13001ZJ-v1.4_EN.zip](https://www.renesas.com/us/en/document/swo/rz-mpu-graphics-library-evaluation-version-rzv2l-rtk0ef0045z13001zj-v14enzip?r=1843541) |
| RZ MPU Codec Library          | Evaluation Version V1.0.1 | [RTK0EF0045Z15001ZJ-v1.0.1_EN.zip](https://www.renesas.com/us/en/document/swo/rz-mpu-video-codec-library-evaluation-version-rzv2l-rtk0ef0045z15001zj-v101enzip?r=1844066) |
| RZ/V2L DRP-AI Support Package | V7.30                      | [r11an0549ej0730-rzv2l-drpai-sp.zip](https://www.renesas.com/us/en/document/sws/rzv2l-drp-ai-support-package-version-730?r=1558356) |
| RZ/V2L Multi-OS Package       | V1.10                      | [r01an6238ej0110-rzv2l-cm33-multi-os-pkg.zip](https://www.renesas.com/us/en/document/sws/rzv-multi-os-package-v110) |


7. wget the docker and makefile
```bash
    wget https://raw.githubusercontent.com/avnet-iotconnect/iotc-yocto-python-sdk/dunfell/board_specific_readmes/rzboardv2l/Dockerfile
    wget https://raw.githubusercontent.com/avnet-iotconnect/iotc-yocto-python-sdk/dunfell/board_specific_readmes/rzboardv2l/Makefile
    make docker
```

4. wget and execute project setup script
``` bash
    wget https://raw.githubusercontent.com/Avnet/meta-rzboard/rzboard_dunfell_5.10_v2/tools/create_yocto_rz_src.sh
    chmod a+x create_yocto_rz_src.sh
    ./create_yocto_rz_src.sh
```

5. clone meta-rzboard
```bash
    cd ./yocto_rzboard
    git clone https://github.com/Avnet/meta-rzboard.git -b rzboard_dunfell_5.10_v2 
```

6. copy over build conf
```bash
    mkdir -p ./build/conf
    cp meta-rzboard/conf/rzboard/* build/conf/
    exit
```

8.
```bash
    make build
```
### Extras

If there are any problems during building then running sequential builds as sometimes some dependencies are built out of sequence:
    ```bash
        make build
    ```
