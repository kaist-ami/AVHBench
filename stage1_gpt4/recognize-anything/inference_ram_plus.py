'''
 * The Recognize Anything Plus Model (RAM++)
 * Written by Xinyu Huang
'''
import argparse
import numpy as np
import random

import torch

from PIL import Image
from ram.models import ram_plus
from ram import inference_ram as inference
from ram import get_transform

from glob import glob
import os
import json


parser = argparse.ArgumentParser(
    description='Tag2Text inferece for tagging and captioning')
parser.add_argument('--image',
                    metavar='DIR',
                    help='path to dataset',
                    default='/data/mok/audiocaps_code/audiocaps_frames_08fps')
parser.add_argument('--pretrained',
                    metavar='DIR',
                    help='path to pretrained model',
                    default='pretrained/ram_plus_swin_large_14m.pth')
parser.add_argument('--image-size',
                    default=384,
                    type=int,
                    metavar='N',
                    help='input image size (default: 448)')
parser.add_argument('--output',
                    default='/data/mok/audiocaps_code/audiocaps_frames_08fps/tags.json')


if __name__ == "__main__":

    args = parser.parse_args()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    transform = get_transform(image_size=args.image_size)

    #######load model
    model = ram_plus(pretrained=args.pretrained,
                             image_size=args.image_size,
                             vit='swin_l')
    model.eval()

    model = model.to(device)

    # image = transform(Image.open(args.image)).unsqueeze(0).to(device)

    # res = inference(image, model)
    # print("Image Tags: ", res[0])
    # print("图像标签: ", res[1])
    
    
    # each_imgs = sorted(glob('/data/mok/audiocaps/frames_1fps/*'))
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
        # imgs = sorted(glob('/node_data/mok/module/recognize-anything/datasets/testvid/*.png'))
        
        if len(imgs)==0:
            continue
        
        if imgs[0].split('/')[-2] in savedict:
            print("Already processed")
            continue
        
        tags = []
        
        for image in imgs:
            image = transform(Image.open(image)).unsqueeze(0).to(device)

            res = inference(image, model)[0]
            print("Image Tags: ", res)
            
            if res==[]:
                continue
            
            tmp_tags = res.split('|')
            
            tags.append(tmp_tags)
        
        savedict[imgs[0].split('/')[-2]] = tags
        
        with open(args.output, 'w') as f:
            json.dump(savedict, f)
        
