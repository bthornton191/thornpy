from scipy.spatial.transform import Rotation as R

def euler_to_matrix(euler, sequence='ZXZ', degrees=False):
    """Convert Euler angles to rotation matrix.

    Parameters
    ----------
    euler : array_like
        Euler angles in radians.
    sequence : str, optional
        Euler sequence. Use capital to indicate extrinsic rotations. Default is 'ZXZ'.

    Returns
    -------
    matrix : ndarray
        Rotation matrix.

    """
    rot: R = R.from_euler(sequence, euler, degrees=degrees)
    return rot.as_matrix()
