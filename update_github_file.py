import os
import requests
from github import Github, GithubException
import re

# --- KONFIGURASI ---
GITHUB_TOKEN = os.getenv('GITHUB_PAT')  # Ambil token dari environment variable
SOURCE_URL = "https://raw.githubusercontent.com/uppermoon77/lazyloxy/refs/heads/main/lazylazyloxy"
DEST_REPO = "uppermoon77/lazyloxy"  # Format: "username/repository"
DEST_FILE_PATH = "LX19OKTOBER2025"
COMMIT_MESSAGE = "Auto update: Sync playlist from source + footer update"
GIT_BRANCH = "main"

GITHUB_TOKEN = os.getenv('GITHUB_PAT')  # Ambil token dari environment variable
SOURCE_URL = "https://raw.githubusercontent.com/uppermoon77/lazyloxy/refs/heads/main/lazylazyloxy"
DEST_REPO = "uppermoon77/lazyloxy"  # Format: "username/repository"
DEST_FILE_PATH = "LX20OKTOBER2025"
COMMIT_MESSAGE = "Auto update: Sync playlist from source + footer update"
GIT_BRANCH = "main"

GITHUB_TOKEN = os.getenv('GITHUB_PAT')  # Ambil token dari environment variable
SOURCE_URL = "https://raw.githubusercontent.com/uppermoon77/lazyloxy/refs/heads/main/lazylazyloxy"
DEST_REPO = "uppermoon77/lazyloxy"  # Format: "username/repository"
DEST_FILE_PATH = "LX21OKTOBER2025"
COMMIT_MESSAGE = "Auto update: Sync playlist from source + footer update"
GIT_BRANCH = "main"

# --- KONSTANTA FOOTER ---
def generate_footer():
    """Buat footer dinamis sesuai nama file."""
    return f'#EXTM3U billed-msg="😎{DEST_FILE_PATH}| lynk.id/magelife😎"'

def clean_and_add_footer(content):
    """Hapus footer lama dan tambahkan yang baru."""
    # Hapus baris yang mengandung pola footer lama (kalimat dengan billed-msg)
    cleaned = re.sub(r'#EXTM3U billed-msg="[^"]+"', '', content).strip()
    # Tambahkan footer baru di akhir file dengan 2 baris kosong sebelum footer
    return f"{cleaned}\n\n{generate_footer()}\n"

def get_source_content():
    """Mengambil konten teks dari URL sumber."""
    try:
        print(f"Mengambil konten dari: {SOURCE_URL}...")
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        print("Konten berhasil diambil.")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengambil konten sumber: {e}")
        return None

def update_github_file():
    """Memperbarui file di repositori GitHub tujuan."""
    if not GITHUB_TOKEN:
        print("Error: GITHUB_PAT environment variable belum diatur. Script tidak bisa berjalan.")
        return

    new_content = get_source_content()
    if new_content is None:
        return

    # Tambahkan footer baru (hapus lama)
    new_content = clean_and_add_footer(new_content)

    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(DEST_REPO)
        print(f"Berhasil terhubung ke repositori: {DEST_REPO}")

        try:
            contents = repo.get_contents(DEST_FILE_PATH, ref=GIT_BRANCH)
            sha = contents.sha
            old_content = contents.decoded_content.decode('utf-8')

            # Hapus footer lama dari konten lama juga untuk perbandingan akurat
            cleaned_old = re.sub(r'#EXTM3U billed-msg="[^"]+"', '', old_content).strip()

            if cleaned_old == new_content.strip():
                print("Konten sudah yang terbaru. Tidak ada pembaruan yang diperlukan.")
                return
        except GithubException as e:
            if e.status == 404:
                print(f"File '{DEST_FILE_PATH}' tidak ditemukan. Akan membuat file baru.")
                repo.create_file(DEST_FILE_PATH, COMMIT_MESSAGE, new_content, branch=GIT_BRANCH)
                print("File baru berhasil dibuat di GitHub.")
                return
            else:
                raise

        print(f"Mencoba memperbarui file '{DEST_FILE_PATH}'...")
        repo.update_file(contents.path, COMMIT_MESSAGE, new_content, sha, branch=GIT_BRANCH)
        print("Pembaruan file berhasil di-commit ke GitHub!")

    except GithubException as e:
        print(f"Error pada API GitHub: {e}")
    except Exception as e:
        print(f"Terjadi error yang tidak terduga: {e}")

if __name__ == "__main__":
    update_github_file()
