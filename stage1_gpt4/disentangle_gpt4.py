from openai import OpenAI
from glob import glob
import json
import os

import numpy as np
import re

from disentangle_gpt4_utils import set_content, parse_tags, make_inputs, manage_text

DEBUG = True

API_KEY="YOUR API KEY HERE"
client = OpenAI(api_key=API_KEY)

####################### ADD YOUR VIDEO PATHS HERE
sample_videos = ['00006', '00159', '00175', '00191', '00251', '00348', '00500', '00528', '00641', '00669', '00732', '00765', '00970', '01256', '01348', '01352', '01358', '01460', '01476', '01480', '01574', '01676', '01726', '01782', '02010', '02030', '02124', '02180', '02198', '02302']


all_video_paths = sample_videos
print('all_video_paths', len(all_video_paths))

####################### LOAD SAVEDICT
cnt=0
savedict = {}
raw_savedict = []    
savedict_path = './stage1_output/gpt_output.json'
if os.path.exists(savedict_path):
    with open(savedict_path, 'r') as f:
        savedict = json.load(f)    
raw_savedict_path = './stage1_output/gpt_raw_output.json'
if os.path.exists(raw_savedict_path):
    with open(raw_savedict_path, 'r') as f:
        raw_savedict = json.load(f)
        
####################### START ITERATING
for i in range(0, len(all_video_paths), 5):
    cnt+=1

    cur_iter_video_paths = all_video_paths[i:i+5]
    if all([each.split('/')[-1] in savedict for each in cur_iter_video_paths]):
        continue
    else:
        print('starting: %s to %s'%(cur_iter_video_paths[0], cur_iter_video_paths[-1]))
    
    input_ = make_inputs(cur_iter_video_paths)
    query = set_content('audiocaps', input_)

    if DEBUG:
        print(query)
        print("===================")
        # assert 0

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {   
                "role": "user",
                "content": query,
            }
        ],
        model="gpt-4-turbo",
        temperature=0
    )
    raw_savedict.append(chat_completion.choices[0].message.content)
    answer = chat_completion.choices[0].message.content.split('#### caption') #### 에러처리 가능하도록 raw 파일에서 post processing
    anslst = [a for a in answer if 'information:' in a.lower()]
    
    if len(anslst)!=5:
        print("ERROR")
        # break
    
    for j, each in enumerate(anslst):
        if 'information:' not in each:
            print(each)
            continue
        
        if '#### information:' in each:
            ans = each.split('#### information:')[1]
            
        elif 'information:' not in each:
            ans = each.split('information:')[0]
            
        else:
            print(each, 'wrong format ===> PASSING')
            continue
        
        ans = ans.split('\n')
        ans = [a for a in ans if a.strip()]
        sounding_object_in_scene = manage_text(ans[0].split(':')[-1][1:] if ans[0].split(':')[-1][0]==' ' else ans[0].split(':')[-1])
        non_sounding_object_in_scene = manage_text(ans[1].split(':')[-1][1:] if ans[1].split(':')[-1][0]==' ' else ans[1].split(':')[-1]) #.strip()
        sounding_object_out_of_scene = manage_text(ans[2].split(':')[-1][1:] if ans[2].split(':')[-1][0]==' ' else ans[2].split(':')[-1]) #.strip()
        sound_in_scene = manage_text(ans[3].split(':')[-1][1:] if ans[3].split(':')[-1][0]==' ' else ans[3].split(':')[-1])  #.strip()
        sound_outside_the_scene = manage_text(ans[4].split(':')[-1][1:] if ans[4].split(':')[-1][0]==' ' else ans[4].split(':')[-1]) #.strip()
        caption = each.split(' information:')[0].split('\n')[0]
        
        tags, sdict = parse_tags(cur_iter_video_paths[j].split('/')[-1])
        
        savedict[cur_iter_video_paths[j].split('/')[-1]] = {
            'in-view sound source': sounding_object_in_scene,
            'in-view silent object': non_sounding_object_in_scene,
            'out-of-view sound source': sounding_object_out_of_scene,
            'in-view sound': sound_in_scene,
            'out-of-view sound': sound_outside_the_scene,
            'caption': caption,
            'tags': tags
        }
        
        if DEBUG:
            print('in-view sound source: ', savedict[cur_iter_video_paths[j].split('/')[-1]]['in-view sound source'])
            print('in-view silent object: ', savedict[cur_iter_video_paths[j].split('/')[-1]]['in-view silent object'])
            print('out-of-view sound source: ', savedict[cur_iter_video_paths[j].split('/')[-1]]['out-of-view sound source'])
            print('in-view sound: ', savedict[cur_iter_video_paths[j].split('/')[-1]]['in-view sound'])
            print('out-of-view sound: ', savedict[cur_iter_video_paths[j].split('/')[-1]]['out-of-view sound'])
            print('caption: ', savedict[cur_iter_video_paths[j].split('/')[-1]]['caption'])
            print('tags: ', savedict[cur_iter_video_paths[j].split('/')[-1]]['tags'])
            print()

        
    if not DEBUG:
        with open(savedict_path, 'w') as f:
            json.dump(savedict, f, indent=4)
            
        if cnt%50==0:
            with open(raw_savedict_path, 'w') as f:
                json.dump(raw_savedict, f, indent=4)
                
    if DEBUG and cnt==1:
        break

with open(savedict_path, 'w') as f:
    json.dump(savedict, f, indent=4)
    
with open(raw_savedict_path, 'w') as f:
    json.dump(raw_savedict, f, indent=4)