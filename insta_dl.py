import os
import json
import subprocess
from urllib.parse import urlparse

import requests
import yt_dlp
from PIL import Image


class InstaDL:
    def __init__(self, *, cookies_file, download_progress=True, convert_jpg=True, delete_original_image=True):
        self.params = {
            "cookies_file": cookies_file,
            "download_progress": download_progress,
            "convert_jpg": convert_jpg,
            "delete_original_image": delete_original_image
        }

    def check_for_video(self, url):
        parts = urlparse(url).path.split("/")
        details = {}

        try:
            ydl_opts = {
                "quiet": True,
                "dumpjson": True,
                "cookiefile": self.params["cookies_file"]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)

            if info_dict.get("_type") == "playlist" and info_dict.get("playlist_count") == 0:
                print(f"\033[91mERROR:\033[0m [Instagram] {parts[-2]}: There is no video in this post")
                raise yt_dlp.utils.DownloadError("There is no video in this post")

            details["type"] = info_dict.get("_type", "video")
            details["data"] = info_dict

            return True, details
        except yt_dlp.utils.DownloadError:
            return False, {}

    def check_for_image(self, url):
        details = {}
        result = subprocess.run(
            ["gallery-dl", "-j", "--cookies", self.params["cookies_file"], url],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            try:
                resout = result.stdout
                data = json.loads(resout)
            except json.JSONDecodeError:
                print("Error: Failed to parse JSON output")
                print(f"Output of gallery-dl\n{resout}")
                return False, {}
        else:
            print("Error: gallery-dl failed to run", result.stderr)

        details["type"] = "image" if data[0][1]["count"] == 1 else "multipost"
        details["data"] = data
        return True, details

    def extract_details(self, url):
        video_check, data = self.check_for_video(url)
        if not video_check:
            image_check, data = self.check_for_image(url)
            if not image_check: return {}
        return data

    def download_insta_video(self, url, filename):
        try:
            ydl_opts = {
                "outtmpl": f"{filename}.%(ext)s",
                "format": "bv+ba/best",
                "cookiefile": self.params["cookies_file"],
                "quiet": not self.params["download_progress"]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            print(f"Video downloaded and saved successfully as {filename}")
            return True
        except yt_dlp.utils.DownloadError as e:
            print(f"Error in downloading video: {url}\n{e}")
            return False

    def download_insta_playlist(self, url, listname):
        try:
            ydl_opts = {
                "outtmpl": f"{listname}/%(playlist_index)s.%(ext)s",
                "format": "bv+ba/best",
                "cookiefile": self.params["cookies_file"],
                "quiet": not self.params["download_progress"]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            print(f"Playlist downloaded and saved successfully as {listname}")
            return True
        except yt_dlp.utils.DownloadError as e:
            print(f"Error in downloading playlist: {url}\n{e}")
            return False

    def download_image(self, url, filename):
        filename = str(filename)
        parsed_url = urlparse(url)
        _, extension = os.path.splitext(parsed_url.path)

        if not extension:
            print("Warning: URL does not contain a file extension. Defaulting to '.jpg'.")
            extension = ".jpg"

        save_path = filename + extension

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to download image: {e}")
            return False

        with open(save_path, "wb") as file:
            file.write(response.content)

        print(f"Image downloaded and saved successfully as {save_path}")

        if self.params["convert_jpg"] and extension != ".jpg":
            jpg_path = filename + ".jpg"
            try:
                with Image.open(save_path) as img:
                    img = img.convert("RGB")
                    img.save(jpg_path, "JPEG")
                print(f"Converted and saved as: {jpg_path}")

                if self.params["delete_original_image"]:
                    os.remove(save_path)
                    print(f"Original file deleted: {save_path}")
            except Exception as e:
                print(f"Conversion failed: {e}")

        return True

    def download(self, url, filename):
        details = self.extract_details(url)
        if not details:
            print(f"No information is extracted for {url}")
            return False

        match details["type"]:
            case "video":
                self.download_insta_video(url=url, filename=filename)
            case "playlist":
                self.download_insta_playlist(url=url, listname=filename)
            case "image":
                image_url = details["data"][1][1]
                self.download_image(url=image_url, filename=filename)
            case "multipost":
                os.makedirs(filename, exist_ok=True)
                for post in details["data"][1:]:
                    path = os.path.join(filename, str(post[2]["num"]))
                    self.download_image(post[1], path)
        return True
