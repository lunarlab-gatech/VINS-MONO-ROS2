import argparse
from decimal import Decimal
import numpy as np
from robotdataprocess.data_types.OdometryData import OdometryData, CoordinateFrame
from pprint import pprint
from scipy.spatial.transform import Rotation as R

def main(est_data_path=None, gt_data_path=None):
    # Load estimated data and convert into proper coordinate frame
    est_data = OdometryData.from_csv(est_data_path, "world", "robot", CoordinateFrame.FLU, True, None)

    R_NED = np.array([[1,  0,  0],
                      [0, -1,  0],
                      [0,  0, -1]])
    R_NED_Q = R.from_matrix(R_NED)
    est_data._ori_apply_rotation(R_NED_Q.inv())
    est_data._ori_change_of_basis(R_NED_Q)

    # Load ground truth data
    gt_data = OdometryData.from_csv(gt_data_path, "world", "robot", CoordinateFrame.FLU, True, None)

    # Calculate RMS ATE and print it
    metrics_dictionary: dict = OdometryData.calculate_trajectory_errors(gt_data, est_data, max_diff=0.1)
    print("RMS ATE: ", metrics_dictionary['APE']['translation_part']['rmse'])

if __name__ == "__main__":
    # Parse overwrite arguments for est_data_path and gt_data_path if provided
    parser = argparse.ArgumentParser()
    parser.add_argument('--est_data_path', type=str, help='Path to the estimated data CSV file')
    parser.add_argument('--gt_data_path', type=str, help='Path to the ground truth data CSV file')
    args = parser.parse_args()

    main(est_data_path=args.est_data_path, gt_data_path=args.gt_data_path)