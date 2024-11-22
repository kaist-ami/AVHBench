# AVHBench
This repository contains dataset for the ICLR 2025 Submission, \
[AVHBench: A Cross-Modal Hallucination Evluation for Audio-Visual Large Language Models].

<img width="1450" alt="0_teaser_iclr" src="https://github.com/user-attachments/assets/4236aed7-8d6d-4a57-9421-5eb310cf499d">

# Leaderboard

### Audio-driven Video Hallucination

|    Model            | Acc. (↑)                        | Precision (↑)    | Recall (↑)       | F1 (↑)           | Yes (%)          | 
|---------------------|---------------------------------|------------------|------------------|------------------|------------------|
| Gemini-Flash        | 83.3                            | 85.7             | 81.0             | 83.7             | 47.3             | 
| Video-SALMONN       | 78.1                            | 74.9             | 84.5             | 79.4             | 56.4             | 
| Video-LLaMA2        | 75.2                            | 73.6             | 78.7             | 76.1             | 53.6             |
| PandaGPT            | 58.5                            | 55.3             | 91.1             | 68.8             | 82.3             |
| OneLLM              | 53.7                            | 58.6             | 64.8             | 49.8             | 63.1             |
| ChatBridge          | 52.9                            | 70.9             | 52.9             | 48.9             | 77.6             |
| ImageBind-LLM       | 50.3                            | 50.2             | 87.1             | 63.7             | 86.7             |
| Video-LLaMA         | 50.1                            | 50.1             | 100              | 66.7             | 99.9             |
| X-InstrcutBLIP      | 18.1                            | 16.0             | 15.0             | 15.5             | 46.9             |


### Video-driven Audio Hallucination

|    Model            | Acc. (↑)                        | Precision (↑)    | Recall (↑)       | F1 (↑)           | Yes (%)          | 
|---------------------|---------------------------------|------------------|------------------|------------------|------------------|
| Video-LLaMA2        | 74.2                            | 69.4             | 86.6             | 77.0             | 62.4             |
| Video-SALMONN       | 65.2                            | 62.3             | 76.9             | 68.8             | 61.7             | 
| Gemini-Flash        | 63.0                            | 57.9             | 94.7             | 71.9             | 81.7             | 
| PandaGPT            | 61.3                            | 57.4             | 86.6             | 69.1             | 75.5             |
| Video-LLaMA         | 50.2                            | 50.2             | 100              | 66.9             | 100              |
| ImageBind-LLM       | 50.0                            | 50.0             | 99.3             | 66.5             | 99.3             |
| OneLLM              | 44.3                            | 50.2             | 39.4             | 49.8             | 55.0             |
| ChatBridge          | 32.8                            | 60.0             | 32.8             | 39.8             | 14.8             |
| X-InstrcutBLIP      | 16.3                            | 14.5             | 38.5             | 21.1             | 77.0             |


## Download the AVHBench Dataset
At this time, we provide a subset of AVHBench, which includes both real and synthetic (swapped) video samples.

1. Download AVHBench dataset v.0 in [here](https://drive.google.com/file/d/1bLHjdlk0G51RfIztXPNmWkqd3nvy7KLT/view?usp=sharing)
2. Unzip the dataset.

    ```
    AVHBench_v0
        |
        |
        └── json
        |     ├── 00006.json
        |     ├── 00159.json
        |     └── ...   
        |           
        └── video
             ├── 00006.mp4
             ├── 00006_swap.mp4
             └── 00159.mp4
             └── 00159_swap.mp4
             └── ...
    ```
3. Details of each file in the dataset
   - **{video_id}.json**: Question-and-Answer pairs for the video, which contain the metadata of: (1) video id, (2) type of hallucination task, (3) input text prompt, and (4) ground-truth label. We provide an axample of json file below:
     
       ```
      [
          {
            "video_id": "00191",
            "task": "Video-driven Audio Hallucination",
            "text": "Is the sleeping man making sound in the audio?",
            "label": "Yes"
          },
          {
            "video_id": "00191",
            "task": "Video-driven Audio Hallucination",
            "text": "Is the couch making sound in the audio?",
            "label": "No"
          },
          {
            "video_id": "00191",
            "task": "Audio-driven Video Hallucination",
            "text": "Is the sleeping man visible in the video?",
            "label": "Yes"
          },
          {
            "video_id": "00191",
            "task": "Audio-driven Video Hallucination",
            "text": "Is the person walking visible in the video?",
            "label": "No"
          },
          {
            "video_id": "00191",
            "task": "AV Matching",
            "text": "Are the contexts of audio and visual content matching?",
            "label": "Yes"
          },
          {
            "video_id": "00191",
            "task": "AV Captioning",
            "text": "Describe what you see and hear in a single sentence.",
            "label": "A young man with no shirt on is laying in bed, with footsteps walking on a hard surface followed by a person snoring."
          }
      ]
       ```
   - **{video_id}.mp4**: a real video sample sourced from VALOR and Audiocaps.
   - **{video_id}_swap.mp4**: a synthetic video sample generated by swapping the audio in the real video with another audio.


## Acknowledgement
We are grateful for the following awesome projects, our AVHBench arising from:
- [GPT4](https://arxiv.org/abs/2303.08774): Language Models are Few-Shot Learners
- [Recognize Anything Model](https://github.com/xinyu1205/recognize-anything): Visual Tagging Models for Dataset Construction Pipeline
- [VALOR](https://github.com/TXH-mercury/VALOR): VALOR: Vision-Audio-Language Omni-Perception Pretraining Model and Dataset
- [AudioCaps](https://audiocaps.github.io/): AudioCaps: Generating Captions for Audios in the Wild

