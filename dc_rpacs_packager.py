###############################################################################
# This is a short script for copying structural DICOM scan folders from 
# recently scanned/acquired Dyslexia Center cases in the L Drive to the rPACS
# directory and then tar-gz zipping them to prepare them for upload to 
# Research Radiology PACS (rPACS) for review by the radiologists:
# by: Rian Bogley
###############################################################################
# %% ##########################################################################
# Import modules
import tarfile
import os
import shutil
###############################################################################
# %% ##########################################################################
# Set Variables:
# Original scans directory filepath:
scans_dir = 'L:/language/Dyslexia_project/Participants/'
# rPACS upload directory filepath:
rPACS_dir = 'L:/language/Dyslexia_project/ResearchRadiologyPACS/Not_Uploaded/'
# Scan prefixes to be copied:
scan_prefixes = ('dc', 'adys', 'leegt')
# Scan types to be copied:
scan_types = [
    't1_mp2rage_jose_UNI_Images',
    'T1_mprage_ND',
    't2_flair_sag_p3_ND',
    't2_space_sag_iso_p2_ND',
    'dti_2mm_m3p2_b2500_96dir_10b0s_TRACEW',
    'dti_2mm_m3p2_b2500_96dir_10b0s_ADC',
    't1_space_ir_cor_p2_iso',
    't2_tse_dark-fluid_tra_3mm'
    ]
###############################################################################
# %% ##########################################################################
# Find all folders in scans_dir that begin with specified prefixes
# i.e. 'DC', 'ADYS', or 'LEEGT' (not case sensitive).
# Then, make a copy of just the folder name in a list:
new_scans = [f for f in os.listdir(scans_dir) 
if f.lower().startswith(scan_prefixes)]

# Check if list of found scans in new_scans already exist and are 
# compressed in rPACS_dir. If so, remove them from the list:
for root, dirs, files in os.walk(rPACS_dir):
    for file in files:
        if file.endswith('.tgz'):
            if file[:-4] in new_scans:
                print('Case: ' + file[:-4] + 
                ' is already compressed in rPACS_dir, skipping.')
                new_scans.remove(file[:-4])

# Print which remaining scans will be copied:
print('The following scans will be copied:')
for scan in new_scans:
    print(scan)
###############################################################################
# %% ##########################################################################
# For each case in the list, make a new folder in rPACS_dir:
for new_scan in new_scans:
    os.mkdir(rPACS_dir + new_scan)
    # Then, copy any specified scan subfolders from the original scans_dir
    # to the new folder in rPACS_dir:
    for root, dirs, files in os.walk(scans_dir + new_scan):
        for dir in dirs:
            if any(s in dir for s in scan_types):
                shutil.copytree(os.path.join(root, dir), 
                os.path.join(rPACS_dir + new_scan, dir))
    # Remove any potentially created NifTI files (ending in .nii or .nii.gz)
    # from the new folder to leave only the DICOM files for upload:
    for root, dirs, files in os.walk(rPACS_dir + new_scan):
        for file in files:
            if file.endswith(('.nii', '.nii.gz')):
                os.remove(os.path.join(root, file))
    # Compress the newly created folder into a tar.gz file (.tgz):
    with tarfile.open(rPACS_dir + new_scan + '.tgz', 'w:gz') as tar:
        tar.add(rPACS_dir + new_scan, arcname=new_scan)
    # Use shutil to remove the copied folder and all its contents:
    shutil.rmtree(rPACS_dir + new_scan)
# %% ##########################################################################
# If any tar.gz files in the rPACS_dir are over 80MB, 
# print their names and file size:
# Compressed files over 80MB will generally not upload properly to rPACS.
# If any are found, please check them and remove any extraneous scans
# before uploading.
# The order of priority of scans to delete is the same as the order they are
# listed in scan_types above (with the scans at the top of the list being
# the most important to keep, and the scans at the bottom of the list being
# the least important to keep).
for root, dirs, files in os.walk(rPACS_dir):
    for file in files:
        if file.endswith('.tgz'):
            if os.path.getsize(rPACS_dir + file) > 80000000:
                print('File: ' + file + ' is over 80MB (',str(
                    os.path.getsize(rPACS_dir + file)/1000000
                    ) ,'MB), please check it.')
###############################################################################