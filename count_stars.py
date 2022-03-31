# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Count GitHub repository stars over a time period

Usage:
    $ python path/to/count_stars.py
"""

import datetime

from github import Github  # pip install PyGithub
from tqdm import tqdm

# Settings
TOKEN = "ghp_YEKVmKSn1Z9..."  # GitHub access token
date = datetime.datetime(2022, 3, 1)  # count stars since this day
repos = [
    'ultralytics/yolov5',
    'facebookresearch/detectron2',
    'PyTorchLightning/pytorch-lightning',
    'streamlit/streamlit',
    'ray-project/ray',
    'PaddlePaddle/Paddle',
    'tencent/ncnn',
    'microsoft/lightgbm',
    'openai/gpt-3',
    'google/automl',
    'deepmind/deepmind-research',
    'awslabs/autogluon',
    'aws/amazon-sagemaker-examples',
    'apple/turicreate',
    'apple/coremltools',
    'pjreddie/darknet',
    'alexeyab/darknet',
    'explosion/spaCy',
    'Megvii-BaseDetection/YOLOX',
    'WongKinYiu/yolor',
    'rwightman/pytorch-image-models',
    'wandb/client',
    'fastai/fastai',
    'Deci-AI/super-gradients',
    # 'huggingface/transformers',  # known issue over 40k stars https://github.com/PyGithub/PyGithub/issues/1876
]

# Parameters
g = Github(TOKEN)  # create a Github instance
now = datetime.datetime.now()
days = (now - date).days + (now - date).seconds / 86400  # days since date
print(f'Counting stars for last {days:.1f} days\n')

# Run
for repo in repos:
    r = g.get_repo(repo)
    s = r.get_stargazers_with_dates().reversed
    total = s.totalCount

    try:
        n = 0
        pbar = tqdm(s, total=total, desc=r.full_name)
        for x in pbar:
            if x.starred_at > date:
                n += 1
            else:
                s1 = f'{n} stars'
                s2 = f'({n / days:.1f}/day)'
                pbar.desc = f'{r.full_name:40s}{s1:12s}{s2:12s}'
                break
    except Exception as e:
        print(e)

    # Threaded
    # from multiprocessing.pool import Pool, ThreadPool
    # fcn = lambda x: x.starred_at > date
    # results = ThreadPool(8).imap(fcn, s)
    # pbar = tqdm(enumerate(results), total=total)
    # n = 0
    # for i, x in pbar:
    #     n += x  # im, hw_orig, hw_resized = load_image(self, i)
    #     pbar.desc = f'{n}/{i}'
