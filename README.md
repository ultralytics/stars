<br>
<img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320">

# Count GitHub Stars per Day ⭐

**Overview**: The objective of this project is to monitor and visualize the popularity of various open-source repositories by tracking the number of GitHub stars they receive daily. This kind of information can be valuable for developers and companies to understand trends in technology tools and frameworks.

## Requirements

To access the GitHub REST API from your Python code, you'll need the `PyGitHub` library. This library facilitates interaction with GitHub resources such as repositories, user profiles, and organizations.

[GitHub REST API]: https://docs.github.com/en/rest
[GitHub]: https://github.com

To install `PyGitHub`, simply run the following command, which will ensure you have all the necessary libraries:

```bash
pip install -r requirements.txt  # installs all requirements
```

## Usage Instructions

1. First, you need a GitHub access token. Follow the guide to create one [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).
2. Next, open the `count_stars.py` file.
3. There, on line 15 (L15), replace `TOKEN` with your own GitHub access token.

Once set up, to start counting stars, run the script in your terminal:

```python
python count_stars.py  # execute the script
```

## Results & Interpretation

Below is an example of the output you will receive when running the script:

```python
# The following is a formatted display of results obtained on April 10th, 2022.

Counting stars for last 30.0 days from 02 May 2022

# Sample output for a repository: 
# > [Repository owner/Repository name]: [Total stars accumulated in period] stars ([Average stars per day])  :  [Progress bar indicating completion]

...
```

Please note that the progress bar is a visual representation meant to indicate the proportion of the count completed for each repository.

## How to Contribute 🤝

Your contributions are what make the open-source community such a powerful and resourceful place. If you wish to contribute to our project, kindly refer to our [Contributing Guide](https://docs.ultralytics.com/help/contributing) and feel free to take our [Survey](https://ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey) to provide feedback. Together we can make a difference! A heartfelt thank you 🙏 to everyone who has contributed so far.

<div align="center">
<!-- This SVG image links to the contributors of the Ultralytics/yolov5 repository -->
<a href="https://github.com/ultralytics/yolov5/graphs/contributors">
<img width="100%" src="https://github.com/ultralytics/assets/raw/main/im/image-contributors.png" alt="Contributors to Ultralytics open-source">
</a>
</div>

## License

Ultralytics offers this software under the AGPL-3.0 License (see [LICENSE](https://github.com/ultralytics/ultralytics/blob/main/LICENSE) for more details), which is an OSI-approved open-source license that ensures your freedom to share and change the software, and to make sure it remains free for all its users.

For proprietary licensing options, please [contact us](https://ultralytics.com/license) directly.

## Getting Help

Have you encountered an issue or do you have a feature suggestion? Head over to [GitHub Issues](https://github.com/ultralytics/stars/issues) to let us know.

We also invite you to join our vibrant [Discord](https://ultralytics.com/discord) community for discussions, questions, and collaboration!

<br>
<div align="center">
  <a href="https://github.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-github.png" width="2.5%" alt="Ultralytics on GitHub"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="2.5%" alt="spacer">
  <a href="https://www.linkedin.com/company/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-linkedin.png" width="2.5%" alt="Ultralytics on LinkedIn"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="2.5%" alt="spacer">
  <a href="https://twitter.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-twitter.png" width="2.5%" alt="Ultralytics on Twitter"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="2.5%" alt="spacer">
  <a href="https://youtube.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-youtube.png" width="2.5%" alt="Ultralytics on YouTube"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="2.5%" alt="spacer">
  <a href="https://www.tiktok.com/@ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-tiktok.png" width="2.5%" alt="Ultralytics on TikTok"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="2.5%" alt="spacer">
  <a href="https://www.instagram.com/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-instagram.png" width="2.5%" alt="Ultralytics on Instagram"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="2.5%" alt="spacer">
  <a href="https://ultralytics.com/discord"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-discord.png" width="2.5%" alt="Join Ultralytics Discord"></a>
</div>
<br>
```

I hope this enhances the clarity and appeal of your README documentation. The formatting and additional context should improve the user experience for both technical and non-technical audiences.
