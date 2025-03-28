# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

"""
Count GitHub repository stars over a time period.

Usage:
    $ python path/to/count_stars.py
"""

import argparse
import time
from datetime import datetime

import pandas as pd
import yaml
from github import Github  # pip install PyGithub
from tqdm import tqdm

# Replace with your GitHub personal access token
GITHUB_TOKEN = ""  # i.e. 'ghp_1gwB...'


def run(
    token="",  # GitHub access token
    days=30,  # trailing days to analyze
    save=False,  # save user info
):
    """
    Counts GitHub stars for specified repositories over a given period and optionally saves user information.

    Args:
        token (str): GitHub personal access token. Default is an empty string which means no authentication.
        days (int): Number of trailing days to analyze. Default is 30.
        save (bool): Whether to save user information to a CSV file. Default is False.

    Returns:
        None

    Notes:
        - Ensure you have a valid GitHub personal access token if you are accessing private repositories or want to avoid
          rate limits. You can generate one at https://github.com/settings/tokens.
        - Requires 'repos.yaml' file in the same directory with a list of repositories to analyze, in the format:
          ```yaml
          repositories:
              - 'repository_owner/repository_name'
              - 'another_owner/another_repository'
          ```

    Example:
        ```python
        from path.to.module import run
        run(token='your_github_token', days=30, save=True)
        ```
    """
    # Settings
    # date = datetime(2022, 3, 1)  # count stars since this day, i.e. March 1st 2022
    # days = (datetime.now() - date).total_seconds() / 86400  # compute number of days
    # days = 30  # specify days directly, i.e. last 30 days

    # Get repos
    with open("repos.yaml") as f:
        repos = yaml.safe_load(f)["repositories"]

    # Parameters
    g = Github(token)  # create a GitHub instance
    print(f"Counting stars for last {days:.1f} days from {datetime.now():%d %B %Y}\n")
    pd.options.display.max_columns = None

    # Run
    t, users = time.time(), []
    sleep = 1.39  # sleep seconds between requests (5000/hr limit)
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
                            users.append(
                                [
                                    r.full_name,
                                    u.name,
                                    u.company,
                                    u.email,
                                    u.location,
                                    u.html_url,
                                    u.followers,
                                    x.starred_at,
                                ]
                            )
                else:
                    n = len(dates)
                    s1 = f"{n} stars"
                    s2 = f"({n / days:.1f}/day)"
                    pbar.desc = f"{r.full_name:40s}{s1:12s}{s2:12s}"
                    break

        except Exception as e:
            print(e)

        df = pd.DataFrame(dates, columns=["date", "stars"])
        df.date = pd.to_datetime(df.date)
        # df.to_csv(f'dates_{r.name}.csv')
        # dg = df.groupby(pd.Grouper(key='date', freq='1M')).sum()  # group by month
        # dg = df.groupby(pd.Grouper(key='date', freq='1D')).sum()  # group by day

    print(f"Done in {time.time() - t:.1f}s")
    if save:
        x = pd.DataFrame(users, columns=["Repo", "Name", "Company", "Email", "Location", "GitHub", "Followers", "Date"])
        x.to_csv("users.csv")
        print(f"{len(x)} users saved to users.csv")


def parse_opt():
    """
    Parses command-line options and returns the arguments.

    Args:
        None

    Returns:
        argparse.Namespace: Parsed command-line arguments including:
            - token (str): GitHub Personal Access Token.
            - days (int): Trailing days to analyze.
            - save (bool): Flag to save user information.

    Example:
        ```python
        args = parse_opt()
        run(token=args.token, days=args.days, save=args.save)
        ```
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", type=str, default=GITHUB_TOKEN, help="GitHub Personal Access Token")
    parser.add_argument("--days", type=int, default=30, help="Trailing days to analyze")
    parser.add_argument("--save", action="store_true", help="Save user info")
    return parser.parse_args()


def main(opt):
    """
    Executes the main process of counting GitHub repository stars over a specified time period with optional user
    information saving.

    Args:
        opt (argparse.Namespace): Command-line arguments parsed by `parse_opt()`, which include:
            token (str): GitHub personal access token to authenticate API requests.
            days (int): Number of trailing days to analyze for star counts. Defaults to 30.
            save (bool): Flag to save user information of those who starred the repositories. Defaults to False.

    Returns:
        None

    Example:
        To count stars over the last 30 days and save user info:

        ```python
        $ python path/to/script.py --token YOUR_GITHUB_TOKEN --days 30 --save
        ```
    """
    run(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
