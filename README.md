# Count GitHub Stars ⭐

### Requirements

`PyGitHub` is required to access the [GitHub REST API] via Python. This library enables you to manage [GitHub] resources such as repositories, user profiles, and organizations in your Python applications.

[GitHub REST API]: https://docs.github.com/en/rest
[GitHub]: https://github.com

```bash
pip install PyGithub
```

### Usage

Update `TOKEN` to a valid GitHub access token in `count_stars.py` L15 and then run:

```python
python count_stars.py
```

### Result

When run on March 31st, 2022 result is:

```python
Counting stars for last 30.8 days

ultralytics/yolov5                      : 1602 stars (52.0/day):   7%|▋         | 1602/24084 [00:12<02:58, 126.09it/s]
PyTorchLightning/pytorch-lightning      : 414 stars (13.4/day):   2%|▏         | 414/17853 [00:03<02:20, 124.19it/s]
facebookresearch/detectron2             : 385 stars (12.5/day):   2%|▏         | 385/20348 [00:03<02:43, 121.77it/s]
streamlit/streamlit                     : 662 stars (21.5/day):   4%|▎         | 662/18475 [00:05<02:18, 128.50it/s]
ray-project/ray                         : 411 stars (13.3/day):   2%|▏         | 411/19700 [00:03<02:33, 125.83it/s]
PaddlePaddle/Paddle                     : 210 stars (6.8/day):   1%|          | 210/17868 [00:01<02:25, 121.37it/s]
Tencent/ncnn                            : 296 stars (9.6/day):   2%|▏         | 296/14171 [00:02<01:49, 126.74it/s]
microsoft/LightGBM                      : 127 stars (4.1/day):   1%|          | 127/13609 [00:01<02:16, 98.64it/s]
google/automl                           : 43 stars (1.4/day):   1%|          | 43/4939 [00:00<00:48, 100.11it/s]
awslabs/autogluon                       : 147 stars (4.8/day):   3%|▎         | 147/4305 [00:01<00:36, 115.48it/s]
aws/amazon-sagemaker-examples           : 136 stars (4.4/day):   2%|▏         | 136/6721 [00:01<01:05, 100.64it/s]
apple/turicreate                        : 55 stars (1.8/day):   1%|          | 55/10646 [00:00<01:25, 123.90it/s]
apple/coremltools                       : 42 stars (1.4/day):   2%|▏         | 42/2608 [00:00<00:24, 104.11it/s]
openai/gpt-3                            : 68 stars (2.2/day):   1%|          | 68/11138 [00:00<02:21, 78.42it/s]
deepmind/deepmind-research              : 208 stars (6.8/day):   2%|▏         | 208/9923 [00:01<01:22, 118.31it/s]
pjreddie/darknet                        : 279 stars (9.1/day):   1%|          | 279/22483 [00:02<02:56, 125.61it/s]
AlexeyAB/darknet                        : 283 stars (9.2/day):   2%|▏         | 283/18773 [00:02<02:28, 124.58it/s]
explosion/spaCy                         : 551 stars (17.9/day):   2%|▏         | 551/23043 [00:04<03:15, 114.84it/s]
Megvii-BaseDetection/YOLOX              : 280 stars (9.1/day):   5%|▍         | 280/6016 [00:02<00:44, 129.15it/s]
WongKinYiu/yolor                        : 78 stars (2.5/day):   5%|▌         | 78/1470 [00:00<00:10, 132.87it/s]
rwightman/pytorch-image-models          : 747 stars (24.3/day):   4%|▍         | 747/17392 [00:05<02:11, 126.24it/s]
```
