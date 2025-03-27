import sys
from insta_dl import InstaDL

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <url> <filename>")
        sys.exit(1)

    url = sys.argv[1]
    filename = sys.argv[2]

    downloader = InstaDL(cookies_file="cookies.txt")  # Initialize the downloader with necessary settings
    success = downloader.download(url, filename)

    if success:
        print("Download completed successfully!")
    else:
        print("Download failed.")
