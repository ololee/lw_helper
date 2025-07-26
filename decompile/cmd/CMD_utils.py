import subprocess

class CMD_utils:

    @staticmethod
    def execute_cmd(command: str) -> tuple[str, str, int]:
        """
        执行 Windows 命令行命令并返回结果

        Args:
            command: 要执行的命令

        Returns:
            包含标准输出、标准错误和返回代码的元组
        """
        print(command)
        try:
            # 创建一个新的进程执行命令
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='gbk'  # Windows 命令行默认编码
            )
            
            # 等待命令执行完成并获取输出
            stdout, stderr = process.communicate()
            return_code = process.returncode
            
            return stdout, stderr, return_code
            
        except Exception as e:
            print(f"执行命令时发生错误: {str(e)}")
            return "", str(e), 1
    