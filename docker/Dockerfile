FROM ros:foxy

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    unzip \
    libgtk-3-dev \
    libcanberra-gtk* \
    libtbb2 libtbb-dev \
    pkg-config \
    libgflags-dev \
    libgoogle-glog-dev \
    libatlas-base-dev \
    libeigen3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# -------------------------
# Install OpenCV 4.2.0
# -------------------------
RUN git clone --branch 4.2.0 https://github.com/opencv/opencv.git /opt/opencv && \
    git clone --branch 4.2.0 https://github.com/opencv/opencv_contrib.git /opt/opencv_contrib && \
    mkdir -p /opt/opencv/build && cd /opt/opencv/build && \
    cmake -D CMAKE_BUILD_TYPE=Release \
          -D CMAKE_INSTALL_PREFIX=/usr/local \
          -D OPENCV_EXTRA_MODULES_PATH=/opt/opencv_contrib/modules \
          -D BUILD_EXAMPLES=OFF \
          .. && \
    make -j$(nproc) && make install && ldconfig

# -------------------------
# Install Ceres Solver 1.14.0
# -------------------------
RUN git clone --branch 1.14.0 https://ceres-solver.googlesource.com/ceres-solver /opt/ceres && \
    mkdir /opt/ceres/build && cd /opt/ceres/build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF && \
    make -j$(nproc) && make install && ldconfig

# Source ROS 2 environment in every shell
RUN echo "source /opt/ros/foxy/setup.bash" >> /root/.bashrc

# Set default command
CMD ["/bin/bash"]

# -------------------------
# Setup User Environment
# -------------------------

# Set user arguments (being username, echo $UID, and id -g)
ARG USERNAME=dbutterfield3
ENV USERNAME=${USERNAME}
ARG USER_UID=3332128
ARG USER_GID=2626

# Create a non-root user with matching UID/GID
RUN groupadd --gid ${USER_GID} ${USERNAME} && \
    useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} && \
    usermod -aG sudo ${USERNAME} && \
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

#Add a custom .bashrc with warm colors and fixed hostname
RUN echo 'export PS1="\\[\\e[1;31m\\]\\u@vins_mono_ros\\[\\e[0m\\]:\\[\\e[1;33m\\]\\w\\[\\e[0m\\]\\$ "' > /home/${USERNAME}/.bashrc && \
    chown ${USERNAME}:${USERNAME} /home/${USERNAME}/.bashrc

# Set default user
USER ${USERNAME}
WORKDIR /home/${USERNAME}
SHELL ["/bin/bash", "-c"]

# Disable the sudo warning message on terminal open
RUN sudo echo ""

# Install tmuxp 
RUN sudo apt update
RUN sudo apt install tmux tmuxp -y
RUN touch ~/.tmux.conf && \
    echo "set -g mouse on" >> ~/.tmux.conf

# Install additional ROS utilities
RUN sudo apt install ros-foxy-rqt-graph ros-foxy-rviz-imu-plugin -y

# Source ROS2 environment for the user
RUN echo "source /opt/ros/foxy/setup.bash" >> /home/${USERNAME}/.bashrc

# Install Boost & image_transport
RUN sudo apt install libboost-all-dev ros-foxy-image-transport ros-foxy-cv-bridge ros-foxy-rviz2 -y

# Install additional plugins for rqt
RUN sudo apt install ros-foxy-rqt-* -y

# Ensure python points to system python 3.8
RUN sudo ln -sf /usr/bin/python3.8 /usr/bin/python

# Install Miniconda (non-interactive, no auto-init)
ENV MINICONDA_PATH=/opt/miniconda3
ENV PYTHONPATH=""

RUN sudo wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    sudo bash /tmp/miniconda.sh -b -p $MINICONDA_PATH && \
    sudo rm /tmp/miniconda.sh

# Disable auto-activation of conda base
RUN $MINICONDA_PATH/bin/conda config --set auto_activate_base false

# Install wandb in system Python 3.8
RUN /usr/bin/python -m pip install --no-cache-dir wandb

# Accept Miniconda TOS and create Python 3.10 environment
RUN $MINICONDA_PATH/bin/conda config --set always_yes yes && \
    $MINICONDA_PATH/bin/conda config --set changeps1 no && \
    $MINICONDA_PATH/bin/conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    $MINICONDA_PATH/bin/conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r && \
    $MINICONDA_PATH/bin/conda create -y -n robotdataprocess python=3.10

# Restore PYTHONPATH for ROS
ENV PYTHONPATH=/opt/ros/foxy/lib/python3.8/site-packages
