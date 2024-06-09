
def set_default_value(input_value, default_content):
    """
    检查输入内容是否为空，如果为空则返回默认内容。

    :param input_value: 需要检查的内容
    :param default_content: 如果输入为空，返回的默认内容
    :return: 输入内容或默认内容
    """
    return default_content if input_value is None or input_value.strip() == "" else input_value

def main():
    a = set_default_value("", 999)
    b = set_default_value("  ", 88)
    c = set_default_value("435435", 999)
    print(a, b, c)

if __name__ == '__main__':
    main()
