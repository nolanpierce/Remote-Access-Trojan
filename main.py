import os
import shutil
from pathlib import Path
import glob

downloads_dir = Path.home() / 'Downloads'
desktop_dir = Path.home() / 'Desktop'
downloads = str(downloads_dir)
desktop = str(desktop_dir)

downloads_files = glob.glob(f'{downloads}/*')
desktop_files = glob.glob(f'{desktop}/*')

# Sort our epubs so we can move them elsewhere before deleting
epubs = [file for file in downloads_files if file.endswith('.epub')]

# Make our books directory if it doesn't exist
books_dir = desktop_dir / 'books'
os.makedirs(books_dir, exist_ok=True)

# Move each epub file to the books directory
for epub in epubs:
    shutil.move(epub, books_dir)
