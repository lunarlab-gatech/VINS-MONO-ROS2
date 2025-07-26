DATA_DIR='/media/dbutterfield3/T73'
ROS_WS_DIR='/home/dbutterfield3/Research/ros_workspaces/vins_mono_ws'

docker run -it \
    --name="vins_mono_ros" \
    --net="host" \
    --privileged \
    --gpus="all" \
    --workdir="/home/$USER/vins_mono_ws" \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --env="XAUTHORITY=/tmp/.Xauthority" \
    --env="USER_ID=$(id -u)" \
    --env="GROUP_ID=$(id -g)" \
    --volume="$ROS_WS_DIR:/home/$USER/vins_mono_ws" \
    --volume="$DATA_DIR:/home/$USER/data" \
    --volume="/home/$USER/.bash_aliases:/home/$USER/.bash_aliases" \
    --volume="/home/$USER/.ssh:/home/$USER/.ssh:ro" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="$XAUTHORITY:/tmp/.Xauthority:ro" \
    vins_mono_ros  \
    /bin/bash
