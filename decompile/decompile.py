from calendar import c
from singleton import singleton
from decompile.cmd.CMD_utils import CMD_utils
from decompile.ScriptExporter import extractFiles
from decompile.lua.XLuac2NormalLuac import xlua2NormalLua
from cache_handler import save_to_cache, get_from_cache
import os
import json
import uuid

@singleton
class Decompiler:

    def __init__(self):
        cur_path = os.getcwd()
        self.adb_path = os.path.join(cur_path,"decompile","adb","adb.exe")
        self.decompile_path = os.path.join(cur_path,"decompile")
        self.from_sd_dir = os.path.join(cur_path,"decompile","from_sd")
        self.export_dir = os.path.join(cur_path,"export")
        self.lw_version = None
        self.local_luac_path = None
    
    def getExportDir(self):
        return self.export_dir

    def check_adb(self):
        devices,err,_ = CMD_utils.execute_cmd(rf"{self.adb_path} devices")
        return (err == None or err == "" ) and (len(devices) > 26)
    
    def check_lastwar(self):
        result,err,_ = CMD_utils.execute_cmd(rf"{self.adb_path} ls /sdcard/Android/data/com.fun.lastwar.gp/files/lwScripts")
        return (err == None or err == "" ) and (len(result) > 0)
    
    def get_LW_version(self):
        version,err,_ = CMD_utils.execute_cmd(rf"{self.adb_path} shell cat /sdcard/Android/data/com.fun.lastwar.gp/files/lwScripts/version.txt")
        return version
    
    def read_versions(self):
        self.version_list_file = rf"{self.from_sd_dir}/versions.json"
        if not os.path.exists(self.version_list_file):
            return []
        with open(self.version_list_file,"r",encoding="utf-8") as r:
            versions = json.load(r)
            return versions
        

    def write_versions(self,jsonArr):
        with open(self.version_list_file,"w",encoding="utf-8") as w:
            versions = json.dumps(jsonArr)
            w.write(versions)

    def pull_Lw_scripts(self,task_id):
        if not self.check_adb():
            return {
                "error": "未找到adb设备",
                "task_id": task_id
            }
        if not self.check_lastwar():
            return {
                "error": "未找到lastwar游戏目录",
                "task_id": task_id
            }
        self.lw_version = self.get_LW_version()
        local_ver_dir = rf"{self.from_sd_dir}/{self.lw_version}"
        if not os.path.exists(local_ver_dir):
            os.makedirs(local_ver_dir)
        result,err,_ = CMD_utils.execute_cmd(rf"{self.adb_path} pull /sdcard/Android/data/com.fun.lastwar.gp/files/lwScripts {local_ver_dir}")
        if err.find("3 files pulled") == -1:
            return {
                 "error": rf"拉取失败，请检查: {local_ver_dir} && error is :{err}",
                 "task_id": task_id
            }
        self.versions = self.read_versions()
        self.versions.append(self.lw_version)
        self.write_versions(self.versions)
        return {
            "success": True,
            "msg": "成功",
            "task_id":task_id,
            "status":"task_completed",
            "result":result
        }

    def unzipFiles(self,progress_callback):
        self.get_version()
        self.lsScriptDir = rf"{self.from_sd_dir}/{self.lw_version}/lwScripts"
        children = os.listdir(self.lsScriptDir)
        if len(children) >0:
            lw_scripts = rf"{self.lsScriptDir}/LWScripts.data"
            extractFiles(lw_scripts,progress_callback)

    def get_version(self):
        if self.lw_version == None:
           self.versions = self.read_versions()
           if self.versions != None and len(self.versions) != 0:
               self.versions.sort()
               self.lw_version = self.versions[-1]
            
        if self.lw_version == None:
            raise Exception("不存在版本号")
        return self.lw_version

    def castXLuac2Lua(self,fileName,xluac):
        self.get_version()
        luac = xlua2NormalLua(xluac)
        normal_luac_path = rf"{self.from_sd_dir}/{self.lw_version}/normal_luac"
        if not os.path.exists(normal_luac_path):
            os.makedirs(normal_luac_path)
        self.local_luac_path = rf"{normal_luac_path}/{fileName}"
        save_to_cache("LAST_LUAC",self.local_luac_path)
        with open(self.local_luac_path,'wb') as w:
            w.write(luac)
    

    def decompile(self):
        if self.local_luac_path == None:
            self.local_luac_path = get_from_cache("LAST_LUAC")
        
        if self.local_luac_path == None:
            return {
                "error": "不存在的luac文件",
                "task_id":4
            }
        self.local_luac_path = self.local_luac_path.replace("\\","/")
        lua_name = self.local_luac_path.split("/")[-1].replace(".luac",".lua")
        self.normal_unlua_jar_path = rf"{self.decompile_path}\unluac_2020_05_28.jar"
        cmd = rf"java -jar {self.normal_unlua_jar_path} {self.local_luac_path}"
        result,err,_ = CMD_utils.execute_cmd(cmd)
        if err != None and err != "":
            return {
                "error": rf"反编译失败，请检查: {err}",
                "task_id": 4
            }

        self.get_version()

        lua_parent = rf"{self.from_sd_dir}/{self.lw_version}/lua"
        if not os.path.exists(lua_parent):
            os.makedirs(lua_parent)
        
        self.normal_lua = rf"{lua_parent}/{lua_name}"

        with open(self.normal_lua,"w",encoding="utf-8") as w:
            w.write(result)
        
        save_to_cache("NORMAL_LUA",self.normal_lua)
        return {
            "task_id":4,
            "status":"task_completed",
            "lua_path": self.normal_lua
        }
        
    def getCode(self,lua_path):
        local_lua_path = lua_path
        if lua_path == None or lua_path == "":
            local_lua_path = get_from_cache("NORMAL_LUA")

        if local_lua_path == None or local_lua_path == "":
            return {
                "error":"lua文件为空或未指定",
                "task_id":5
            }
        
        if not os.path.exists(local_lua_path):
            return {
                "error":"lua路径不正确",
                "task_id":5
            }
        
        local_uuid = self.string_to_uuid(local_lua_path)
        save_to_cache(local_uuid,local_lua_path)
        return {
            "task_id":5,
            "status":"task_completed",
            "path":local_lua_path,
            "token":local_uuid
        }
    
    def getCodeByToken(self,token):
        if token == None or token == "":
            return {
                "error":"token为空或未指定"
            }
        code_path = get_from_cache(token)

        if code_path == None or code_path == "":
            return {
                "error":"未找到对应的代码文件"
            }
        content = ""
        with open(code_path,"r",encoding="utf-8") as r:
            content = r.read()
        
        code_path = code_path.replace("\\","\\\\").replace("/","\\\\")
        return {
            "content":content.replace("/","\\"),
            "path":code_path
        }

    def generate_luac(self):
        local_lua_path = get_from_cache("NORMAL_LUA")
        print(local_lua_path)

    
    def string_to_uuid(self,input_str: str) -> uuid.UUID:
        # 使用 UUID 命名空间（例如 uuid.NAMESPACE_DNS 或自定义）
        namespace = uuid.NAMESPACE_DNS  # 或 uuid.NAMESPACE_URL 等
        uuid_ret = uuid.uuid5(namespace, input_str)
        return str(uuid_ret).replace("-","_")

        
    
    
        