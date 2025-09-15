import csv
import os

def filter_audio_by_duration(input_csv_path: str, output_csv_path: str, min_duration: float = 2.0) -> None:
    """
    读取输入CSV文件，筛选出duration≥min_duration的记录，保存到输出CSV文件
    :param input_csv_path: 输入CSV文件路径（原始metadata文件）
    :param output_csv_path: 输出CSV文件路径（筛选后的新文件）
    :param min_duration: 最小音频时长（默认2秒）
    """
    # 1. 检查输入文件是否存在
    if not os.path.isfile(input_csv_path):
        print(f"❌ 输入文件不存在：{input_csv_path}")
        return

    # 2. 初始化统计变量
    total_records = 0  # 总记录数
    kept_records = 0   # 保留的记录数（≥2秒）
    skipped_records = 0# 跳过的记录数（<2秒或格式错误）
    skipped_details = []# 跳过的记录详情（用于排查）

    # 3. 读取输入CSV并筛选
    with open(input_csv_path, mode='r', encoding='utf-8', newline='') as input_file:
        # 用csv.DictReader读取，按表头字段访问数据（避免依赖列顺序）
        csv_reader = csv.DictReader(input_file)
        
        # 检查表头是否包含必需的字段
        required_columns = ['audio_path', 'text_path', 'sex', 'duration']
        for col in required_columns:
            if col not in csv_reader.fieldnames:
                print(f"❌ 输入CSV缺少必需字段：{col}，表头应为：{required_columns}")
                return

        # 4. 写入筛选后的记录到输出CSV
        with open(output_csv_path, mode='w', encoding='utf-8', newline='') as output_file:
            # 保持与输入相同的表头
            csv_writer = csv.DictWriter(output_file, fieldnames=csv_reader.fieldnames)
            csv_writer.writeheader()  # 写入表头

            # 逐行处理记录
            for row_num, row in enumerate(csv_reader, start=2):  # row_num从2开始（跳过表头行）
                total_records += 1
                audio_path = row['audio_path']
                duration_str = row['duration'].strip()

                # 验证duration字段是否为有效数字
                try:
                    duration = float(duration_str)
                except ValueError:
                    # duration格式错误（非数字），跳过该记录
                    skipped_records += 1
                    skipped_details.append(f"第{row_num}行：duration格式错误（{duration_str}），音频路径：{audio_path}")
                    continue

                # 筛选出≥min_duration的记录
                if duration >= min_duration:
                    csv_writer.writerow(row)
                    kept_records += 1
                else:
                    skipped_records += 1
                    skipped_details.append(f"第{row_num}行：时长不足（{duration:.2f}秒 < {min_duration}秒），音频路径：{audio_path}")

    # 5. 输出处理结果
    print("=" * 60)
    print(f"📊 CSV文件筛选完成！")
    print(f"输入文件：{input_csv_path}")
    print(f"输出文件：{output_csv_path}")
    print(f"总记录数：{total_records}")
    print(f"保留记录数（≥{min_duration}秒）：{kept_records}")
    print(f"跳过记录数（<{min_duration}秒或格式错误）：{skipped_records}")
    
    # 可选：打印跳过的记录详情（便于排查短音频）
    if skipped_details:
        print(f"\n⚠️  跳过的记录详情（前10条，共{len(skipped_details)}条）：")
        for detail in skipped_details[:10]:
            print(f"  {detail}")
        if len(skipped_details) > 10:
            print(f"  ... 还有{len(skipped_details)-10}条跳过记录未显示")
    print("=" * 60)

if __name__ == "__main__":
    # --------------------------
    # 请根据你的文件路径修改以下参数
    # --------------------------
    INPUT_CSV = "mdcc-dataset/cnt_asr_train_metadata.csv"  # 原始输入CSV路径
    OUTPUT_CSV = "mdcc-dataset/train.csv"                  # 筛选后输出CSV路径
    MIN_DURATION = 2.0                          # 最小音频时长（2秒）

    # 执行筛选
    filter_audio_by_duration(INPUT_CSV, OUTPUT_CSV, MIN_DURATION)
