# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
import os
import shutil
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

class FileHelper:
    """ Различные утилитки работы с файлами """
    
    @staticmethod
    def save_data_to_file(file_name : str, data : bytearray, len0_ : int=-1) -> None:
        """ Сохранение данных в файле
        
        Args:
            file_name(str): имя файла
            data(bytearray): сохраняемая последовательсноть байт
        """
        if (data is None): 
            return
        f = None
        try: 
            f = FileStream(file_name, "wb")
            f.write(data, 0, (len(data) if len0_ < 0 else len0_))
        finally: 
            if (f is not None): 
                f.close()
    
    @staticmethod
    def load_data_from_file(file_name : str, attampts : int=0) -> bytearray:
        """ Получить последовательность байт из файла.
        
        Args:
            file_name(str): имя файла
            attampts(int): число попыток с небольшой задержкой
        
        Returns:
            bytearray: последовательнсоть байт, null, если файл пусто
        """
        f = None
        buf = None
        try: 
            ex = None
            i = 0
            while i <= attampts: 
                try: 
                    f = FileStream(file_name, "rb")
                    break
                except Exception as e0_: 
                    ex = e0_
                if (i == 0 and not pathlib.Path(file_name).is_file()): 
                    break
                i += 1
            if (f is None): 
                raise ex
            if (f.length == (0)): 
                return None
            buf = Utils.newArrayOfBytes(f.length, 0)
            f.read(buf, 0, f.length)
        finally: 
            if (f is not None): 
                f.close()
        return buf
    
    @staticmethod
    def is_file_exists(pattern : str) -> bool:
        """ Проверка существования файла по его имени или шаблону (типа *.*).
        Если файл существует и в него кто-то сейчас записывает, то ожидать конца записи.
        
        Args:
            pattern(str): 
        
        """
        if (Utils.isNullOrEmpty(pattern)): 
            return False
        try: 
            dir0_ = pathlib.PurePath(pattern).parent.absolute()
            if (dir0_ is None): 
                raise Exception("Невозможно определить папку для пути '" + pattern + "'")
            name = pattern[len(dir0_):]
            if (name[0] == '\\'): 
                name = name[1:]
            files = [os.path.abspath(x) for x in os.listdir(os.path.join(dir0_, name)) if os.path.isfile(os.path.join(dir0_, f))]
            if (len(files) > 0): 
                if (len(files) == 1): 
                    return FileHelper.check_file_ready(files[0])
                return True
        except Exception as ex2710: 
            pass
        return False
    
    @staticmethod
    def copy_file_to_folder(source_file_path : str, destination_folder : str) -> str:
        """ Метод копирования файла в папку назначения с изменением имени файла на уникальной.
        
        Args:
            source_file_path(str): Путь к исходному файлу
            destination_folder(str): Папка назначения
        
        Returns:
            str: Полный путь куда скопирован файл
        """
        file_name = Utils.getFilenameWithoutExt(source_file_path)
        file_ext = pathlib.PurePath(source_file_path).suffix
        if (Utils.isNullOrEmpty(file_name)): 
            raise Exception("Исходный путь не содержит имени файла. Путь'" + source_file_path + "'")
        if (not pathlib.Path(destination_folder).is_dir()): 
            raise Exception("Папка назначения отсутствует.\nПапка назначения'" + destination_folder + "'")
        destination_path = pathlib.PurePath(destination_folder).joinpath(file_name + file_ext)
        i = 1
        while pathlib.Path(destination_path).is_file():
            destination_path = pathlib.PurePath(destination_folder).joinpath((file_name + "_" + (chr(i))) + file_ext)
            i += 1
        shutil.copy(source_file_path, destination_path)
        return destination_path
    
    @staticmethod
    def check_file_ready(file_name : str) -> bool:
        """ Проверка, что файл существует и в него никто не пишет.
        А если пишет, то дождаться окончания записи.
        
        Args:
            file_name(str): 
        
        """
        ok = False
        while True:
            try: 
                with FileStream(file_name, "r+b") as f: 
                    ok = True
                    break
            except Exception as ex2711: 
                pass
            if (not pathlib.Path(file_name).is_file()): 
                break
        return ok
    
    @staticmethod
    def remove(path : str, remove_root : bool=True) -> bool:
        """ Удаление объекта\объектов
        
        Args:
            path(str): файл, шаблон или директория
            remove_root(bool): удалять ли саму директорию (при false только очистка)
        
        """
        ret = True
        fnames = None
        try: 
            fnames = [os.path.abspath(x) for x in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        except Exception as ex2712: 
            pass
        if (fnames is not None): 
            for f in fnames: 
                try: 
                    pathlib.Path(f).unlink()
                except Exception as ex: 
                    ret = False
        dirs = None
        try: 
            dirs = [os.path.abspath(x) for x in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        except Exception as ex2713: 
            pass
        if (dirs is not None): 
            for d in dirs: 
                FileHelper.remove(d, True)
        if (pathlib.Path(path).is_dir() and remove_root): 
            try: 
                shutil.rmtree(path, ignore_errors=True)
                ret = True
            except Exception as ex: 
                ret = False
        return ret
    
    @staticmethod
    def create_full_path(path : str) -> bool:
        """ Создание дорожки
        
        Args:
            path(str): 
        
        """
        if (Utils.isNullOrEmpty(path)): 
            return False
        parts = Utils.splitString(path, '\\', False)
        if (parts is None or (len(parts) < 1)): 
            return False
        dir0_ = parts[0]
        try: 
            if (len(dir0_) == 2 and dir0_[1] == ':'): 
                pass
            elif (not pathlib.Path(dir0_).is_dir()): 
                pathlib.Path(dir0_).mkdir(exist_ok=True)
            i = 1
            while i < len(parts): 
                if (len(dir0_) == 2 and dir0_[1] == ':'): 
                    dir0_ += ("\\" + parts[i])
                else: 
                    dir0_ = pathlib.PurePath(dir0_).joinpath(parts[i])
                if (not pathlib.Path(dir0_).is_dir()): 
                    pathlib.Path(dir0_).mkdir(exist_ok=True)
                i += 1
            return True
        except Exception as ex: 
            return False
    
    @staticmethod
    def copy_directory(src : str, dst : str) -> None:
        if (not pathlib.Path(dst).is_dir()): 
            pathlib.Path(dst).mkdir(exist_ok=True)
        for f in [os.path.abspath(x) for x in os.listdir(src) if os.path.isfile(os.path.join(src, f))]: 
            shutil.copy(f, pathlib.PurePath(dst).joinpath(pathlib.PurePath(f).name))
        for d in [os.path.abspath(x) for x in os.listdir(src) if os.path.isdir(os.path.join(src, f))]: 
            FileHelper.copy_directory(d, pathlib.PurePath(dst).joinpath(pathlib.PurePath(d).name))
    
    @staticmethod
    def write_string_to_file(str0_ : str, file_name : str) -> None:
        """ Сохранение текста в файл. Формат UTF-8, вставляется префикс EF BB BF.
        
        Args:
            str0_(str): 
            file_name(str): 
        """
        if (str0_ is None): 
            str0_ = ""
        data = str0_.encode("UTF-8", 'ignore')
        pream = Utils.preambleCharset("UTF-8")
        if (len(data) > len(pream)): 
            i = 0
            i = 0
            while i < len(pream): 
                if (pream[i] != data[i]): 
                    break
                i += 1
            if (i >= len(pream)): 
                pream = (None)
        if (len(str0_) == 0): 
            pream = (None)
        fstr = None
        try: 
            fstr = FileStream(file_name, "wb")
            if (pream is not None): 
                fstr.write(pream, 0, len(pream))
            fstr.write(data, 0, len(data))
        finally: 
            if (fstr is not None): 
                fstr.close()