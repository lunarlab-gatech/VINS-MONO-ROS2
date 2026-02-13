DATA_DIR='/media/dbutterfield3/T73/'
ROS_WS_DIR='/home/dbutterfield3/Research/ros_workspaces/vins_mono_ws'

docker run -it \
    --name="vins_mono_ros" \
    --shm-size=2gb \
    --net="host" \
    --privileged \
    --gpus="all" \
    --device /dev/dri \
    --workdir="/home/$USER/vins_mono_ws" \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --env="XAUTHORITY=/tmp/.Xauthority" \
    --env="XDG_RUNTIME_DIR=/tmp/runtime-$USER" \
    --env="USER_ID=$(id -u)" \
    --env="GROUP_ID=$(id -g)" \
    --volume="$ROS_WS_DIR:/home/$USER/vins_mono_ws" \
    --volume="$DATA_DIR:/home/$USER/data" \
    --volume="/home/$USER/.bash_aliases:/home/$USER/.bash_aliases" \
    --volume="/home/$USER/.ssh:/home/$USER/.ssh:ro" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="/tmp/runtime-$USER:/tmp/runtime-$USER" \
    --volume="$XAUTHORITY:/tmp/.Xauthority:ro" \
    --volume="$HOME/.bash_aliases:/root/.bash_aliases:ro" \
    --volume="$HOME/.ssh:/root/.ssh:ro" \
    vins_mono_ros  \
    /bin/bash
