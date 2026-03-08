import os
import copy
import json
import random
import pathlib
import pandas as pd
from PIL import Image
from typing import Dict, Optional, Sequence

import decord
from decord import VideoReader

import torch

import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, LlamaTokenizer

from video_llama.processors import transforms_video, AlproVideoTrainProcessor
from video_llama.conversation.conversation_video import Conversation,SeparatorStyle
from video_llama.datasets.datasets.base_dataset import BaseDataset
from video_llama.processors.video_processor import ToTHWC,ToUint8,load_video
from video_llama.models.ImageBind.data import load_and_transform_audio_data
import sys
import pdb

# class ForkedPdb(pdb.Pdb):
#     """A Pdb subclass that may be used
#     from a forked multiprocessing child

#     """
#     def interaction(self, args, **kwargs):
#         _stdin = sys.stdin
#         try:
#             sys.stdin = open('/dev/stdin')
#             pdb.Pdb.interaction(self,args, **kwargs)
#         finally:
#             sys.stdin = _stdin

# 要让模型同时支持audio, video, text三部分输入信息才行
class Halluci_Reasoning_Dataset(BaseDataset):
    def __init__(self, vis_processor, text_processor, vis_root, ann_path, 
                 max_length=1024,
                 num_audio_query_token=8, 
                 num_video_query_token=32, 
                 tokenizer_name='/mnt/workspace/ckpt/vicuna-13b/'):
        
        
        # self.annotation = []
        # df = pd.read_csv(ann_path)
        # for _, row in df.iterrows():
        #     name = row['names']
        #     subtitle = row['subtitles']
        #     reason   = row['reasons']
        #     if pd.isna(subtitle): subtitle=""
        #     self.annotation.append({'name': name, 'subtitle': subtitle, 'reason': reason})
        
        with open(ann_path, "r") as f:
            self.annotation = json.load(f) # list of dict

        # use base model initialize approach
        super().__init__(vis_processor=vis_processor, 
                         text_processor=text_processor,
                         vis_root=vis_root,
                         ann_path=ann_path,
                         max_length=max_length,
                         num_audio_query_token=num_audio_query_token,
                         num_video_query_token=num_video_query_token,
                         tokenizer_name=tokenizer_name)
        
        
    # def _get_video_path(self, sample):
    #     full_video_fp = os.path.join(self.vis_root, sample['name'] + '.avi')
    #     return full_video_fp

    def _get_video_path(self, sample):
        # rel_video_fp = sample['video']
        rel_video_fp = sample['video_id']
        full_video_fp = os.path.join(self.vis_root, rel_video_fp + ".mp4")
        return full_video_fp

    def __getitem__(self, index):
        num_retries = 10 # skip error or too long videos
        for _ in range(num_retries):
            try:
                sample = self.annotation[index]
                # step1: read video and audio feats
                video_path = self._get_video_path(sample)


                video, msg = load_video(
                    video_path=video_path,
                    n_frms = 8,
                    height = 224,
                    width  = 224,
                    sampling ="uniform",
                    return_msg = True
                )
                video = self.vis_processor.transform(video) # [3, 8, 224, 224]
                audio = load_and_transform_audio_data([video_path], "cpu", clips_per_video=8)[0] # [8, 1, 128, 204]

                # question = sample['question']
                question = sample['text']


#                 user_message = f""" \
# Reasoning task: you are to answer why the person laughed given the video clip. \
# The person laughing moment is mostly at the end of the clip. \
# Explain why the person laughed given the video clip, at most 30 words, starting with 'The person laughed because ‘ Given video clip: {textrep}.\
# """

                # user_message = question + " Answer Yes or No."
                user_message = question

                captioning_user_message = question


                task = sample['task']

                if task == 'Audio Hallucination':
                    prompt = f"###Human: <Audio><AudioHere></Audio>. {user_message} ###Assistant:"
                    print("task: ", task)
                    print("prompt: ", prompt)
                    # print("answer: ", sample['answer'])
                    print("answer: ", sample['label'])

                elif task == 'Video Hallucination':
                    prompt = f"###Human: <Video><ImageHere></Video>. {user_message} ###Assistant:"
                    print("task: ", task)
                    print("prompt: ", prompt)
                    # print("answer: ", sample['answer'])
                    print("answer: ", sample['label'])


                elif task == "AV Hallucination (Audio)" or task == "AV Hallucination (Video)" or task == "AV Matching":
                    prompt = f"###Human: <Video><ImageHere></Video>. <Audio><AudioHere></Audio> {user_message} ###Assistant:"
                    print("task: ", task)
                    print("prompt: ", prompt)
                    # print("answer: ", sample['answer'])
                    print("answer: ", sample['label'])

                elif task == "AV Captioning" or task == "AV Reasoning" or task == "Object Listing":
                    prompt = f"###Human: <Video><ImageHere></Video>. <Audio><AudioHere></Audio> {captioning_user_message} ###Assistant:"
                    print("task: ", task)
                    print("prompt: ", prompt)
                    # print("answer: ", sample['answer'])
                    print("answer: ", sample['label'])

                # conversation_list = copy.deepcopy(sample['QA'])

                # # step2: generate (text_input, label)
                # subtitle = sample['subtitle']
                # # user_message = "From what clues can we infer the person's emotional state?"
                # prompt =   f"###Human: Close your eyes, open your ears and you imagine only based on the sound that <Audio><AudioHere></Audio>. " \
                #          + f"Close your ears, open your eyes and you see that <Video><ImageHere></Video>. "  \
                #          + f"The subtitle of this video is <Subtitle>{subtitle}</Subtitle>. " \
                #          + f"Now answer my question based on what you have seen, heard, and provided subtitle. {user_message} ###Assistant: "
                
                ## replace DEFAULT_IMAGE_PATCH_TOKEN and DEFAULT_AUDIO_PATCH_TOKEN => for convinence to get attention vectors
                replace_token = self.DEFAULT_IMAGE_PATCH_TOKEN * self.num_video_query_token
                prompt = prompt.replace(self.DEFAULT_IMAGE_PATCH_TOKEN, replace_token)
                replace_token = self.DEFAULT_AUDIO_PATCH_TOKEN * self.num_audio_query_token
                prompt = prompt.replace(self.DEFAULT_AUDIO_PATCH_TOKEN, replace_token)

                ## tokenizer
                prompt_id = self.to_token_ids(prompt, self.max_length)
                
                # reason = sample['reason'] + '###'
                # target_id = self.to_token_ids(reason, self.max_length)

                # answer = sample['answer'] + '###'
                answer = sample['label'] + '###'

                target_id = self.to_token_ids(answer, self.max_length)

                text_input = torch.cat([prompt_id, target_id])
                label    = torch.cat([torch.ones([len(prompt_id)], dtype=text_input.dtype) * -100, target_id])
                assert len(text_input) == len(label)
                if len(text_input) > self.max_length:
                    raise RuntimeError("too long text_input")
            except Exception as e:
                print(f"Failed to load or too long inputs: {video_path}. ", e,
                      f"Will randomly sample an example as a replacement.")
                index = random.randint(0, len(self) - 1)
                continue
            break
        else:  
            raise RuntimeError(f"Failed to fetch video after {num_retries} retries.")
        return {
            "image": video, # [c=3, frame=8, 224, 224]
            "audio": audio, # [frame=8, c=1, 128, 204]
            "label": label,
            "text_input": text_input,
            'dataset': 'emotion_video',
        }
    