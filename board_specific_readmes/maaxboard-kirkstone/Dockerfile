# Use the base image from crops/poky with Ubuntu 20.04
FROM crops/poky:ubuntu-22.04

# Update package lists and install rsync
USER root
RUN apt-get update && \
    apt-get install -y \
    rsync

# Switch back to the original user
USER usersetup

