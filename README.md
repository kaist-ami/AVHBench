# AVHBench: A Cross-Modal Hallucination Benchmark for Audio-Visual Large Language Models (ICLR 2025)
Authors: [Kim Sung-Bin*](https://sites.google.com/view/kimsungbin), [Oh Hyun-Bin*](https://hyunbin70.github.io/), [JungMok Lee](https://ami.postech.ac.kr/d81b1c7c-7c84-4904-808e-097513816ae1/),
[Arda Senocak](https://ardasnck.github.io), [Joon Son Chung](https://mm.kaist.ac.kr/joon/), [Tae-Hyun Oh](https://ami.postech.ac.kr/members/tae-hyun-oh)
<br>
(* denotes equal contribution.)

### [Project Page](https://avhbench.github.io/) | [Github](https://github.com/postech-ami/AVHBench) | [Paper](https://arxiv.org/pdf/2410.18325) 

<img width="1888" alt="Image" src="https://github.com/user-attachments/assets/a9c48347-954a-4cd9-b499-2dcd3c27f61c" />

This repository contains the official dataset for the ICLR 2025 paper, ["AVHBench: A Cross-Modal Hallucination Evluation for Audio-Visual Large Language Models"](https://arxiv.org/pdf/2410.18325).
We introduce AVHBench, the first comprehensive benchmark specifically designed to evaluate the perception and comprehension capabilities of audio-visual LLMs.

<br>

> **Abstract:** *Following the success of Large Language Models (LLMs), expanding their boundaries to new modalities represents a significant paradigm shift in multimodal understanding. Human perception is inherently multimodal, relying not only on text but also on auditory and visual cues for a complete understanding of the world. In recognition of this fact, audio-visual LLMs have recently emerged. Despite promising developments, the lack of dedicated benchmarks poses challenges for understanding and evaluating models. In this work, we show that audio-visual LLMs struggle to discern subtle relationships between audio and visual signals, leading to hallucinations, underscoring the need for reliable benchmarks. To address this, we introduce AVHBench, the first comprehensive benchmark specifically designed to evaluate the perception and comprehension capabilities of audio-visual LLMs. Our benchmark includes tests for assessing hallucinations, as well as the crossmodal matching and reasoning abilities of these models. Our results reveal that most existing audio-visual LLMs struggle with hallucinations caused by crossinteractions between modalities, due to their limited capacity to perceive complex multimodal signals and their relationships. Additionally, we demonstrate that simple training with our AVHBench improves robustness of audio-visual LLMs against hallucinations.*

## Leaderboard

### Audio-driven Video Hallucination

 |Rank        |    Model            | Acc. (↑)                        | Precision (↑)    | Recall (↑)       | F1 (↑)           | Yes (%)          | 
 |:----------:|---------------------|---------------------------------|------------------|------------------|------------------|------------------|
 |🥇**1st**   | AVHModel-Align-FT   | 83.9                            | -                |  -               | -                | -             |
 |🥈**2nd**   | Gemini-Flash        | 83.3                            | 85.7             | 81.0             | 83.7             | 47.3             | 
 |🥉**3rd**   | Video-SALMONN       | 78.1                            | 74.9             | 84.5             | 79.4             | 56.4             | 
 |4th         | Video-LLaMA2        | 75.2                            | 73.6             | 78.7             | 76.1             | 53.6             |
 |5th         | PandaGPT            | 58.5                            | 55.3             | 91.1             | 68.8             | 82.3             |
 |6th         | OneLLM              | 53.7                            | 58.6             | 64.8             | 49.8             | 63.1             |
 |7th         | ChatBridge          | 52.9                            | 70.9             | 52.9             | 48.9             | 77.6             |
 |8th         | ImageBind-LLM       | 50.3                            | 50.2             | 87.1             | 63.7             | 86.7             |
 |9th         | Video-LLaMA         | 50.1                            | 50.1             | 100              | 66.7             | 99.9             |
 |10th        | X-InstrcutBLIP      | 18.1                            | 16.0             | 15.0             | 15.5             | 46.9             |


### Video-driven Audio Hallucination

|Rank        |    Model            | Acc. (↑)                        | Precision (↑)    | Recall (↑)       | F1 (↑)           | Yes (%)          | 
|:----------:|---------------------|---------------------------------|------------------|------------------|------------------|------------------|
|🥇**1st**   | AVHModel-Align-FT   | 77.3                            | -                | -                | -                | -             |
|🥈**2nd**   | Video-LLaMA2        | 74.2                            | 69.4             | 86.6             | 77.0             | 62.4             |
|🥉**3rd**   | Video-SALMONN       | 65.2                            | 62.3             | 76.9             | 68.8             | 61.7             | 
|4th         | Gemini-Flash        | 63.0                            | 57.9             | 94.7             | 71.9             | 81.7             | 
|5th         | PandaGPT            | 61.3                            | 57.4             | 86.6             | 69.1             | 75.5             |
|6th         | Video-LLaMA         | 50.2                            | 50.2             | 100              | 66.9             | 100              |
|7th         | ImageBind-LLM       | 50.0                            | 50.0             | 99.3             | 66.5             | 99.3             |
|8th         | OneLLM              | 44.3                            | 50.2             | 39.4             | 49.8             | 55.0             |
|9th         | ChatBridge          | 32.8                            | 60.0             | 32.8             | 39.8             | 14.8             |
|10th       | X-InstrcutBLIP      | 16.3                            | 14.5             | 38.5             | 21.1             | 77.0             |

- **Ranked by Accuracy**
- **AVHModel-Align-FT** refers to our final model presented in the fourth row of Table 4 in the main paper.
- **Last update**:  April 4th, 2025

## Download the AVHBench Dataset
At this time, we provide a subset of AVHBench, which includes both real and synthetic (swapped) video samples.

1. Download AVHBench dataset ([videos](https://drive.google.com/file/d/10-Qp8zxA3ITT-ileEnCgJkf5Nzx1wry7/view?usp=sharing)|[QA](https://drive.google.com/file/d/1KcYDAv9lLy3hsx5rWdfRqMFV2NYcZ94W/view?usp=sharing)) 
2. Details of each file in the dataset
   - **{video_id}.mp4**: a real video sample sourced from VALOR and Audiocaps.
   - **{QA}.json**: All the question-and-answer pairs for the video, which contain the metadata of: (1) video id, (2) type of hallucination task, (3) input text prompt, and (4) ground-truth label. We provide an example of the json file below:
     
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

## Citation
If you use AVHBench in a research paper, please cite our work as follows:
````BibTeX
@article{sung2024avhbench,
  title={AVHBench: A Cross-Modal Hallucination Benchmark for Audio-Visual Large Language Models},
  author={Sung-Bin, Kim and Hyun-Bin, Oh and Lee, JungMok and Senocak, Arda and Chung, Joon Son and Oh, Tae-Hyun},
  journal={arXiv preprint arXiv:2410.18325},
  year={2024}
}
````


## Acknowledgement
We are grateful for the following awesome projects, our AVHBench arising from:
- [GPT4](https://arxiv.org/abs/2303.08774): Language Models are Few-Shot Learners
- [Recognize Anything Model](https://github.com/xinyu1205/recognize-anything): Visual Tagging Models for Dataset Construction Pipeline
- [VALOR](https://github.com/TXH-mercury/VALOR): VALOR: Vision-Audio-Language Omni-Perception Pretraining Model and Dataset
- [AudioCaps](https://audiocaps.github.io/): AudioCaps: Generating Captions for Audios in the Wild

