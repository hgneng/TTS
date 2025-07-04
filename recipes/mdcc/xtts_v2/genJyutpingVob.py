def extract_characters(file_path, id):
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

def generate_cantonese_characters():
    # 常用汉字Unicode范围 (基本汉字U+4E00-U+9FFF)
    common_chinese_range = range(0x4E00, 0x9FFF + 1)

    # 扩展A区 (U+3400-U+4DBF) - 包含一些罕用汉字
    extended_a_range = range(0x3400, 0x4DBF + 1)

    # 粤语专用字符（示例，非完整列表）
    cantonese_specific_chars = [
        '嘅', '嘢', '乜', '咁', '哋', '冇', '谂', '喺', '嘞', '嘥',
        '嗰', '啲', '咪', '梗', '噉', '系', '喎', '噃', '咩', '嚟',
        '掂', '㗎', '嘞', '啱', '冚', '抌', '踎', '瞓', '氹', '晏',
        '拗', '掟', '揩', '嗌', '攞', '摞', '捱', '啲', '奀', '拎',
    ]

    # 生成器函数：逐个生成字符
    def character_generator():
        # 生成常用汉字
        for code_point in common_chinese_range:
            yield chr(code_point)

        # 生成扩展A区汉字（可选，因为包含很多罕用字）
        # for code_point in extended_a_range:
        #     yield chr(code_point)

        # 生成粤语专用字符
        for char in cantonese_specific_chars:
            yield char

    return character_generator()

# 输出到控制台或文件
if __name__ == "__main__":
    id = 41;
    # 输出到控制台
    # for char in generate_cantonese_characters():
    #     print(char)

    # 输出到文件
    with open('cantonese_chars.txt', 'w', encoding='utf-8') as f:
        for char in generate_cantonese_characters():
            f.write('"' + char + '": ' + str(id) + ',\n')
            id += 1

    extract_characters('jyutping_phon_list.txt', id)
    print("粤语字符集已生成到 cantonese_chars.txt")

