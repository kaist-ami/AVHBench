
## Requirements.
1. first set recognize-anything.
- make the conda environment 'recognize_anything'.
- please download tag2text_swin_14m.pth and put the path on preprocess.sh

2. Create the 'avhbench' conda environment.
```bash
conda create -n avhbench python=3.11 -y
conda activate avhbench
pip install -r requirements.txt
```

## Stage 1 - disentanglement
Please locate your openai key to disentangle_gpt4.py, and run preprocess.sh.
```bash 
./preprocess.sh
```