# AVHBench
This repository contains dataset for the NeurIPS 2024 Submission, \
[AVHBench: A Cross-Modal Hallucination Evluation for Audio-Visual Large Language Models].


## Download the AVHBench Dataset
1. Download AVHBench dataset in [here](https://drive.google.com/file/d/15KjSeYn3tjiHXiswLgffmxPEoMYtepv2/view?usp=sharing)
2. unzip the dataset.

    ```
    |
    |
    └── Train
    |     ├── videos
    |     ├── audios
    |     └── qa_train.json   
    |           
    └── Test
         ├── videos
         ├── audios
         └── qa_test.json  
             
    
    ``` 
3. Details about each file
   - Train: Train data split
   - Test: Test data split
   - videos: silent videos
   - audios: audios extracted from the videos
   - qa_train.json: question and answer pairs for each video in train data split.
   - qa_test.json: question and answer pairs for each video in test data split.
     


## Acknowledgement
We are grateful for the following awesome projects, our AVHBench arising from:
- [GPT4](https://arxiv.org/abs/2303.08774): Language Models are Few-Shot Learners
- [Recognize Anything Model](https://github.com/xinyu1205/recognize-anything): Visual Tagging Models for Dataset Construction Pipeline
- [VALOR](https://github.com/TXH-mercury/VALOR): VALOR: Vision-Audio-Language Omni-Perception Pretraining Model and Dataset
- [AudioCaps](https://audiocaps.github.io/): AudioCaps: Generating Captions for Audios in the Wild

