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

ultralytics/yolov5                      1603 stars  (52.0/day)  :   7%|▋         | 1603/24085 [00:12<02:48, 133.15it/s]
facebookresearch/detectron2             385 stars   (12.5/day)  :   2%|▏         | 385/20348 [00:03<02:46, 119.57it/s]
PyTorchLightning/pytorch-lightning      414 stars   (13.4/day)  :   2%|▏         | 414/17852 [00:03<02:16, 127.75it/s]
streamlit/streamlit                     662 stars   (21.5/day)  :   4%|▎         | 662/18475 [00:05<02:15, 131.23it/s]
ray-project/ray                         412 stars   (13.4/day)  :   2%|▏         | 412/19701 [00:03<03:06, 103.19it/s]
PaddlePaddle/Paddle                     210 stars   (6.8/day)   :   1%|          | 210/17868 [00:01<02:31, 116.34it/s]
Tencent/ncnn                            296 stars   (9.6/day)   :   2%|▏         | 296/14171 [00:02<01:50, 125.60it/s]
microsoft/LightGBM                      127 stars   (4.1/day)   :   1%|          | 127/13609 [00:01<02:29, 90.12it/s]
openai/gpt-3                            69 stars    (2.2/day)   :   1%|          | 69/11139 [00:00<02:20, 78.58it/s]
google/automl                           43 stars    (1.4/day)   :   1%|          | 43/4939 [00:00<00:48, 101.11it/s]
deepmind/deepmind-research              208 stars   (6.7/day)   :   2%|▏         | 208/9923 [00:01<01:20, 120.49it/s]
awslabs/autogluon                       147 stars   (4.8/day)   :   3%|▎         | 147/4305 [00:01<00:36, 114.93it/s]
aws/amazon-sagemaker-examples           136 stars   (4.4/day)   :   2%|▏         | 136/6721 [00:01<01:02, 105.61it/s]
apple/turicreate                        55 stars    (1.8/day)   :   1%|          | 55/10646 [00:00<01:22, 127.75it/s]
apple/coremltools                       42 stars    (1.4/day)   :   2%|▏         | 42/2608 [00:00<00:25, 100.24it/s]
pjreddie/darknet                        279 stars   (9.1/day)   :   1%|          | 279/22482 [00:02<02:52, 128.97it/s]
AlexeyAB/darknet                        283 stars   (9.2/day)   :   2%|▏         | 283/18772 [00:02<02:15, 136.74it/s]
explosion/spaCy                         551 stars   (17.9/day)  :   2%|▏         | 551/23043 [00:04<03:04, 121.72it/s]
Megvii-BaseDetection/YOLOX              280 stars   (9.1/day)   :   5%|▍         | 280/6016 [00:02<00:41, 138.38it/s]
WongKinYiu/yolor                        78 stars    (2.5/day)   :   5%|▌         | 78/1470 [00:00<00:10, 133.42it/s]
rwightman/pytorch-image-models          747 stars   (24.2/day)  :   4%|▍         | 747/17392 [00:05<02:02, 136.22it/s]
```
