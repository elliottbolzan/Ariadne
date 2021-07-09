from os import listdir, makedirs
from os.path import dirname, isdir, isfile, join, realpath
from PIL import Image
import urllib.request

gorila_path = dirname(realpath(__file__)) + "/"

volume_count = 5
volume_names = ["1_1976", "2_1979", "3_1976", "4_1982", "5_1985"]
pages = [372, 162, 236, 222, 384]

images_path = str(gorila_path) + "images/"
volumes_path = str(gorila_path) + "volumes/"

if not isdir(images_path):
    makedirs(images_path)

if not isdir(volumes_path):
    makedirs(volumes_path)

# Download.
for volume_index in range(0, len(volume_names)):
    volume_name = volume_names[volume_index]
    volume_path = images_path + str(volume_index + 1) + "/"
    if not isdir(volume_path):
        makedirs(volume_path)
    max_pages = pages[volume_index]
    for page_number in range(1, max_pages + 1):
        online_path = "https://cefael.efa.gr/apps/library/services/images/?f=EtCret_21-" + volume_name + "_" + \
            f"{page_number:03d}" + ".jpg&p=jpg%2F150%2FEtCret%2FEtCret_21-" + \
            volume_name + "%2FEtCret_21-" + volume_name + "_VolumeBroche"
        image_path = volume_path + str(page_number) + ".jpg"
        try:
            urllib.request.urlretrieve(online_path, image_path)
        except Exception as e:
            print(e)
            continue

# Combine into PDFs.
for volume_index in range(1, volume_count + 1):
    images = []
    images_for_volume_path = images_path + str(volume_index) + "/"
    files = sorted([f for f in listdir(images_for_volume_path) if isfile(join(
        images_for_volume_path, f)) and ".jpg" in f], key=lambda x: int(x.split(".")[0]))
    for file in files:
        filepath = images_for_volume_path + file
        temp_image = Image.open(filepath)
        keep_image = temp_image.copy()
        images.append(keep_image)
        temp_image.close()
    volume_path = volumes_path + str(volume_index) + ".pdf"
    first_image = images[0]
    first_image.save(volume_path, "PDF", resolution=100.0,
                     save_all=True, append_images=images[1:])
