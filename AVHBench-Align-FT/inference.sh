# CUDA_VISIBLE_DEVICES=7 python3 inference_halluci.py --gpu-id=0 --cfg-path="/home/hboh/neurips24/AffectGPT/AffectGPT/train_configs/inference.yaml" \
# 					--ckpt_root='/node_data/hboh/neurips24/affectgpt/output_ckpt/20240526174134_100_1000_1000' \
# 					--test_epochs='8-8' \
# 					--output_pth='/home/hboh/neurips24/AffectGPT/AffectGPT/output/qa_2000_result.json' \
# 					--label_path='/node_data/hboh/neurips24/0525_sanity_test/qa_affectgpt.json'

CUDA_VISIBLE_DEVICES=1 python3 inference_halluci.py --gpu-id=0 --cfg-path="/home/hboh/neurips24/AffectGPT/AffectGPT/train_configs/inference.yaml" \
					--ckpt_root='/node_data/hboh/neurips24/affectgpt/output_ckpt/20240528112455_100_400_400' \
					--test_epochs='1-1' \
					--output_pth='/home/hboh/neurips24/AffectGPT/AffectGPT/output/qa_2000_result_20240528112455_100_400_400.json' \
					--label_path='/node_data/hboh/neurips24/0525_sanity_test/qa.json'