# InstaDL
A wrapper script to download Instagram posts using `yt-dlp` and `gallery-dl`, supporting videos, images, and multi-posts with optional image conversion.

> This project is for **educational purposes only**. Use it at your own risk. Downloading content from Instagram may violate its **Terms of Service**, and redistributing downloaded content could lead to legal consequences.

## Features
- Download Instagram videos, reels, and multi-posts
- Automatically convert images to JPG (optional)
- Uses cookies for authenticated downloads
- Supports playlist downloading
- Simple and user-friendly command-line usage

## Setup

### Clone the Repository
```bash
git clone https://github.com/yourusername/instagram-downloader.git
cd instagram-downloader
```

### Install Dependencies
```bash
pip install requirements.txt
```

### Add cookies.txt
Use the **"Get Cookies.txt"** or **"Cookie Editor"** browser extension to extract cookies for Instagram and save them as `cookies.txt` in the project directory.

## Usage

### Example Script Usage
```python
from insta_dl import InstaDL

downloader = InstaDL(cookies_file="cookies.txt")
downloader.download("https://www.instagram.com/p/EXAMPLE/", "output_filename")
```

### Command-Line Usage
You can integrate this script with the command line for ease of use.

```bash
python script.py "https://www.instagram.com/p/EXAMPLE/" "output_filename"
```

### **Built With**
-   `yt-dlp` – For downloading Instagram videos
-   `gallery-dl` – For extracting Instagram images
-   `Pillow` – For image processing (JPG conversion)
-   `Requests` – For handling HTTP requests
