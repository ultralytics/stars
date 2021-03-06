# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Count GitHub repository stars over a time period

Usage:
    $ python path/to/count_stars.py
"""

import argparse
import time
from datetime import datetime

import pandas as pd
from github import Github  # pip install PyGithub
from tqdm import tqdm


def run(
        token="ghp_YEKVmKSn1Z9...",  # GitHub access token
        days=30,  # trailing days to analyze
        save=False  # save user info
):
    # Settings
    # date = datetime(2022, 3, 1)  # count stars since this day, i.e. March 1st 2022
    # days = (datetime.now() - date).total_seconds() / 86400  # compute number of days
    # days = 30  # specify days directly, i.e. last 30 days

    repos = [
        'ultralytics/yolov5',  # YOLOv5 🚀

        'facebookresearch/detectron2',  # FAANG companies
        'deepmind/deepmind-research',
        'aws/amazon-sagemaker-examples',
        'awslabs/autogluon',
        'microsoft/lightgbm',
        'openai/gpt-3',
        'apple/turicreate',
        'apple/coremltools',
        'google/automl',
        'google-research/google-research',
        'google-research/vision_transformer',
        'google-research/bert',
        'NVlabs/stylegan3',

        'tencent/ncnn',  # Chinese companies
        'Megvii-BaseDetection/YOLOX',
        'PaddlePaddle/Paddle',

        'rwightman/pytorch-image-models',  # Startups/architectures
        'streamlit/streamlit',
        'explosion/spaCy',
        'PyTorchLightning/pytorch-lightning',
        'ray-project/ray',
        'fastai/fastai',
        'alexeyab/darknet',
        'pjreddie/darknet',
        'WongKinYiu/yolor',
        'wandb/client',
        'allegroai/clearml',
        'Deci-AI/super-gradients',
        'neuralmagic/sparseml',
        'MosaicML/composer',
        'nebuly-ai/nebullvm',
        'commaai/openpilot',
        'CorentinJ/Real-Time-Voice-Cloning',
        'iperov/DeepFaceLab',
        # 'ageitgey/face_recognition',  # known issue over 40k stars
        # edgeimpulse  # not open-source
        # octoml  # not open-source
        # 'huggingface/transformers',  # known issue over 40k stars https://github.com/PyGithub/PyGithub/issues/1876
    ]
    sleep = 1.5  # sleep time between requests

    # Parameters
    g = Github(token)  # create a Github instance
    print(f'Counting stars for last {days:.1f} days from {datetime.now():%d %B %Y}\n')
    pd.options.display.max_columns = None

    # Run
    t, users = time.time(), []
    for repo in repos:
        r = g.get_repo(repo)
        s = r.get_stargazers_with_dates().reversed
        total = s.totalCount

        dates = []
        try:
            pbar = tqdm(s, total=total, desc=r.full_name)
            for x in pbar:
                dt = (datetime.now() - x.starred_at).total_seconds() / 86400
                if dt < days:
                    dates.append([x.starred_at, 1])
                    if save:
                        time.sleep(sleep)
                        u = x.user
                        if u.email is not None:
                            users.append([r.full_name, u.name, u.company, u.email, u.location, u.html_url, u.followers,
                                          x.starred_at])
                else:
                    n = len(dates)
                    s1 = f'{n} stars'
                    s2 = f'({n / days:.1f}/day)'
                    pbar.desc = f'{r.full_name:40s}{s1:12s}{s2:12s}'
                    break

        except Exception as e:
            print(e)

        df = pd.DataFrame(dates, columns=['date', 'stars'])
        df.date = pd.to_datetime(df.date)
        # df.to_csv(f'dates_{r.name}.csv')
        # dg = df.groupby(pd.Grouper(key='date', freq='1M')).sum()  # group by month
        # dg = df.groupby(pd.Grouper(key='date', freq='1D')).sum()  # group by day

    print(f'Done in {time.time() - t:.1f}s')
    if save:
        x = pd.DataFrame(users, columns=['Repo', 'Name', 'Company', 'Email', 'Location', 'GitHub', 'Followers', 'Date'])
        x.to_csv('users.csv')
        print(f'{len(x)} users saved to users.csv')


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', type=str, default='ghp_YEKVmKSn1Z9...', help='GitHub access token')
    parser.add_argument('--days', type=int, default=30, help='Trailing days to analyze')
    parser.add_argument('--save', action='store_true', help='Save user info')
    return parser.parse_args()


def main(opt):
    run(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
