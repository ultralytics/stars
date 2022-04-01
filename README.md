# Count GitHub Stars per Day ⭐

This tool helps track 

### Requirements

`PyGitHub` is required to access the [GitHub REST API] via Python. This library enables you to manage [GitHub] resources such as repositories, user profiles, and organizations in your Python applications.

[GitHub REST API]: https://docs.github.com/en/rest
[GitHub]: https://github.com

```bash
pip install PyGithub
```

### Usage

Update `TOKEN` to a valid [GitHub access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) in `count_stars.py` L15 and then run:

```python
python count_stars.py
```

### Result

When run on March 31st, 2022 result is:

```python
Counting stars for last 30.8 days

ultralytics/yolov5                      1636 stars  (52.0/day)  :   7%|▋         | 1636/24118 [00:16<03:52, 96.58it/s]
facebookresearch/detectron2             400 stars   (12.7/day)  :   2%|▏         | 400/20363 [00:03<02:53, 114.75it/s]
deepmind/deepmind-research              209 stars   (6.6/day)   :   2%|▏         | 209/9924 [00:01<01:21, 119.41it/s]
aws/amazon-sagemaker-examples           138 stars   (4.4/day)   :   2%|▏         | 138/6723 [00:01<01:00, 108.33it/s]
awslabs/autogluon                       153 stars   (4.9/day)   :   4%|▎         | 153/4311 [00:01<00:35, 117.60it/s]
microsoft/LightGBM                      129 stars   (4.1/day)   :   1%|          | 129/13611 [00:01<02:17, 98.37it/s]
openai/gpt-3                            70 stars    (2.2/day)   :   1%|          | 70/11140 [00:00<02:21, 78.15it/s]
apple/turicreate                        57 stars    (1.8/day)   :   1%|          | 57/10648 [00:00<01:30, 116.69it/s]
apple/coremltools                       42 stars    (1.3/day)   :   2%|▏         | 42/2608 [00:00<00:29, 88.18it/s]
Tencent/ncnn                            300 stars   (9.5/day)   :   2%|▏         | 300/14175 [00:02<01:49, 126.88it/s]
Megvii-BaseDetection/YOLOX              285 stars   (9.1/day)   :   5%|▍         | 285/6021 [00:02<00:42, 133.68it/s]
PaddlePaddle/Paddle                     216 stars   (6.9/day)   :   1%|          | 216/17874 [00:01<02:26, 120.36it/s]
rwightman/pytorch-image-models          759 stars   (24.1/day)  :   4%|▍         | 759/17404 [00:05<02:11, 126.54it/s]
streamlit/streamlit                     673 stars   (21.4/day)  :   4%|▎         | 673/18486 [00:05<02:36, 113.52it/s]
explosion/spaCy                         556 stars   (17.7/day)  :   2%|▏         | 556/23048 [00:04<03:19, 112.54it/s]
PyTorchLightning/pytorch-lightning      432 stars   (13.7/day)  :   2%|▏         | 432/17868 [00:03<02:17, 126.56it/s]
ray-project/ray                         418 stars   (13.3/day)  :   2%|▏         | 418/19706 [00:03<02:42, 118.41it/s]
fastai/fastai                           160 stars   (5.1/day)   :   1%|          | 160/22108 [00:01<03:37, 100.89it/s]
google/automl                           45 stars    (1.4/day)   :   1%|          | 45/4941 [00:00<00:45, 106.84it/s]
AlexeyAB/darknet                        288 stars   (9.2/day)   :   2%|▏         | 288/18777 [00:02<02:24, 128.33it/s]
pjreddie/darknet                        283 stars   (9.0/day)   :   1%|▏         | 283/22486 [00:02<02:56, 125.59it/s]
WongKinYiu/yolor                        80 stars    (2.5/day)   :   5%|▌         | 80/1472 [00:00<00:14, 99.01it/s]
wandb/client                            72 stars    (2.3/day)   :   2%|▏         | 72/3791 [00:00<00:43, 86.35it/s]
Deci-AI/super-gradients                 19 stars    (0.6/day)   :   6%|▌         | 19/312 [00:00<00:06, 47.65it/s]
```
