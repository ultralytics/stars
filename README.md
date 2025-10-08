<a href="https://www.ultralytics.com/"><img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320" alt="Ultralytics logo"></a>

# Ultralytics Analytics & Star Tracking ⭐️

Track GitHub stars, contributors, and PyPI downloads for [Ultralytics](https://github.com/ultralytics) projects.

[![Ultralytics Actions](https://github.com/ultralytics/stars/actions/workflows/format.yml/badge.svg)](https://github.com/ultralytics/stars/actions/workflows/format.yml)
[![Update Analytics](https://github.com/ultralytics/stars/actions/workflows/analytics.yml/badge.svg)](https://github.com/ultralytics/stars/actions/workflows/analytics.yml)
[![Ultralytics Discord](https://img.shields.io/discord/1089800235347353640?logo=discord&logoColor=white&label=Discord&color=blue)](https://discord.com/invite/ultralytics)
[![Ultralytics Forums](https://img.shields.io/discourse/users?server=https%3A%2F%2Fcommunity.ultralytics.com&logo=discourse&label=Forums&color=blue)](https://community.ultralytics.com/)
[![Ultralytics Reddit](https://img.shields.io/reddit/subreddit-subscribers/ultralytics?style=flat&logo=reddit&logoColor=white&label=Reddit&color=blue)](https://reddit.com/r/ultralytics)

## 📊 Analytics API

Real-time analytics updated daily at 02:07 UTC via GitHub Actions.

### GitHub Stars & Contributors

```
https://raw.githubusercontent.com/ultralytics/stars/main/data/org_stars.json
```

**Fields:**

- `total_stars`: Total stars across all public repos
- `total_contributors`: Sum of contributors across all repos (may include duplicates)
- `public_repos`: Number of public repositories
- `timestamp`: Last update time (ISO 8601)
- `repos`: Array with per-repo `name`, `stars`, and `contributors`

### PyPI Downloads

```
https://raw.githubusercontent.com/ultralytics/stars/main/data/pypi_downloads.json
```

**Packages tracked:**

- `ultralytics` - Main YOLO11 package
- `ultralytics-actions` - GitHub Actions
- `ultralytics-thop` - PyTorch ops profiling
- `hub-sdk` - Ultralytics HUB SDK
- `mkdocs-ultralytics-plugin` - Documentation plugin
- `ultralytics-autoimport` - Auto-import utilities

**Fields:**

- `total_last_month`: Combined downloads across all packages (last 30 days)
- `timestamp`: Last update time (ISO 8601)
- `packages`: Array with per-package `last_day`, `last_week`, and `last_month` downloads

### Example Usage

**REST API:**

```bash
curl https://raw.githubusercontent.com/ultralytics/stars/main/data/org_stars.json
curl https://raw.githubusercontent.com/ultralytics/stars/main/data/pypi_downloads.json
```

**Python:**

```python
import requests

stars = requests.get("https://raw.githubusercontent.com/ultralytics/stars/main/data/org_stars.json").json()
downloads = requests.get("https://raw.githubusercontent.com/ultralytics/stars/main/data/pypi_downloads.json").json()
print(f"Total stars: {stars['total_stars']:,}")
print(f"Total contributors: {stars['total_contributors']:,}")
print(f"PyPI downloads (30d): {downloads['total_last_month']:,}")
```

## 🔧 Repository Structure

```
stars/
├── fetch_stats.py          # Unified analytics fetcher (GitHub + PyPI)
├── count_stars.py          # Historical star tracking script
├── utils.py                # Shared utilities
├── repos.yaml              # Repositories to track
├── data/
│   ├── org_stars.json     # GitHub analytics (updated daily)
│   └── pypi_downloads.json # PyPI analytics (updated daily)
└── .github/workflows/
    ├── analytics.yml       # Daily analytics update
    └── format.yml         # Code formatting
```

## 📈 Historical Star Tracking

Track star growth over time for any GitHub repositories using `count_stars.py`.

### Setup

```bash
pip install -r requirements.txt
```

### Usage

```bash
python count_stars.py --token YOUR_GITHUB_TOKEN --days 30 --save
```

**Arguments:**

- `--token`: GitHub Personal Access Token ([create one](https://github.com/settings/tokens))
- `--days`: Number of trailing days to analyze (default: 30)
- `--save`: Save user information to CSV (optional)

Edit `repos.yaml` to customize which repositories to track.

### Example Output

```
Counting stars for last 30.0 days from 08 October 2025

ultralytics/ultralytics                 1572 stars  (52.4/day)  :   6%|▌         | 1572/46959 [00:16<04:15, 94.53it/s]
ultralytics/yolov5                      391 stars   (13.0/day)  :   2%|▏         | 391/55572 [00:04<03:56, 85.86it/s]
...
```

## 💡 Contribute

Contributions are the lifeblood of the [open-source](https://www.ultralytics.com/blog/tips-to-start-contributing-to-ultralytics-open-source-projects) community, and we greatly appreciate your input! Whether it's bug fixes, feature suggestions, or documentation improvements, every contribution helps.

Please see our [Contributing Guide](https://docs.ultralytics.com/help/contributing/) for detailed instructions on how to get involved. We also encourage you to fill out our [Survey](https://www.ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey) to share your feedback. Thank you 🙏 to everyone who contributes!

[![Ultralytics open-source contributors](https://raw.githubusercontent.com/ultralytics/assets/main/im/image-contributors.png)](https://github.com/ultralytics/ultralytics/graphs/contributors)

## 📝 License

Ultralytics provides two licensing options to accommodate different use cases:

- **AGPL-3.0 License**: Ideal for students and enthusiasts, this [OSI-approved](https://opensource.org/license/agpl-v3) open-source license promotes collaboration and knowledge sharing. See the [LICENSE](https://github.com/ultralytics/stars/blob/main/LICENSE) file for details.
- **Enterprise License**: Designed for commercial applications, this license allows for the integration of Ultralytics software and AI models into commercial products and services. For more information, visit [Ultralytics Licensing](https://www.ultralytics.com/license).

## 📬 Contact Us

If you encounter bugs, have feature requests, or wish to contribute, please visit [GitHub Issues](https://github.com/ultralytics/stars/issues). For broader discussions and questions about Ultralytics projects, join our vibrant community on [Discord](https://discord.com/invite/ultralytics)!

<br>
<div align="center">
  <a href="https://github.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-github.png" width="3%" alt="Ultralytics GitHub"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.linkedin.com/company/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-linkedin.png" width="3%" alt="Ultralytics LinkedIn"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://twitter.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-twitter.png" width="3%" alt="Ultralytics Twitter"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://youtube.com/ultralytics?sub_confirmation=1"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-youtube.png" width="3%" alt="Ultralytics YouTube"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.tiktok.com/@ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-tiktok.png" width="3%" alt="Ultralytics TikTok"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://ultralytics.com/bilibili"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-bilibili.png" width="3%" alt="Ultralytics BiliBili"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://discord.com/invite/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-discord.png" width="3%" alt="Ultralytics Discord"></a>
</div>
