<br>
<img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320">

# Count GitHub Stars per Day ⭐

Track GitHub stars per day over a date range to measure the open-source popularity of different repositories.

# Requirements

`PyGitHub` is required to access the [GitHub REST API] via Python. This library enables you to manage [GitHub] resources such as repositories, user profiles, and organizations in your Python applications.

[GitHub REST API]: https://docs.github.com/en/rest
[GitHub]: https://github.com

```bash
pip install -r requirements.txt  # install
```

# Usage

Update `TOKEN` to a valid [GitHub access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) in `count_stars.py` L15 and then run:

```python
python count_stars.py
```

# Result

When run on April 10th, 2022 result is:

```python
Counting stars for last 30.0 days from 02 May 2022

ultralytics/yolov5                      1572 stars  (52.4/day)  :   6%|▌         | 1572/25683 [00:16<04:15, 94.53it/s]
facebookresearch/detectron2             391 stars   (13.0/day)  :   2%|▏         | 391/20723 [00:04<03:56, 85.86it/s]
deepmind/deepmind-research              165 stars   (5.5/day)   :   2%|▏         | 165/10079 [00:01<01:50, 89.52it/s]
aws/amazon-sagemaker-examples           120 stars   (4.0/day)   :   2%|▏         | 120/6830 [00:02<02:16, 49.17it/s]
awslabs/autogluon                       127 stars   (4.2/day)   :   3%|▎         | 127/4436 [00:01<01:00, 71.45it/s]
microsoft/LightGBM                      122 stars   (4.1/day)   :   1%|          | 122/13730 [00:01<03:10, 71.54it/s]
openai/gpt-3                            95 stars    (3.2/day)   :   1%|          | 95/11225 [00:01<03:34, 52.00it/s]
apple/turicreate                        40 stars    (1.3/day)   :   0%|          | 40/10676 [00:00<02:24, 73.59it/s]
apple/coremltools                       41 stars    (1.4/day)   :   2%|▏         | 41/2641 [00:00<00:46, 56.00it/s]
google/automl                           55 stars    (1.8/day)   :   1%|          | 55/4991 [00:00<01:25, 57.53it/s]
google-research/google-research         548 stars   (18.3/day)  :   2%|▏         | 548/23087 [00:07<05:11, 72.37it/s]
google-research/vision_transformer      279 stars   (9.3/day)   :   6%|▌         | 279/5043 [00:02<00:49, 95.93it/s]
google-research/bert                    283 stars   (9.4/day)   :   1%|          | 283/31066 [00:03<07:01, 73.11it/s]
NVlabs/stylegan3                        158 stars   (5.3/day)   :   4%|▍         | 158/4045 [00:01<00:44, 86.41it/s]
Tencent/ncnn                            278 stars   (9.3/day)   :   2%|▏         | 278/14440 [00:03<02:41, 87.55it/s]
Megvii-BaseDetection/YOLOX              273 stars   (9.1/day)   :   4%|▍         | 273/6286 [00:02<01:04, 92.53it/s]
PaddlePaddle/Paddle                     239 stars   (8.0/day)   :   1%|▏         | 239/18086 [00:02<03:33, 83.73it/s]
rwightman/pytorch-image-models          772 stars   (25.7/day)  :   4%|▍         | 772/18169 [00:08<03:21, 86.24it/s]
streamlit/streamlit                     375 stars   (12.5/day)  :   2%|▏         | 375/18834 [00:03<03:07, 98.67it/s]
explosion/spaCy                         234 stars   (7.8/day)   :   1%|          | 234/23249 [00:02<03:47, 101.24it/s]
PyTorchLightning/pytorch-lightning      407 stars   (13.6/day)  :   2%|▏         | 407/18246 [00:04<03:02, 97.83it/s]
ray-project/ray                         545 stars   (18.2/day)  :   3%|▎         | 545/20228 [00:05<03:03, 107.33it/s]
fastai/fastai                           136 stars   (4.5/day)   :   1%|          | 136/22202 [00:01<04:28, 82.22it/s]
AlexeyAB/darknet                        248 stars   (8.3/day)   :   1%|▏         | 248/18993 [00:02<03:40, 84.84it/s]
pjreddie/darknet                        201 stars   (6.7/day)   :   1%|          | 201/22651 [00:02<05:13, 71.62it/s]
WongKinYiu/yolor                        92 stars    (3.1/day)   :   6%|▌         | 92/1559 [00:01<00:16, 87.69it/s]
wandb/client                            66 stars    (2.2/day)   :   2%|▏         | 66/3853 [00:00<00:46, 82.16it/s]
Deci-AI/super-gradients                 74 stars    (2.5/day)   :  19%|█▉        | 74/380 [00:00<00:03, 96.71it/s]
neuralmagic/sparseml                    105 stars   (3.5/day)   :  11%|█         | 105/947 [00:01<00:08, 101.97it/s]
mosaicml/composer                       247 stars   (8.2/day)   :  19%|█▉        | 247/1306 [00:02<00:10, 104.76it/s]
nebuly-ai/nebullvm                      205 stars   (6.8/day)   :  20%|█▉        | 205/1045 [00:02<00:08, 97.46it/s]
Done in 125.7s
```

# Contribute

We love your input! Ultralytics open-source efforts would not be possible without help from our community. Please see our [Contributing Guide](https://docs.ultralytics.com/help/contributing) to get started, and fill out our [Survey](https://ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey) to send us feedback on your experience. Thank you 🙏 to all our contributors!

<!-- SVG image from https://opencollective.com/ultralytics/contributors.svg?width=990 -->
<a href="https://github.com/ultralytics/yolov5/graphs/contributors">
<img width="100%" src="https://github.com/ultralytics/assets/raw/main/im/image-contributors.png" alt="Ultralytics open-source contributors"></a>

# License

Ultralytics offers two licensing options to accommodate diverse use cases:

- **AGPL-3.0 License**: This [OSI-approved](https://opensource.org/licenses/) open-source license is ideal for students and enthusiasts, promoting open collaboration and knowledge sharing. See the [LICENSE](https://github.com/ultralytics/ultralytics/blob/main/LICENSE) file for more details.
- **Enterprise License**: Designed for commercial use, this license permits seamless integration of Ultralytics software and AI models into commercial goods and services, bypassing the open-source requirements of AGPL-3.0. If your scenario involves embedding our solutions into a commercial offering, reach out through [Ultralytics Licensing](https://ultralytics.com/license).

# Contact

For Ultralytics bug reports and feature requests please visit [GitHub Issues](https://github.com/ultralytics/stars/issues), and join our [Discord](https://ultralytics.com/discord) community for questions and discussions!

<br>
<div align="center">
  <a href="https://github.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-github.png" width="3%" alt="Ultralytics GitHub"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.linkedin.com/company/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-linkedin.png" width="3%" alt="Ultralytics LinkedIn"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://twitter.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-twitter.png" width="3%" alt="Ultralytics Twitter"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://youtube.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-youtube.png" width="3%" alt="Ultralytics YouTube"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.tiktok.com/@ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-tiktok.png" width="3%" alt="Ultralytics TikTok"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.instagram.com/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-instagram.png" width="3%" alt="Ultralytics Instagram"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://ultralytics.com/discord"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-discord.png" width="3%" alt="Ultralytics Discord"></a>
</div>
