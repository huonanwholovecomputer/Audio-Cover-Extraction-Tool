import os
import time
from mutagen import File
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.asf import ASF

def extract_cover(audio_path, output_dir):
    # 根据文件扩展名选择合适的音频处理类
    audio = None
    if audio_path.endswith('.mp3'):
        audio = MP3(audio_path, ID3=ID3)
    elif audio_path.endswith('.flac'):
        audio = FLAC(audio_path)
    elif audio_path.endswith('.m4a') or audio_path.endswith('.mp4'):
        audio = MP4(audio_path)
    elif audio_path.endswith('.wma'):
        audio = ASF(audio_path)
    
    if audio is None:
        print(f"×× 不支持的音频文件格式: {audio_path}")
        return

    # 提取封面图片
    if isinstance(audio, MP3):
        tags = audio.tags.values()
    elif isinstance(audio, FLAC):
        tags = audio.pictures
    elif isinstance(audio, MP4):
        tags = audio.tags.get('covr', [])
    elif isinstance(audio, ASF):
        tags = audio.pictures

    for tag in tags:
        if (isinstance(audio, MP3) and tag.FrameID == "APIC") or \
           (isinstance(audio, FLAC) and tag.type == 3) or \
           (isinstance(audio, MP4) and tag.image_type == 1) or \
           (isinstance(audio, ASF) and tag.type == 3):
            cover_data = tag.data if isinstance(audio, MP3) else tag
            output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(audio_path))[0] + ".jpg")
            with open(output_path, "wb") as img:
                img.write(cover_data)
            print(f"√ 封面图片已提取到 {output_path}")
            return
    print(f"× 未找到封面图片: {audio_path}")

def main():
    # 获取当前工作目录
    current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, "提取到的封面图片")
    os.makedirs(output_dir, exist_ok=True)

    # 标志是否找到任何音频文件
    found_audio = False

    # 遍历当前目录的所有文件
    for file in os.listdir(current_dir):
        if file.endswith(('.mp3', '.flac', '.m4a', '.mp4', '.wma')) and os.path.isfile(file):
            found_audio = True
            audio_path = os.path.join(current_dir, file)
            extract_cover(audio_path, output_dir)

    if not found_audio:
        print("未找到任何音频文件......")

if __name__ == "__main__":
    main()
    time.sleep(1)
    print("\n程序将在两秒后退出......")
    time.sleep(2)
