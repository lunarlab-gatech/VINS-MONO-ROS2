import wandb
import subprocess
import time
import os
from pathlib import Path
import signal

wandb.init()

# Set dataset number and robot name
dataset_number = "V1.4.1"
robot_name = "Drone1"

# Load sweep parameter values for this run
acc_n = wandb.config.acc_n  
gyr_n = wandb.config.gyr_n
acc_w = wandb.config.acc_w
gyr_w = wandb.config.gyr_w

# Launch the feature tracker node
feature_tracker_process = subprocess.Popen([
    "ros2", "launch", "feature_tracker", "vins_feature_tracker.launch.py", 
    f"config_path:=config/hercules/{dataset_number}/{robot_name}.yaml"
])

# Launch VINS-Mono Estimator with specified noise parameters
vins_est_process = subprocess.Popen([
    "ros2", "launch", "vins_estimator", "euroc.launch.py", 
    f"config_path:=config/hercules/{dataset_number}/{robot_name}.yaml",
    f"acc_n:={acc_n}", f"gyr_n:={gyr_n}",
    f"acc_w:={acc_w}", f"gyr_w:={gyr_w}"
])

# Launch the rosbag play command
time.sleep(2)
rosbag_process = subprocess.Popen([
    "ros2", "bag", "play", f"/home/dbutterfield3/data/Hercules_datasets/{dataset_number}/extract/bags_for_vins_mono/{robot_name}", 
    "--topics", "/imu", "/cam0", "/odom_gt", "/odom_gt/path"
])

# When the rosbag_process ends, wait 5 seconds and send shutdown signals to other processes
rosbag_process.wait()
time.sleep(5)
feature_tracker_process.send_signal(signal.SIGINT)
feature_tracker_process.wait()
vins_est_process.send_signal(signal.SIGINT)
vins_est_process.wait()

# After 30 seconds, terminate all processes
# time.sleep(10)
# rosbag_process.send_signal(signal.SIGINT)
# rosbag_process.wait()
# feature_tracker_process.send_signal(signal.SIGINT)
# feature_tracker_process.wait()
# vins_est_process.send_signal(signal.SIGINT)
# vins_est_process.wait()

# Get the path to the CSV with the final results
results_csv_path = Path(__file__).parent.parent / "output" / "hercules" / robot_name / "vins_result_no_loop.csv"

# Get the Conda Python with 3.10 for running robot data process
username = str(os.environ.get("USERNAME"))
conda_env_path = "/home/" + username + "/.conda/envs/robotdataprocess"
conda_python = os.path.join(conda_env_path, "bin", "python")

# Unset PYTHONPATH for isolation from ROS2 Python environment
conda_env = os.environ.copy()
conda_env.pop("PYTHONPATH", None)

# Run the evaluation script and log the results to WandB
completed_process = subprocess.run(
    [
        conda_python,
        "/home/" + username + "/vins_mono_ws/src/VINS-MONO-ROS2/research/vins_mono_sweep_eval.py",
        "--est_data_path", str(results_csv_path),
        "--gt_data_path", "/home/" + username + "/data/Hercules_datasets/" 
            + dataset_number + "/extract/files_for_roman_baseline/" + robot_name + "/poseGT.csv"
    ],
    env=conda_env,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

rms_ate = None
for line in completed_process.stdout.splitlines():
    if "RMS ATE:" in line:
        rms_ate = float(line.split("RMS ATE:")[1].strip())
        break

wandb.log({"RMS_ATE": rms_ate})
