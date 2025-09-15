import os
import librosa
from typing import List

def get_audio_duration(file_path: str) -> float:
    """
    计算单个音频文件的时长（单位：秒）
    :param file_path: 音频文件路径
    :return: 时长（秒），若文件无效返回 -1
    """
    try:
        # 加载音频（仅读取元数据，不加载完整波形，提高效率）
        # sr=None 保留原始采样率，避免重采样导致时长计算误差
        _, sr = librosa.load(file_path, sr=None, mono=False)
        # 获取音频总采样数，时长 = 总采样数 / 采样率
        duration = librosa.get_duration(path=file_path, sr=sr)
        return round(duration, 2)  # 保留两位小数
    except Exception as e:
        # 捕获非音频文件、损坏文件、格式不支持等异常
        print(f"⚠️  跳过无效文件 {file_path}：{str(e)[:50]}")  # 打印异常前50字符，避免输出过长
        return -1

def calculate_average_audio_length(folder_path: str, supported_extensions: List[str] = None) -> None:
    """
    统计目录中所有音频文件的平均时长
    :param folder_path: 目标目录路径
    :param supported_extensions: 支持的音频格式（默认：MP3、WAV、FLAC、M4A）
    """
    # 默认支持的音频格式（不区分大小写）
    if supported_extensions is None:
        supported_extensions = [".mp3", ".wav", ".flac", ".m4a", ".ogg"]
    
    # 存储所有有效音频的时长
    durations = []
    # 遍历目录下所有文件（不递归子目录，若需递归可改用 os.walk）
    for filename in os.listdir(folder_path):
        # 获取文件后缀（转为小写，避免格式大小写问题）
        file_ext = os.path.splitext(filename)[1].lower()
        # 跳过非支持格式的文件
        if file_ext not in supported_extensions:
            continue
        
        # 拼接完整文件路径
        file_path = os.path.join(folder_path, filename)
        # 计算文件时长
        duration = get_audio_duration(file_path)
        # 仅保留有效时长（排除异常文件）
        if duration > 0:
            durations.append(duration)
            print(f"✅ {filename}: {duration} 秒")  # 实时打印单个文件时长

    # 计算并输出统计结果
    if not durations:
        print("\n❌ 未找到有效音频文件")
        return
    
    total_files = len(durations)
    total_duration = sum(durations)
    average_duration = total_duration / total_files

    # 格式化输出（转换为 分:秒 格式，更直观）
    def format_time(seconds: float) -> str:
        minutes = int(seconds // 60)
        secs = round(seconds % 60, 2)
        return f"{minutes}分{secs}秒" if minutes > 0 else f"{secs}秒"

    print("\n" + "="*50)
    print(f"📊 音频文件统计结果")
    print(f"总文件数：{total_files} 个")
    print(f"总时长：{format_time(total_duration)}（{total_duration:.2f} 秒）")
    print(f"平均时长：{format_time(average_duration)}（{average_duration:.2f} 秒）")
    print(f"最长时长：{format_time(max(durations))}（{max(durations):.2f} 秒）")
    print(f"最短时长：{format_time(min(durations))}（{min(durations):.2f} 秒）")
    print("="*50)

if __name__ == "__main__":
    # 替换为你的音频目录路径（绝对路径或相对路径均可）
    TARGET_FOLDER = "./mdcc-dataset/audio"  # 示例：你的训练数据音频目录
    
    # 检查目录是否存在
    if not os.path.isdir(TARGET_FOLDER):
        print(f"❌ 目录不存在：{TARGET_FOLDER}")
    else:
        calculate_average_audio_length(TARGET_FOLDER)
