def extract_characters(file_path):
    id = 41;
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()  # 去除首尾空白字符
                if ':' in line and '7' not in line:
                    char_part = line.split(':', 1)[0]
                    print('"' + char_part + '": ' + str(id) + ",")
                    id += 1;
    except FileNotFoundError:
        print(f"错误：找不到文件 '{file_path}'")
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == "__main__":
    file_path = 'jyutping_phon_list.txt'  # 修改为实际文件路径
    extract_characters(file_path)