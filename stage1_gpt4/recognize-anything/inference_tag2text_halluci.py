'''
 * The Tag2Text Model
 * Written by Xinyu Huang
'''
import argparse
import numpy as np
import random

import torch

from PIL import Image
from ram.models import tag2text
from ram import inference_tag2text as inference
from ram import get_transform

import os
from glob import glob
import json


parser = argparse.ArgumentParser(
    description='Tag2Text inferece for tagging and captioning')
parser.add_argument('--image',
                    metavar='DIR',
                    help='path to dataset',
                    default='../../data/AVHBench_v0/frame')
parser.add_argument('--pretrained',
                    metavar='DIR',
                    help='path to pretrained model',
                    default='pretrained/tag2text_swin_14m.pth')
parser.add_argument('--image-size',
                    default=384,
                    type=int,
                    metavar='N',
                    help='input image size (default: 384)')
parser.add_argument('--thre',
                    default=0.68,
                    type=float,
                    metavar='N',
                    help='threshold value')
parser.add_argument('--specified-tags',
                    default='None',
                    help='User input specified tags')
parser.add_argument('--output',
                    default='../visual_tagging/tags.json')



if __name__ == "__main__":

    args = parser.parse_args()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    transform = get_transform(image_size=args.image_size)

    # delete some tags that may disturb captioning
    # 127: "quarter"; 2961: "back", 3351: "two"; 3265: "three"; 3338: "four"; 3355: "five"; 3359: "one"
    delete_tag_index = [127,2961, 3351, 3265, 3338, 3355, 3359]

    #######load model
    model = tag2text(pretrained=args.pretrained,
                             image_size=args.image_size,
                             vit='swin_b',
                             delete_tag_index=delete_tag_index)
    model.threshold = args.thre  # threshold for tagging
    model.eval()

    model = model.to(device)
    each_imgs = sorted(glob(os.path.join(args.image, '*')))

    print('length of all videos: ', len(each_imgs))


    savedict = {}
    
    if os.path.exists(args.output):
        with open(args.output, 'r') as f:
            savedict = json.load(f)
            
            
    for i, imgs in enumerate(each_imgs):
        print()
        print("##################")
        print('Processing video: ', imgs)
        imgs = sorted(glob(imgs + '/*.png'))
        
        print('length of all frames: ', len(imgs))
        
        if len(imgs)==0:
            continue
        
        if imgs[0].split('/')[-2] in savedict:
            print("Already processed")
            continue
        
        tags = []
        captions = []
        
        for image in imgs:
            image = transform(Image.open(image)).unsqueeze(0).to(device)

            res = inference(image, model, args.specified_tags)
            print("Model Identified Tags: ", res[0])
            print("Image Caption: ", res[2])
            print()

            
            if res==[]:
                continue
                        
            tags.append(res[0].split('|'))
            captions.append(res[2])
        
        # savedict[imgs[0].split('/')[-2]] = {
        #     'tags': tags,
        #     'captions': captions
        # }
        
        savedict[imgs[0].split('/')[-2]] = []
        for t in tags:
            savedict[imgs[0].split('/')[-2]].append(t)
        savedict[imgs[0].split('/')[-2]].append(captions)
        
        with open(args.output, 'w') as f:
            json.dump(savedict, f)
        

