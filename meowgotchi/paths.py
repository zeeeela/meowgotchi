from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"

FONT_PATH = ASSETS_DIR / "PixelifySans-VariableFont_wght.ttf"
PET_IMAGE_PATH = ASSETS_DIR / "black_meow.png"
MENU_ICON_PATH = ASSETS_DIR / "menu.png"
LAYOUT_ICON_PATH = ASSETS_DIR / "layout2.png" 
PLAY_ICON_PATH = ASSETS_DIR / "play.png"
STOP_ICON_PATH = ASSETS_DIR / "exit.png"
NEXT_ICON_PATH = ASSETS_DIR / "next.png"
PREV_ICON_PATH = ASSETS_DIR / "prev.png"   

PAPER_PATH = ASSETS_DIR / "papers/"
GITHUB_ACTIVITY_PATH = ASSETS_DIR / "github_activity.csv"

def github_activity_image_path(date=None):
    date = date or datetime.now()
    return ASSETS_DIR / f"github_activity_{date.strftime('%Y%m%d')}.png"