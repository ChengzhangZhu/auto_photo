import os
import exifread
from shutil import copyfile
from tqdm import tqdm


def list_all_files(root_dir):
    _files = []
    file_list = os.listdir(root_dir)
    for i in range(0, len(file_list)):
        path = os.path.join(root_dir, file_list[i])
        if os.path.isdir(path):
            _files.extend(list_all_files(path))
        if os.path.isfile(path):
            _files.append(path)
    return _files


def get_exif(old_full_file_name, org_path, period='d'):
    """

    :param old_full_file_name: original file name
    :param org_path: organized file path
    :param period: the organized period, support 'd' for day, 'm' for month, 'y' for year
    :return:
    """
    # old_full_file_name = os.path.join(img_path, file_name)
    img_path, file_name = os.path.split(old_full_file_name)
    field = 'EXIF DateTimeOriginal'
    fd = open(old_full_file_name, 'rb')
    tags = exifread.process_file(fd)
    fd.close()

    if field in tags:
        photo_time = str(tags[field]).split(' ')[0].replace(':', '_')
        new_name = str(tags[field]).replace(':', '').replace(' ', '_') + os.path.splitext(file_name)[1]

        # process year, month, day
        year = photo_time.split('_')[0]
        month = photo_time.split('_')[1]
        day = photo_time.split('_')[2]

        new_path = org_path
        period = list(period)
        if 'y' in period:
            new_path = os.path.join(new_path, year)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
        if 'm' in period:
            new_path = os.path.join(new_path, year+'_'+month)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
        if 'd' in period:
            new_path = os.path.join(new_path, year+'_'+month+'_'+day)
            if not os.path.exists(new_path):
                os.makedirs(new_path)

        new_full_file_name = os.path.join(new_path, new_name)
        copyfile(old_full_file_name, new_full_file_name)
    else:
        # print('No {} found'.format(field), ' in: ', old_full_file_name)
        new_path = os.path.join(org_path, 'others')
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        new_full_file_name = os.path.join(new_path, file_name)
        copyfile(old_full_file_name, new_full_file_name)


def organize(file_path, org_path, organized_files=None, period='d'):
    if organized_files is None:
        organized_files = list()
    candidate = list_all_files(file_path)
    processing_file = list()
    for i in candidate:
        if i not in organized_files:
            processing_file.append(i)
    for filename in tqdm(processing_file):
        full_file_name = os.path.join(file_path, filename)
        if os.path.isfile(full_file_name):
            try:
                get_exif(full_file_name, org_path, period)
            except:
                img_path, file_name = os.path.split(full_file_name)
                new_path = os.path.join(org_path, 'others')
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                new_full_file_name = os.path.join(new_path, file_name)
                copyfile(full_file_name, new_full_file_name)
            organized_files.append(full_file_name)
    return organized_files
