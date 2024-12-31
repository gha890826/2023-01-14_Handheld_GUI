# Write by ck
# This program show the zed serial number and available video mode

import pyzed.sl as sl


def zed_speed_test():
    print("Start ZED speed test")
    zed = sl.Camera()

    init_params = sl.InitParameters()
    init_params.sdk_verbose = False
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("err")

    # Get camera information (ZED serial number)
    zed_serial = zed.get_camera_information().serial_number
    print("serial number: {0}".format(zed_serial))
    zed.close()

    print("start check connection speed ...")
    init_params = sl.InitParameters()
    video_mode = [sl.RESOLUTION.HD2K, sl.RESOLUTION.HD1080, sl.RESOLUTION.HD720, sl.RESOLUTION.VGA]
    video_fps = [[15], [15, 30], [15, 30, 60], [15, 30, 60, 100]]
    for mode in video_mode:
        print("\n" + str(mode) + ":")
        init_params.camera_resolution = mode
        for fps in video_fps[video_mode.index(mode)]:
            # print(fps)
            init_params.camera_fps = fps
            err = zed.open(init_params)
            if err == sl.ERROR_CODE.SUCCESS:
                print(str(fps) + "fps is ok")
            else:
                print(str(fps) + "fps fail")
            zed.close()


if __name__ == "__main__":
    zed_speed_test()