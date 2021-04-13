# helper functions for downloading and preprocessing SMPLpix training data
#
# (c) Sergey Prokudin (sergey.prokudin@gmail.com), 2021
#

import os

def download_dropbox_url(url, filepath, chunk_size=1024):

    import requests
    headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}
    r = requests.get(url, stream=True, headers=headers)
    with open(filepath, 'wb') as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
    return

def unzip(zip_path, target_dir, remove_zip=True):
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
    if remove_zip:
        os.remove(zip_path)
    return


def download_and_unzip(dropbox_url, workdir):

    if not os.path.exists(workdir):
        print("creating workdir %s" % workdir)
        os.makedirs(workdir)

    data_zip_path = os.path.join(workdir, 'data.zip')
    print("downloading zip from dropbox link: %s" % dropbox_url)
    download_dropbox_url(dropbox_url, data_zip_path)
    print("unzipping %s" % data_zip_path)
    unzip(data_zip_path, workdir)
    data_dir = os.path.join(workdir, 'dropbox_data')
    print("data loaded and stored at %s" % data_dir)

    return data_dir

def get_amass_cmu_sketch_data(workdir):

    if not os.path.exists(workdir):
        print("creating workdir %s" % workdir)
        os.makedirs(workdir)

    data_zip_url = 'https://www.dropbox.com/s/nptjx8najw3t17c/amass_cmu_renders_kabarov_sketches.zip?dl=0'
    data_zip_path = os.path.join(workdir, 'amass_cmu_renders_kabarov_sketches.zip')
    print("downloading zip from dropbox link: %s" % data_zip_url)
    download_dropbox_url(data_zip_url, data_zip_path)
    print("unzipping %s" % data_zip_path)
    unzip(data_zip_path, workdir)
    data_dir = os.path.join(workdir, 'amass_cmu_renders_kabarov_sketches')
    print("data loaded and stored at %s" % data_dir)
    amass_cmu_renders_dir = os.path.join(data_dir, 'amass_cmu_renders')
    sketches_dir = os.path.join(data_dir, 'sketches')

    return amass_cmu_renders_dir, sketches_dir

def generate_mp4(image_dir, video_path, frame_rate=15, img_ext=None):

    if img_ext is None:
        test_img = os.listdir(image_dir)[0]
        img_ext = os.path.splitext(test_img)

    ffmpeg_cmd = "ffmpeg -framerate %d -pattern_type glob " \
                "-i \'%s/*%s\' -vcodec h264 -an -b:v 1M -pix_fmt yuv420p -an \'%s\'" % \
                (frame_rate, image_dir, img_ext, video_path)

    print("executing %s" % ffmpeg_cmd)
    exit_code = os.system(ffmpeg_cmd)

    if exit_code != 0:
        print("something went wrong during video generation. Make sure you have ffmpeg tool installed.")

    return exit_code