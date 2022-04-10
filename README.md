# Count GitHub Stars per Day ⭐

Track GitHub stars per day over a date range to measure the open-source popularity of different repositories.

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

When run on April 10th, 2022 result is:

```python
Counting stars for last 30.0 days from 10 April 2022

ultralytics/yolov5                      1572 stars  (52.4/day)  :   6%|▋         | 1572/24560 [00:11<02:51, 133.78it/s]
facebookresearch/detectron2             371 stars   (12.4/day)  :   2%|▏         | 371/20463 [00:03<02:57, 112.90it/s]
deepmind/deepmind-research              187 stars   (6.2/day)   :   2%|▏         | 187/9976 [00:01<01:19, 123.89it/s]
aws/amazon-sagemaker-examples           124 stars   (4.1/day)   :   2%|▏         | 124/6756 [00:01<00:55, 119.95it/s]
awslabs/autogluon                       157 stars   (5.2/day)   :   4%|▎         | 157/4355 [00:01<00:38, 108.15it/s]
microsoft/LightGBM                      120 stars   (4.0/day)   :   1%|          | 120/13648 [00:01<02:16, 99.24it/s]
openai/gpt-3                            81 stars    (2.7/day)   :   1%|          | 81/11163 [00:00<01:53, 97.37it/s]
apple/turicreate                        57 stars    (1.9/day)   :   1%|          | 57/10658 [00:00<01:59, 88.64it/s]
apple/coremltools                       34 stars    (1.1/day)   :   1%|▏         | 34/2613 [00:00<00:45, 56.13it/s]
google/automl                           50 stars    (1.7/day)   :   1%|          | 50/4954 [00:00<00:59, 81.86it/s]
google-research/google-research         505 stars   (16.8/day)  :   2%|▏         | 505/22697 [00:03<02:55, 126.45it/s]
google-research/vision_transformer      195 stars   (6.5/day)   :   4%|▍         | 195/4835 [00:01<00:39, 116.84it/s]
google-research/bert                    316 stars   (10.5/day)  :   1%|          | 316/30898 [00:02<04:04, 124.86it/s]
NVlabs/stylegan3                        153 stars   (5.1/day)   :   4%|▍         | 153/3934 [00:01<00:29, 128.11it/s]
Tencent/ncnn                            257 stars   (8.6/day)   :   2%|▏         | 257/14229 [00:02<01:52, 123.86it/s]
Megvii-BaseDetection/YOLOX              266 stars   (8.9/day)   :   4%|▍         | 266/6097 [00:02<00:44, 131.35it/s]
PaddlePaddle/Paddle                     179 stars   (6.0/day)   :   1%|          | 179/17919 [00:01<02:24, 122.79it/s]
rwightman/pytorch-image-models          734 stars   (24.5/day)  :   4%|▍         | 734/17605 [00:05<02:08, 131.68it/s]
streamlit/streamlit                     371 stars   (12.4/day)  :   2%|▏         | 371/18559 [00:02<02:16, 132.76it/s]
explosion/spaCy                         272 stars   (9.1/day)   :   1%|          | 272/23108 [00:02<03:09, 120.73it/s]
PyTorchLightning/pytorch-lightning      382 stars   (12.7/day)  :   2%|▏         | 382/17959 [00:03<02:28, 118.25it/s]
ray-project/ray                         439 stars   (14.6/day)  :   2%|▏         | 439/19867 [00:03<02:52, 112.74it/s]
fastai/fastai                           127 stars   (4.2/day)   :   1%|          | 127/22114 [00:01<03:55, 93.44it/s]
AlexeyAB/darknet                        270 stars   (9.0/day)   :   1%|▏         | 270/18849 [00:02<02:29, 124.08it/s]
pjreddie/darknet                        183 stars   (6.1/day)   :   1%|          | 183/22526 [00:01<03:08, 118.50it/s]
WongKinYiu/yolor                        70 stars    (2.3/day)   :   5%|▍         | 70/1493 [00:00<00:11, 123.44it/s]
wandb/client                            65 stars    (2.2/day)   :   2%|▏         | 65/3808 [00:00<00:34, 108.04it/s]
Deci-AI/super-gradients                 25 stars    (0.8/day)   :   8%|▊         | 25/322 [00:00<00:04, 63.49it/s]
neuralmagic/sparseml                    33 stars    (1.1/day)   :   4%|▍         | 33/850 [00:00<00:09, 85.61it/s]
Done in 80.8s
```
