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

When run on April 3rd, 2022 result is:

```python
Counting stars for last 30.0 days

ultralytics/yolov5                      1596 stars  (53.2/day)  :   7% 1596/24203 [00:09<02:20, 160.51it/s]
facebookresearch/detectron2             372 stars   (12.4/day)  :   2% 372/20380 [00:02<02:20, 141.93it/s]
deepmind/deepmind-research              205 stars   (6.8/day)   :   2% 205/9932 [00:01<01:06, 145.76it/s]
aws/amazon-sagemaker-examples           128 stars   (4.3/day)   :   2% 128/6729 [00:00<00:44, 150.01it/s]
awslabs/autogluon                       149 stars   (5.0/day)   :   3% 149/4316 [00:01<00:28, 143.74it/s]
microsoft/LightGBM                      126 stars   (4.2/day)   :   1% 126/13622 [00:01<02:08, 105.21it/s]
openai/gpt-3                            73 stars    (2.4/day)   :   1% 73/11149 [00:00<01:18, 141.94it/s]
apple/turicreate                        57 stars    (1.9/day)   :   1% 57/10651 [00:00<01:41, 104.59it/s]
apple/coremltools                       39 stars    (1.3/day)   :   1% 39/2607 [00:00<00:22, 115.67it/s]
NVlabs/stylegan3                        163 stars   (5.4/day)   :   4% 163/3901 [00:01<00:27, 136.62it/s]
Tencent/ncnn                            277 stars   (9.2/day)   :   2% 277/14185 [00:01<01:28, 157.73it/s]
Megvii-BaseDetection/YOLOX              274 stars   (9.1/day)   :   5% 274/6034 [00:02<00:59, 96.40it/s]
PaddlePaddle/Paddle                     201 stars   (6.7/day)   :   1% 201/17877 [00:01<01:51, 158.78it/s]
rwightman/pytorch-image-models          724 stars   (24.1/day)  :   4% 724/17452 [00:04<01:42, 163.86it/s]
streamlit/streamlit                     617 stars   (20.6/day)  :   3% 617/18498 [00:03<01:50, 162.51it/s]
explosion/spaCy                         551 stars   (18.4/day)  :   2% 551/23052 [00:03<02:25, 154.51it/s]
PyTorchLightning/pytorch-lightning      409 stars   (13.6/day)  :   2% 409/17883 [00:02<01:56, 149.61it/s]
ray-project/ray                         390 stars   (13.0/day)  :   2% 390/19722 [00:02<02:04, 155.03it/s]
fastai/fastai                           137 stars   (4.6/day)   :   1% 137/22107 [00:00<02:31, 145.06it/s]
google/automl                           45 stars    (1.5/day)   :   1% 45/4941 [00:00<00:37, 130.84it/s]
AlexeyAB/darknet                        268 stars   (8.9/day)   :   1% 268/18786 [00:01<02:07, 144.91it/s]
pjreddie/darknet                        269 stars   (9.0/day)   :   1% 269/22496 [00:01<02:35, 143.38it/s]
WongKinYiu/yolor                        73 stars    (2.4/day)   :   5% 73/1475 [00:00<00:12, 114.79it/s]
wandb/client                            71 stars    (2.4/day)   :   2% 71/3794 [00:00<00:27, 134.94it/s]
Deci-AI/super-gradients                 19 stars    (0.6/day)   :   6% 19/312 [00:00<00:05, 57.68it/s]
Done in 62.2s
```
