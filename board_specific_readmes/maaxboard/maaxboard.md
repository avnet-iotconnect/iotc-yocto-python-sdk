* Notes:
	* Based on the MaaXBoard [Development Guide](https://www.avnet.com/wps/wcm/connect/onesite/35645cc9-4317-4ca0-a2fa-30cce5f9ff17/MaaXBoard-Mini-Linux-Yocto-Lite-Development_Guide-V1.0-EN.pdf?MOD=AJPERES) from [this page](https://www.avnet.com/wps/portal/us/products/avnet-boards/avnet-board-families/maaxboard/maaxboard?utm_source=hackster)

## Build Instructions

These instructions are designed to get a Yocto image up and running for a specific board, these are simplified to get you to a similar point on each board and then you return to the main instructions of adding the IOTConnect layers to your build.

These instructions leverage the power of Docker to create a reproducible build that works across different OS environments, one of the main ideas is to avoid problems caused by having a too old/new version of Linux being used the Yocto build system, as those can cause build failures.

Provided in the folder are both the `Dockerfile` and `Makefile` to simplify the build process.

Tested on Ubuntu 22.04, 23.10

# Requirements
- Repo tool (from Google) - https://android.googlesource.com/tools/repo
- Docker - https://docs.docker.com/engine/install/ubuntu/ + https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user
- git name and email added to global scope

# Method
1. Create a work directory, for example ~/work
    ```bash
    cd ~/work
    ```

2. Create project directory and enter it
    ```bash
    mkdir imx-yocto-bsp && cd imx-yocto-bsp
    ```

3. Use repo tool to get the yocto sources
    ```bash
    repo init -u https://github.com/nxp-imx/imx-manifest  -b imx-linux-kirkstone -m imx-5.15.71-2.2.2.xml && repo sync
    
    git clone https://github.com/Avnet/meta-maaxboard.git -b kirkstone sources/meta-maaxboard
    ```

4.  Copy provided Makefile to project directory and execute these commands in the terminal
    ```bash
    make docker
    
    MACHINE=maaxboard source sources/meta-maaxboard/tools/maaxboard-setup.sh -b maaxboard/build
    
    exit
    
    make build
    # this will take a while as this is the initial build.
    ```

### Extras

Instructions for using a serial adapter and UART are found [here](https://www.hackster.io/monica/getting-started-with-maaxboard-headless-setup-24102b)  

If there are any problems during building then try:
    ```bash
        rm -rf ./maaxboard/build/tmp
        make build
    ```
