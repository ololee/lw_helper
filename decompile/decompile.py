from calendar import c
from singleton import singleton
from decompile.cmd.CMD_utils import CMD_utils
from decompile.ScriptExporter import extractFiles
from decompile.lua.XLuac2NormalLuac import xlua2NormalLua
from decompile.lua.Luac2XLuac import luac2XLuac
from cache_handler import save_to_cache, get_from_cache
from decompile.ScriptImporter import compressFiles
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
        self.export_dir = os.path.join(cur_path,"decompile","export")
        self.export_out_dir = os.path.join(self.export_dir,"output")
        if not os.path.exists(self.export_out_dir): 
            os.makedirs(self.export_out_dir)
        self.lw_version = None
        self.local_luac_path = None
        self.normal_unlua_jar_path = os.path.join(self.decompile_path,"unluac_2020_05_28.jar")
        self.luac_exe_path = os.path.join(self.decompile_path,"luac.exe")
        self.saved_decompile_file_path = None
    
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
        save_to_cache("Last_Pulled_LW_BIN_PATH",os,path.join(local_ver_dir,"LWScripts.data"))
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
            extractFiles(self.export_out_dir,lw_scripts,progress_callback)

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
        lua_name = local_lua_path.split("/")[-1].replace(".lua",".luac")
        self.get_version()
        local_luac_output_dir = rf"{self.from_sd_dir}/{self.lw_version}/output/luac"
        if not os.path.exists(local_luac_output_dir):
            os.makedirs(local_luac_output_dir)
        local_xluac_output_dir = rf"{self.from_sd_dir}/{self.lw_version}/output/xluac"
        if not os.path.exists(local_xluac_output_dir):
            os.makedirs(local_xluac_output_dir)
        output_path = rf"{local_luac_output_dir}/{lua_name}"
        output_xluac_path = rf"{local_xluac_output_dir}/{lua_name}"
        self.output_normal_luac = output_path
        cmd = f"{self.luac_exe_path} -o {output_path} {local_lua_path}"
        result,err,_= CMD_utils.execute_cmd(cmd)
        if err != None and err != "":
            return {
                "error": err,
                "task_id":6,
                "status":"task_failed"
            }
        with open(output_path,'rb') as reader:
            luac_bytes = reader.read()
            xluac_bytes = luac2XLuac(luac_bytes)
            with open(output_xluac_path,'wb') as writer:
                writer.write(xluac_bytes)
        
        local_uuid = self.string_to_uuid(output_xluac_path)
        save_to_cache(local_uuid,output_xluac_path)
        save_to_cache("LAST_MODIFIED_AND_GEND_XLUAC",output_xluac_path)
        return {
            "task_id":6,
            "output_xluac_path":output_xluac_path,
            "token":local_uuid,
            "status":"task_completed"
        }

    def save_file(self,save_file_path):
        if not os.path.exists(save_file_path):
            return {
                "task_id":3,
                "status":"task_failed",
                "message":"文件不存在",
                "error": "file not exists"
            }
        save_to_cache("SAVED_DECOMPILE_FILE_PATH",save_file_path)
        self.saved_decompile_file_path = save_file_path
        lua_name = save_file_path.split("/")[-1]
        with open(save_file_path,"rb") as f:
            xluac = f.read()
            self.castXLuac2Lua(lua_name,xluac)
        return {
            "error":None,
            "task_id":3,
            "status":"task_completed",
            "message":"保存成功"
        }
    
    def get_saved_file_path(self) -> str:
        if self.saved_decompile_file_path == None or self.saved_decompile_file_path == "":
            self.saved_decompile_file_path = get_from_cache("SAVED_DECOMPILE_FILE_PATH")
        return self.saved_decompile_file_path
    
    def string_to_uuid(self,input_str: str) -> uuid.UUID:
        # 使用 UUID 命名空间（例如 uuid.NAMESPACE_DNS 或自定义）
        namespace = uuid.NAMESPACE_DNS  # 或 uuid.NAMESPACE_URL 等
        uuid_ret = uuid.uuid5(namespace, input_str)
        return str(uuid_ret).replace("-","_")

    def replace_origin_file(self):
        origin_file_path = self.get_saved_file_path()
        modified_xluac_path = get_from_cache("LAST_MODIFIED_AND_GEND_XLUAC")
        if not os.path.exists(origin_file_path):
            return {
                "task_id": 7,
                "status": "task_failed",
                "error": f"原始文件不存在，请检查文件路径是否正确{origin_file_path}",
                "message": "原始文件不存在，请检查文件路径是否正确。"
            }
        if not os.path.exists(modified_xluac_path):
            return {
                "task_id": 7,
                "status": "task_failed",
                "error": f"修改后的文件不存在，请检查文件路径是否正确{modified_xluac_path}",
                "message": "修改后的文件不存在，请检查文件路径是否正确。"
            }
        with open(origin_file_path,"wb") as w:
            with open(modified_xluac_path,"rb") as r:
                w.write(r.read())
        return {
            "status": "task_completed",
            "message": "替换成功",
            "task_id": 7
        }

    def check_file_valied(self,desc,file_path):
        if file_path == None or file_path == "":
            raise Exception(f"{desc} 为空")
        if not os.path.exists(file_path):
            raise Exception(f"{desc} 不存在")
        
    
    def getModifiedPackFiles(self,folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
        binFile = os.path.join(folder,"LWScripts.data")
        crcFile = os.path.join(folder,"LWScripts.txt")
        return binFile,crcFile

    def packFiles(self):
        try:
            self.check_file_valied("导出的文件夹",self.export_out_dir)
            bin_file = get_from_cache("Last_Pulled_LW_BIN_PATH")
            self.check_file_valied("LWScripts.data",bin_file)
            self.get_version()
            self.out_put_pack_folder = os.path.join(self.from_sd_dir,self.lw_version,"pack")
            save_to_cache("MODIFIED_LW_FOLDER",self.out_put_pack_folder)
            out_bin,out_crc = self.getModifiedPackFiles(self.out_put_pack_folder)
            compressFiles(self.out_put_pack_folder,bin_file,out_bin,out_crc)
        except Exception as e:
            return {
                "status": "task_failed",
                "message": str(e),
                "task_id": 8
            }
        return {
            "status": "task_completed",
            "message": "Pack files successfully",
            "task_id": 8
        }

    def uploadResult(self):
        try:
            task_id = 9
            out_put_folder = get_from_cache("MODIFIED_LW_FOLDER")
            self.check_file_valied("打包的文件夹",out_put_folder)
            input_bin,input_crc = self.getModifiedPackFiles(out_put_folder)
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
            cmd = rf"{self.adb_path} push {input_bin} /sdcard/Android/data/com.fun.lastwar.gp/files/lwScripts/"
            result,err,_ = CMD_utils.execute_cmd(cmd)
            if err != None or err != "":
                return {
                    "status": "task_failed",
                    "error": "adb push bin失败",
                    "task_id": task_id
                }
            cmd = rf"{self.adb_path} push {input_crc} /sdcard/Android/data/com.fun.lastwar.gp/files/lwScripts/"
            result,err,_ = CMD_utils.execute_cmd(cmd)
            if err != None or err != "":
                return {
                    "status": "task_failed",
                    "error": "adb push crc失败",
                    "task_id": task_id
                }
        except Exception as e:
            return {
                "status": "task_failed",
                "message": str(e),
                "task_id": 9,
                "error":"上传失败"
            }
        return {
            "status": "task_success",
            "message": "上传成功",
            "task_id": 9
        }
       



        
    
    
        