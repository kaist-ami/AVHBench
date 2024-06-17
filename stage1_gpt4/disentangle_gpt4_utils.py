from openai import OpenAI
from glob import glob
import json
import os

import numpy as np
import re

with open('./caption/sample_captions.json', 'r') as f:
    all_captions = json.load(f)

def set_content(input_type, input_):
    type_dict = {'audiocaps':'audio events', 'valor':'audio-visual events', 'mixed':'audio and audio-visual events'}
    QUERY="""\
The “caption” provides the explation about %s. The “visual tagging” identifies the observable visual objects or actions. If similar objects from the “caption” are found in the “visual tagging”, it is assumed to exist in-view. If not, it is assumed they exist out-of-view. The “information” aims summarize the inferable audio and visual information: In-view sound source is the object that makes sound and is visible in the scene. In-view sound is the type of sound that the object in the scene makes, In-view silent object is the object that does not make sound but is visible in the scene, Out-of-view sound source is the expected object that makes sound and is not visible in the scene, and Out-of-view sound is the type of sound that the object out of the scene makes.

#### caption: A motorboat engine is running, and a man speaks.
#### visual tagging: attach | boat | computer | laptop | open | seat | sit | cloth | computer | curtain | laptop | open | sit | white | computer | lap | laptop | open | seat | sit
#### information: 
- In-view sound source: boat
- In-view silent object: laptop, cloth
- Out-of-view sound source: man
- In-view sound: engine running
- Out-of-view sound: man’s voice

#### caption: A man speaking and item beeping.
#### visual tagging: attach | bathroom | bathroom accessory | control | floor | meter | remote | shower head | tile wall | attach | bathroom | control | electronic | floor | meter | pole | remote | thermometer | tile wall | catch | control | hand | floor | person | meter | remote | selfie | thermometer | tile wall
#### information:
- In-view sound source: thermometer
- In-view silent object: tile wall
- Out-of-view sound source: man
- In-view sound: beeping
- Out-of-view sound: man’s voice

By referencing the above examples, please extract the In-view sound source, In-view silent object, Out-of-view sound source, In-view sound, and Out-of-view sound. Print the caption and information in order, sdo not print already given visual tagging.

%s
"""%(type_dict[input_type],input_)

    return QUERY

def parse_tags(video_name):    
    path = './visual_tagging/sample_tags.json'
    with open(path, 'r') as f:
        tags = json.load(f)[video_name]
    
    cur_image_tags = []
    
    score_dict = {}
    for each_frame in tags:
        each_frame = [each.strip() for each in each_frame]
        cur_image_tags.extend(each_frame)
        
        for each in each_frame:
            if each not in score_dict:
                score_dict[each] = 1
            else:
                score_dict[each] += 1
                
    cur_image_tags = list(set(cur_image_tags))#
    cur_image_tags.reverse()
    
    avg = int(sum(score_dict.values()) / len(score_dict))
    values = sorted(score_dict.values(), reverse=True)[:len(score_dict) * 18 // 30]
    median = values[len(values) // 2] if len(values) % 2 != 0 else (values[len(values) // 2 - 1] + values[len(values) // 2]) / 2

    
    tags = [each for each in score_dict if score_dict[each]>=median]
        
    return tags, score_dict

def make_inputs(img_name_list): # 5개씩
    num = len(img_name_list)
    img_name_list = [each.split('/')[-1] for each in img_name_list]
    
    all_prompt = ''

    for each in img_name_list:
        tags, score_dict = parse_tags(each)
        tags = ' | '.join(tags)
        
        if each in all_captions:
            if 'audio caption' in all_captions[each]:
                caption = all_captions[each]['audio caption']
                
            elif 'audio-visual caption' in all_captions[each]:
                caption = all_captions[each]['audio-visual caption']
            
        else:
            # print("No caption for ", each)
            caption = all_captions[each+'.000']
            caption=''
            if 'audio caption' in all_captions[each+'.000']:
                caption = all_captions[each+'.000']['audio caption'].strip()
                
            elif 'audio-visual caption' in all_captions[each+'.000']:
                caption = all_captions[each+'.000']['audio visual caption'].strip()
        
        all_prompt += """\
#### caption: %s
#### visual tagging: %s            
#### information:

"""%(caption, tags)
    
    return all_prompt
        
def manage_text(text):
    if ',' in text:
        text = text.split(',')
    
        retlist = []
        for each in text:
            each = each.strip()
            if '(' in each:
                each = each.split('(')[0].strip()
            retlist.append(each)
            
        return retlist
    
    else:
        return text.strip()
