<img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320">

# Count GitHub Stars per Day ⭐️

Track the daily growth of GitHub stars over a time period to gauge the open-source popularity of various repositories.

## 📌 Requirements

To interface with the [GitHub REST API](https://docs.github.com/en/rest) using Python, the `PyGitHub` library is required. Utilize this library to interact with GitHub resources such as repositories, user profiles, and organizations within your Python applications.

### Installation

Run the following command to install dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt  # Install required libraries
```

## 🚀 Usage

First, update the `TOKEN` in `count_stars.py` on line 15 with your valid [GitHub access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). Then execute the script:

```python
# Before running, ensure TOKEN is set to your GitHub access token.
python count_stars.py
```

## 📈 Result

The output below shows the star count for various repositories on April 10th, 2022, over the last 30 days since May 2nd, 2022:

```python
# The script provides a streamlined summary of star counts and daily averages:
# Example:
# <repository-name> <total stars for the period> stars (<average stars per day>/day) : <Progress Bar> [<current progress>/<total stars>] [Elapsed Time]

# Representative output sample:
... (output trimmed for brevity) ...
```

## 💡 Contribute

Contributions are what make the open-source community thrive. We value your ideas and input! Refer to our [Contributing Guide](https://docs.ultralytics.com/help/contributing) to get started and complete our [Survey](https://ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey) to give us feedback on your experience. A big thank you 🙏 to all our contributors!

<!-- Always showcase the community's effort with an image link to contributors. -->
<a href="https://github.com/ultralytics/yolov5/graphs/contributors">
<img width="100%" src="https://opencollective.com/ultralytics/contributors.svg?width=890" alt="Ultralytics open-source contributors"></a>

## 📝 License

Ultralytics offers two types of licensing options:

- **AGPL-3.0 License**: This [Open Source Initiative (OSI)-approved](https://opensource.org/licenses/agpl-3.0) license is fit for students, hobbyists, and enthusiasts, promoting collaborative open-source development. Consult the [LICENSE](https://github.com/ultralytics/ultralytics/blob/main/LICENSE) file for complete details.
- **Enterprise License**: Tailored for commercial uses, this licensing option allows the seamless integration of Ultralytics software and AI models into commercial products and services without the obligations typically associated with AGPL-3.0. If you are looking to incorporate our solutions into your commercial products, please reach out via [Ultralytics Licensing](https://ultralytics.com/license).

## 📬 Contact

For bug reports, feature requests, or any other queries, please head over to our [GitHub Issues](https://github.com/ultralytics/stars/issues). We also invite you to join our vibrant [Discord](https://ultralytics.com/discord) community for further discussions and support!

<br>
<!-- Social media and community links are essential for outreach and engagement. -->
<div align="center">
  <a href="https://github.com/ultralytics"><img src="https://opencollective.com/ultralytics/contributors.svg?width=60" alt="Ultralytics GitHub"></a>
  <a href="https://www.linkedin.com/company/ultralytics/"><img src="https://opencollective.com/ultralytics/contributors.svg?width=60" alt="Ultralytics LinkedIn"></a>
  <a href="https://twitter.com/ultralytics"><img src="https://opencollective.com/ultralytics/contributors.svg?width=60" alt="Ultralytics Twitter"></a>
  <a href="https://youtube.com/ultralytics"><img src="https://opencollective.com/ultralytics/contributors.svg?width=60" alt="Ultralytics YouTube"></a>
  <a href="https://www.tiktok.com/@ultralytics"><img src="https://opencollective.com/ultralytics/contributors.svg?width=60" alt="Ultralytics TikTok"></a>
  <a href="https://www.instagram.com/ultralytics/"><img src="https://opencollective.com/ultralytics/contributors.svg?width=60" alt="Ultralytics Instagram"></a>
  <a href="https://ultralytics.com/discord"><img src="https://opencollective.com/ultralytics/contributors.svg?width=60" alt="Ultralytics Discord"></a>
</div>
