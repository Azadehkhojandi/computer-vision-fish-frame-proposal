#########################################################################
# Purpose:  Script to run the Microsoft Computer Vision API to do a 
# binary classification of frames in a video into "object"/"no object"
# information and separating frames into appropriate folders for further
# processing.
#
# Author:  Micheleen Harris (with original code by Azadeh Khojandi)
#
# Example from command line:
#   python classify_and_get_object_frames.py --sub_key <subscription key> --conf_thresh 0.6 --video_path videos/video1.mp4 --secs_pe 2 --object_name fish
#########################################################################


import os
from matplotlib import figure
from PIL import Image, ImageOps
from matplotlib import pyplot as plt
import base64
import json
import pandas as pd
import numpy as np
import cv2
import requests
import math
import time
import shutil
import argparse
import io


print('cv2 version:',cv2.__version__)

######################### DEFAULT VALUES #########################

DEFAULT_VIDEO_PATH = './data/fish_pics/video1.mp4'
DEFAULT_BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/'
DEFAULT_EXPORT_PATH = 'exported_frames'
DEFAULT_OBJECT_NAME = 'obj'
DEFAULT_CONFIDENCE_THRESHOLD = 0.2
DEFAULT_EXPORTED_FRAMES_PER_SEC = 2

######################### PROCESS COMMAND-LINE ARGS #########################

parser = argparse.ArgumentParser(
    description='Finding single objects through binary classification with \
        the Microsoft Computer Vision API')                 
parser.add_argument('--video_path', default=DEFAULT_VIDEO_PATH, type=str,
                    help='Video file path')
parser.add_argument('--export_dir', default=DEFAULT_EXPORT_PATH, type=str,
                    help='Export directory name')
parser.add_argument('--sub_key',
                    help='Computer Vision API subscription key')
parser.add_argument('--base_url', default=DEFAULT_BASE_URL, type=str,
                    help='Computer Vision API base URL')
parser.add_argument('--object_name', default=DEFAULT_OBJECT_NAME, type=str,
                    help='Name of object for output dirs')
parser.add_argument('--conf_thresh', default=DEFAULT_CONFIDENCE_THRESHOLD, type=float,
                    help='Confidence threshold from 0-1')
parser.add_argument('--secs_pe', default=DEFAULT_EXPORTED_FRAMES_PER_SEC, type=int,
                    help='Seconds per frame extraction, e.g, if equals 2, export frame every 2 seconds')
args = parser.parse_args()


######################### DEFINE METHODS #########################

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def normalize(arr):
    """
    Linear normalization
    http://en.wikipedia.org/wiki/Normalization_%28image_processing%29
    """
    arr = arr.astype('float')
    # Do not touch the alpha channel
    for i in range(3):
        minval = arr[...,i].min()
        maxval = arr[...,i].max()
        if minval != maxval:
            arr[...,i] -= minval
            arr[...,i] *= (255.0/(maxval-minval))
    return arr

def analyse(imagepath):
    
    # Replace <Subscription Key> with your valid subscription key.
    subscription_key = args.sub_key
    assert subscription_key

    # You must use the same region in your REST call as you used to get your
    # subscription keys. For example, if you got your subscription keys from
    # westus, replace "westcentralus" in the URI below with "westus".
    #
    # Free trial subscription keys are generated in the westcentralus region.
    # If you use a free trial subscription key, you shouldn't need to change
    # this region.
    
    vision_base_url = args.base_url
    api_url = vision_base_url + "analyze"
    
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params   = {'visualFeatures': 'Tags,Description'}

    # Open image file and pixel intensity normalize individual RGB channels
    img = Image.open(imagepath).convert('RGBA')
    arr = np.array(img)
    img_data = Image.fromarray(normalize(arr).astype('uint8'),'RGBA')

    # Save a normalized version to export path
    img_data_save = img_data.convert('RGB')
    img_data_save.save(imagepath.replace('.jpg', '_processed.jpg'))

    # Convert to bytes object for serialization and sending to REST endpoint
    img_byte_arry = io.BytesIO()
    img_data.save(img_byte_arry, format='PNG')
    img_data = img_byte_arry.getvalue()

        
    response = requests.post(api_url,params=params,headers=headers,data=img_data)
    
    try:
          response.raise_for_status()
    except:
        print(response)
        print(response.json())
        print('error:',imagepath)
     
    analysis = response.json()
    return analysis

def makedir(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print ('Error: Creating directory ' + dir)

def exportframes(videoPath,outputpath,secs_per_export=2):
    
    print('exportig frames to %s' % (outputpath) )
    vidcap = cv2.VideoCapture(videoPath)
    success,np_image = vidcap.read()
    fps=vidcap.get(cv2.CAP_PROP_FPS)

    #number of frames to export per second
    fpsexport = int(fps * secs_per_export)

    print('exporting frame every %s second' %(secs_per_export))
    count = 0
    success = True
    while success:
        if (count % fpsexport) ==0:
            tmpimagepath=os.path.join(outputpath,'frame_%04d.jpg' % count).replace('\\','/') 
            cv2.imwrite(tmpimagepath, np_image)     # save frame as JPEG file
        success,np_image = vidcap.read()
        count += 1

    print('exporting finished....')

def analyseframes(outputpath):
    
    
    print('analysing exported frames from %s' %(outputpath))
    
    frames =[]
    tags =[]
    texts =[]
    imagepaths =[]
    confidences=[]
    cnt = 0
    for (dirpath, dirnames, filenames) in os.walk(outputpath):
        for filename in filenames:
            if filename.endswith('.jpg'): 
                imagepath = os.path.join(dirpath, filename).replace('\\','/') 
                #print(imagepath)
                frame = filename.split('.')[0].replace('frame_','')
                print('analysing', imagepath)

                result=analyse(imagepath)
                #print ('%s frame - %s ' %(frame,imagepath))
                #print(result)
                if ('tags' in result):
                    alltagnames=[x['name'] for x in result['tags']]
                    if ('description' in result 
                        and 'captions' in result['description'] 
                        and len(result['description']['captions'])>0):
                        text=result['description']['captions'][0]['text']
                        confidence=result['description']['captions'][0]['confidence']
                    else:
                        text=""
                        confidence=""
                    frames.append(frame)
                    tags.append(' '.join(alltagnames))
                    texts.append(text)
                    imagepaths.append(imagepath)
                    confidences.append(confidence)
        # Pause x seconds so as not to exceed rate of API requests
        time.sleep(30)

    np_frames =np.array(frames)
    np_tags =np.array(tags)
    np_texts =np.array(texts)
    np_imagepaths =np.array(imagepaths)
    np_confidences=np.array(confidences)

    d = {'frame': np_frames, 'tags': np_tags, 'text':np_texts, 'imagepath':np_imagepaths,'confidence':np_confidences}

    df = pd.DataFrame(data=d)
    
    print('analysing finished....')
    return df

def getexportfolderpath(videoPath,exportPath):
    if not os.path.exists(videoPath):
        raise ValueError('video path is invalid',videoPath)
    videofile = os.path.basename(videoPath)  # os independent
    videoname = '.'.join(videofile.split('.')[:-1])
    outputpath=os.path.join(exportPath,videoname).replace('\\','/')
    return outputpath


######################### RUN CODE #########################

# Video path
videofilePath=args.video_path

# Define dirs
exportPath = args.export_dir
outputpath = getexportfolderpath(videofilePath, exportPath)
csv_path = os.path.join(outputpath, 'result.csv')
obj_path = os.path.join(outputpath, args.object_name)
no_obj_path = os.path.join(outputpath, 'not_'+args.object_name)
outputpath_list = [outputpath, obj_path, no_obj_path]

# Delete object output dirs because we want to start fresh
if os.path.exists(obj_path):
    shutil.rmtree(obj_path)
if os.path.exists(no_obj_path):
    shutil.rmtree(no_obj_path)

# Create dirs
for path in outputpath_list:
    if not os.path.exists(path):
        os.makedirs(path)

# Export frames
secs_per_export = args.secs_pe # seconds to capture frame
exportframes(videofilePath, outputpath, secs_per_export)
print(exportPath, outputpath)

if not os.path.exists(csv_path):
    # Analyze and get all tags/descriptions
    df = analyseframes(outputpath)
    df['confidence'] = pd.to_numeric(df['confidence'])
    total_rows,total_col= df.shape
    
    print('%s frames analysed' % total_rows)

    # Write results files
    print(outputpath)
    df.to_csv(csv_path)
    result_fish = df[df['tags'].str.contains(args.object_name)]
else:
    df = pd.read_csv(csv_path)
    result_fish = df[df['tags'].str.contains(args.object_name)]
print('df shape', df.shape)

# If there is an object present with sufficient confidence,
# save to obj_path folder, if not then no_obj_path
print(df.loc[:, 'frame'])
obj_cnt = 0
for i in range(len(df.loc[:, 'frame'])):
    # Get frame information
    res = df.iloc[i, :]
    res_frame = res['frame']
    res_tag = res['tags']
    res_conf = res['confidence']
    print(res_tag)
    # Name of frame file and locations
    frame_name = 'frame_{:04d}.jpg'.format(int(res_frame))
    old_frame_path = os.path.join(outputpath, frame_name)
    old_frame_path_proc = os.path.join(outputpath, frame_name.replace('.jpg', '_processed.jpg'))
    new_frame_path_no_obj_proc = os.path.join(no_obj_path, frame_name.replace('.jpg', '_processed.jpg'))
    new_frame_path_obj_proc = os.path.join(obj_path, frame_name.replace('.jpg', '_processed.jpg'))

    # Filter by user-defined confidence threshold (keep NaNs just in case)
    if float(res_conf) < float(args.conf_thresh):
        print('frame {} - too low of confidence :( '.format(res_frame))
        new_frame_path = os.path.join(no_obj_path, frame_name)
        # Could change these "copyfile"'s to "move"'s to not duplicate images
        shutil.copyfile(old_frame_path, new_frame_path)
        shutil.copyfile(old_frame_path_proc, new_frame_path_no_obj_proc)
        continue
    # Does have object?
    # Move the frame to the object directory
    if args.object_name in res_tag:
        print('frame {} - has {} with sufficient confidence :)'.format(res_frame, 
            args.object_name))
        new_frame_path = os.path.join(obj_path, frame_name)
        shutil.copyfile(old_frame_path, new_frame_path)
        shutil.copyfile(old_frame_path_proc, new_frame_path_obj_proc)
        obj_cnt += 1
    else:
        print('frame {} - does not have any {} tags :('.format(res_frame,
            args.object_name))
        new_frame_path = os.path.join(no_obj_path, frame_name)
        shutil.copyfile(old_frame_path, new_frame_path)
        shutil.copyfile(old_frame_path_proc, new_frame_path_no_obj_proc)

print('%s frames detected with fish' % obj_cnt)
result_fish.to_csv(os.path.join(outputpath, 'result_fish.csv'))
