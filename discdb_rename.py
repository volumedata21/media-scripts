import os
import re
import requests
from bs4 import BeautifulSoup
import subprocess

# Helper function to sanitize filenames
def sanitize_filename(name):
    """Sanitize the filename by removing or replacing invalid characters."""
    return re.sub(r'[\\/*?:"<>|]', '-', name)

# Series-specific functions

def duration_to_seconds(time_str):
    """Convert duration from HH:MM:SS format to seconds."""
    h, m, s = map(int, time_str.strip().split(":"))
    return h * 3600 + m * 60 + s

def get_mkv_durations(folder_path):
    """Get durations, file sizes, and creation times for MKV files."""
    mkv_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.mkv')]
    file_data = []

    for f in mkv_files:
        file_path = os.path.join(folder_path, f)
        try:
            output = subprocess.check_output([
                'ffprobe', '-v', 'error', '-show_entries',
                'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path
            ])
            duration = int(float(output.decode().strip()))
            size = os.path.getsize(file_path)
            created = os.path.getctime(file_path)
            file_data.append({
                'filename': file_path,
                'original_name': f,
                'duration': duration,
                'size': size,
                'created': created
            })
        except subprocess.CalledProcessError:
            print(f"⚠️ Error reading duration of {f}")
    return file_data

def extract_show_name(url):
    """Extract the show name from the DiscDB URL."""
    match = re.search(r'/series/([^/]+)', url)
    if match:
        raw = match.group(1)
        clean = re.sub(r'-\d{4}$', '', raw)
        return clean.replace('-', ' ').title()
    return "Unknown Show"

def parse_discdb(url):
    """Parse the DiscDB page and extract episode details."""
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    rows = soup.select('table tbody tr')
    episodes = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 7:
            continue
        title = cols[1].text.strip()
        type_ = cols[2].text.strip()
        ep_num = cols[4].text.strip()
        ep_num = int(ep_num) if ep_num.isdigit() else 0
        season_match = re.search(r's(\d{2})d\d{2}', url.lower())  # FIXED: case-insensitive match
        season = int(season_match.group(1)) if season_match else 1
        duration = cols[6].text.strip()
        try:
            seconds = duration_to_seconds(duration)
        except:
            continue
        suffix = ''
        if type_.lower() != 'episode':
            suffix = f'-{type_.lower()}'
        episodes.append({
            'title': title,
            'season': season,
            'episode': ep_num,
            'duration': seconds,
            'suffix': suffix,
            'type': type_.lower()
        })
    return episodes

def rename_series_files(show_name, episodes, mkv_files):
    """Rename MKV files based on series details using duration, size, and creation time."""
    unmatched_files = mkv_files.copy()
    matched_files = []

    print("\n🎯 Matching files...\n")

    for ep in episodes:
        potential_matches = []
        for offset in (-1, 0, 1):
            for f in unmatched_files:
                if f['duration'] == ep['duration'] + offset:
                    potential_matches.append(f)

        # Further narrow by file size if duplicates
        if len(potential_matches) > 1:
            sizes = [f['size'] for f in potential_matches]
            unique_sizes = list(set(sizes))
            if len(unique_sizes) < len(potential_matches):  # Some same size
                size_counts = {s: sizes.count(s) for s in unique_sizes}
                least_common_size = min(size_counts, key=size_counts.get)
                potential_matches = [f for f in potential_matches if f['size'] == least_common_size]

        # If still multiple, sort by creation time
        potential_matches = sorted(potential_matches, key=lambda x: x['created'])

        if potential_matches:
            matched_file = potential_matches[0]
            unmatched_files.remove(matched_file)
            matched_files.append((ep, matched_file))
        else:
            print(f"❌ No match for: S{ep['season']:02}E{ep['episode']:02} - {ep['title']}")

    # Perform renames
    for ep, file_info in matched_files:
        folder = os.path.dirname(file_info['filename'])
        if ep['type'] == 'episode':
            new_name = f"{show_name} - S{ep['season']:02}E{ep['episode']:02} - {sanitize_filename(ep['title'])}.mkv"
        else:
            new_name = f"Season {ep['season']} - {sanitize_filename(ep['title'])}{ep['suffix']}.mkv"
        os.rename(file_info['filename'], os.path.join(folder, new_name))
        print(f"✅ Renamed: {file_info['original_name']} → {new_name}")

# Movie-specific functions

def get_video_resolution(disc_type):
    """Determine video resolution based on disc type."""
    if '4k' in disc_type.lower():
        return '4k'
    elif 'blu-ray' in disc_type.lower():
        return '1080p'
    elif 'dvd' in disc_type.lower():
        return '480p'
    return 'unknown'

def extract_movie_details(url):
    """Extract movie details from the provided DiscDB URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1').text.strip()
    year_match = re.search(r'\((\d{4})\)', title)
    year = year_match.group(1) if year_match else 'Unknown Year'
    discs = soup.find_all('div', class_='disc')
    return title, year, discs

def get_mkv_files(folder_path):
    """Retrieve a list of MKV files in the given directory."""
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith('.mkv')]

def rename_movie_files(movie_title, movie_year, discs, mkv_filenames):
    """Rename MKV files based on the movie details and disc information."""
    for disc in discs:
        disc_title = disc.find('h2').text.strip()
        disc_type = disc.find('span', class_='type').text.strip()
        resolution = get_video_resolution(disc_type)
        sanitized_title = sanitize_filename(disc_title)
        matching_files = [f for f in mkv_filenames if resolution in f.lower() and sanitized_title.lower() in f.lower()]

        if matching_files:
            for file in matching_files:
                folder = os.path.dirname(file)
                new_name = (
                    f"{movie_title} ({movie_year}) - {resolution} {sanitized_title}.mkv"
                    if len(matching_files) > 1 else
                    f"{movie_title} ({movie_year}) - {resolution}.mkv"
                )
                os.rename(file, os.path.join(folder, new_name))
                print(f"Renamed: {os.path.basename(file)} -> {new_name}")
        else:
            print(f"No matching file found for: {disc_title}")

# Main function to determine if URL is for a series or movie and process accordingly
def main():
    url = input("Enter the DiscDB URL: ").strip()
    folder_path = input("Enter the full path to the folder containing the MKV files: ").strip()

    if not os.path.isdir(folder_path):
        print("❌ Invalid folder path.")
        return

    if '/series/' in url:
        show_name = extract_show_name(url)
        episodes = parse_discdb(url)
        mkv_files = get_mkv_durations(folder_path)
        print("\n📋 Episodes found on the website:")
        for ep in episodes:
            print(f"  S{ep['season']:02}E{ep['episode']:02} - {ep['title']} ({ep['duration']}s) [{ep['type']}]")

        print("\n🎞️ MKV durations found locally:")
        for f in mkv_files:
            print(f"  {f['original_name']} - {f['duration']}s - {f['size']} bytes")

        rename_series_files(show_name, episodes, mkv_files)

    elif '/movie/' in url:
        movie_title, movie_year, discs = extract_movie_details(url)
        mkv_files = get_mkv_files(folder_path)
        print("\n🎞️ Movie details found:")
        print(f"  Title: {movie_title} ({movie_year})")

        rename_movie_files(movie_title, movie_year, discs, mkv_files)
    else:
        print("❌ Invalid URL. Please provide a valid DiscDB series or movie URL.")

if __name__ == "__main__":
    main()
