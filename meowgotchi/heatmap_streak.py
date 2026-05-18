import csv
from tkinter import font
from matplotlib import colors
import requests
import os
from dotenv import load_dotenv
import pandas as pd
import calplot
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from collections import Counter
from matplotlib.font_manager import FontProperties
from meowgotchi.paths import FONT_PATH, GITHUB_ACTIVITY_PATH, github_activity_image_path


def generate_github_activity_heatmap(image_path=None):

    font = FontProperties(fname=str(FONT_PATH), size=15)

    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    username = "zeeeela"  

    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.github.com/users/{username}/events"
    resp = requests.get(url, headers=headers)
    events = resp.json()

    output_path = GITHUB_ACTIVITY_PATH
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "repo", "created_at", "action"])
        for event in events:
            writer.writerow([
                event.get("type"),
                event.get("repo", {}).get("name"),
                event.get("created_at"),
                event.get("payload", {}).get("action")
            ])

    print(f"saved to {output_path}")

    data = pd.read_csv(output_path)
    data['created_at'] = pd.to_datetime(data['created_at'])
    dates = data['created_at'].dt.date.tolist()

    colors = [ '#df90b9', '#ad4785', '#52464b']
    cmap = ListedColormap(colors)

    # Count occurrences per date
    date_counts = Counter(dates)
    date_series = pd.Series(date_counts)
    date_series.index = pd.to_datetime(date_series.index)

    # Create the calendar heatmap
    fig, ax = calplot.calplot(
        date_series,
        cmap=cmap,
        suptitle=None,
        colorbar=False,
        edgecolor='#eec7bd',
        fillcolor="white")
    fig.suptitle("Github Activity Calendar Heatmap", fontproperties=font)
    # Save to file
    image_path = image_path or github_activity_image_path()
    plt.savefig(image_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    return image_path

if __name__ == "__main__":
    generate_github_activity_heatmap()