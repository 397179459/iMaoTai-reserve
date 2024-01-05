import subprocess

def display_menu():
    print("欢迎使用预约系统")
    print("1. 添加账号")
    print("2. 立即预约")
    print("其它. 退出程序")

def main():
    while True:
        display_menu()
        choice = input("请输入选项 (1/2): ")

        if choice == '1':
            # 使用 subprocess.call 调用 login.py
            subprocess.call(["python", "login.py"])
            # 登录结束后回到主菜单

        elif choice == '2':
            # 使用 subprocess.call 调用 main.py
            subprocess.call(["python", "main.py"])
            # 预约结束后回到主菜单

        else:
            print("程序已退出。")
            break

if __name__ == "__main__":
    main()
