import requests
import re
import os
import subprocess

# 定义一个伪装成Chrome的User-Agent
CHROME_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

def download_file(url, filename):
    """下载文件并检查是否成功，伪装成Chrome浏览器"""
    headers = {"User-Agent": CHROME_USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查HTTP状态码
        with open(filename, 'wb') as f:
            f.write(response.content)
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            print(f"成功下载文件: {filename}")
            return True
        else:
            print(f"错误：文件 {filename} 下载后为空或不存在")
            return False
    except requests.RequestException as e:
        print(f"下载文件 {url} 失败: {str(e)}")
        return False

def extract_key_info(m3u8_content):
    """从m3u8文件中提取key的URI"""
    try:
        key_line = re.search(r'#EXT-X-KEY:METHOD=AES-128,URI="([^"]+)"', m3u8_content)
        if key_line:
            return key_line.group(1)
        else:
            print("错误：未能在m3u8文件中找到密钥信息")
            return None
    except Exception as e:
        print(f"解析m3u8文件时出错: {str(e)}")
        return None

def run_command_with_output(command):
    """执行命令并实时输出日志"""
    print(f"执行命令: {command}")
    try:
        # 使用Popen实时获取输出
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 实时读取标准输出和标准错误
        while True:
            stdout_line = process.stdout.readline()
            stderr_line = process.stderr.readline()
            
            if stdout_line:
                print(stdout_line, end='')  # 实时输出标准输出
            if stderr_line:
                print(stderr_line, end='')  # 实时输出标准错误
            
            # 检查进程是否结束
            if process.poll() is not None and not stdout_line and not stderr_line:
                break
        
        # 获取最终返回码
        return_code = process.wait()
        if return_code == 0:
            print("N_m3u8DL-RE 执行成功")
        else:
            print(f"N_m3u8DL-RE 执行失败，返回码: {return_code}")
        return return_code == 0
    except Exception as e:
        print(f"执行N_m3u8DL-RE时出错: {str(e)}")
        return False

def main():
    # 获取用户输入的链接
    m3u8_url = input("请输入m3u8链接: ").strip()
    print(f"您输入的链接是: {m3u8_url}")

    # 步骤1：下载m3u8文件
    m3u8_filename = "temp.m3u8"
    if not download_file(m3u8_url, m3u8_filename):
        print("步骤1失败：无法下载m3u8文件，程序退出")
        return

    # 读取m3u8文件内容
    try:
        with open(m3u8_filename, 'r', encoding='utf-8') as f:
            m3u8_content = f.read()
        print("成功读取m3u8文件内容")
        print("文件开头内容如下:")
        print('\n'.join(m3u8_content.splitlines()[:5]))  # 显示前5行
    except Exception as e:
        print(f"错误：读取m3u8文件失败: {str(e)}")
        print("程序退出")
        return

    # 步骤2：提取密钥文件名并构建新链接
    key_filename = extract_key_info(m3u8_content)
    if not key_filename:
        print("步骤2失败：无法提取密钥信息，程序退出")
        return

    # 构建密钥文件的完整URL
    base_url = m3u8_url.rsplit('/', 1)[0]  # 获取URL的目录部分
    key_url = f"{base_url}/{key_filename}"
    print(f"构建的密钥文件URL: {key_url}")

    # 步骤3：下载密钥文件
    if not download_file(key_url, key_filename):
        print("步骤3失败：无法下载密钥文件，程序退出")
        return

    # 步骤4：执行N_m3u8DL-RE命令并实时输出
    command = f'./N_m3u8DL-RE "{m3u8_url}" --key-text-file "{key_filename}"'
    if not run_command_with_output(command):
        print("步骤4失败：N_m3u8DL-RE执行未成功完成")

    # 清理临时文件（可选）
    try:
        os.remove(m3u8_filename)
        print(f"已删除临时文件: {m3u8_filename}")
    except:
        pass

    # 等待用户输入退出
    input("按回车键退出程序...")

if __name__ == "__main__":
    main()
