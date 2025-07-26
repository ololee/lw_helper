from singleton import singleton
from decompile.cmd.CMD_utils import CMD_utils
import os




@singleton
class Decompiler:

    def __init__(self):
        cur_path = os.getcwd()
        print(cur_path)
        self.adb_path = os.path.join(cur_path,"adb","adb.exe")

    def check_adb(self):
        devices,err,_ = CMD_utils.execute_cmd(rf"{self.adb_path} devices")
        print(err)
        return err == None or err == ""

    def pull_Lw_scripts(self):
        if not self.check_adb():
            return {
                "error": "未找到adb设备"
            }
        