#!/usr/bin/env python3
"""
Dodge Game 打包构建脚本
版本: 1.05
作者: Find 1134
"""

import os
import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

class GameBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.build_dir = self.project_root / "build"
        self.dist_dir = self.project_root / "dist"
        self.release_dir = self.project_root / "releases"
        
        # 游戏配置
        self.game_name = "DodgeGame"
        self.main_script = "src/main.py"
        self.icon_file = "game_icon.ico"
        self.version = "1.05"
        
        # 资源文件配置
        self.asset_dirs = ["assets", "sounds"]
        
    def print_header(self):
        """打印构建头部信息"""
        print("🚀" * 50)
        print(f"🎮 {self.game_name} 游戏打包工具")
        print(f"📦 版本: {self.version}")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🚀" * 50)
        print()
        
    def check_environment(self):
        """检查构建环境"""
        print("🔍 检查构建环境...")
        
        # 检查 Python
        try:
            python_version = subprocess.check_output([sys.executable, '--version'], 
                                                    text=True).strip()
            print(f"✅ {python_version}")
        except:
            print("❌ Python 环境异常")
            return False
            
        # 检查 PyInstaller
        try:
            pyinstaller_version = subprocess.check_output([
                sys.executable, '-m', 'PyInstaller', '--version'
            ], text=True).strip()
            print(f"✅ PyInstaller {pyinstaller_version}")
        except:
            print("❌ PyInstaller 未安装，请运行: pip install pyinstaller")
            return False
            
        # 检查主脚本
        if not (self.project_root / self.main_script).exists():
            print(f"❌ 主脚本不存在: {self.main_script}")
            return False
            
        # 检查资源文件
        missing_assets = []
        for asset_dir in self.asset_dirs:
            if not (self.project_root / asset_dir).exists():
                missing_assets.append(asset_dir)
                
        if missing_assets:
            print(f"⚠️  缺少资源文件夹: {', '.join(missing_assets)}")
        else:
            print("✅ 所有资源文件就绪")
            
        print("✅ 环境检查完成")
        return True
        
    def clean_previous_builds(self):
        """清理之前的构建文件"""
        print("\n🧹 清理之前的构建文件...")
        
        dirs_to_clean = [self.build_dir, self.dist_dir]
        files_to_clean = [self.project_root / f"{self.game_name}.spec"]
        
        cleaned_count = 0
        
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"✅ 删除目录: {dir_path.name}")
                cleaned_count += 1
                
        for file_path in files_to_clean:
            if file_path.exists():
                file_path.unlink()
                print(f"✅ 删除文件: {file_path.name}")
                cleaned_count += 1
                
        if cleaned_count == 0:
            print("✅ 无需清理，目录已干净")
            
    def build_game(self):
        """构建游戏可执行文件"""
        print(f"\n📦 开始构建 {self.game_name}...")
        
        # 构建 PyInstaller 命令
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',           # 单文件打包
            '--noconsole',         # 无控制台窗口
            '--clean',             # 清理临时文件
            f'--name={self.game_name}',
        ]
        
        # 添加图标（如果存在）
        if (self.project_root / self.icon_file).exists():
            cmd.append(f'--icon={self.icon_file}')
        else:
            print("⚠️  未找到图标文件，使用默认图标")
            
        # 添加资源文件
        for asset_dir in self.asset_dirs:
            if (self.project_root / asset_dir).exists():
                cmd.append(f'--add-data={asset_dir}{os.pathsep}{asset_dir}')
                
        # 添加隐藏导入（Pygame 相关）
        cmd.extend(['--hidden-import=pygame._view'])
        
        # 添加主脚本
        cmd.append(str(self.main_script))
        
        print(f"🔧 执行命令: {' '.join(cmd)}")
        
        # 执行构建
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✅ 构建成功完成！")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 构建失败！错误信息:")
            print(e.stderr)
            return False
            
    def create_release_package(self):
        """创建发布包"""
        print(f"\n📁 创建发布包...")
        
        # 创建 releases 目录
        self.release_dir.mkdir(exist_ok=True)
        
        # 生成版本名称
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        release_name = f"{self.game_name}_v{self.version}_{timestamp}"
        release_path = self.release_dir / release_name
        
        # 创建发布目录
        release_path.mkdir(exist_ok=True)
        
        # 复制可执行文件
        exe_source = self.dist_dir / f"{self.game_name}.exe"
        exe_dest = release_path / f"{self.game_name}.exe"
        
        if exe_source.exists():
            shutil.copy2(exe_source, exe_dest)
            print(f"✅ 复制可执行文件: {exe_dest.name}")
        else:
            print(f"❌ 可执行文件不存在: {exe_source}")
            return False
            
        # 复制资源文件
        for asset_dir in self.asset_dirs:
            source_dir = self.project_root / asset_dir
            dest_dir = release_path / asset_dir
            
            if source_dir.exists():
                shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
                print(f"✅ 复制资源文件: {asset_dir}/")
                
        # 复制文档文件
        docs_to_copy = ["README.md", "CHANGELOG.md"]
        for doc_file in docs_to_copy:
            source_file = self.project_root / doc_file
            if source_file.exists():
                shutil.copy2(source_file, release_path / doc_file)
                print(f"✅ 复制文档: {doc_file}")
                
        # 创建版本信息文件
        self._create_version_file(release_path)
        
        # 创建压缩包
        zip_path = self.release_dir / f"{release_name}.zip"
        shutil.make_archive(str(release_path), 'zip', str(release_path))
        
        # 清理临时目录
        shutil.rmtree(release_path)
        
        print(f"🎉 发布包创建完成: {zip_path.name}")
        return zip_path
        
    def _create_version_file(self, release_path):
        """创建版本信息文件"""
        version_info = f"""
{self.game_name} 版本信息
=======================

版本号: {self.version}
构建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
构建环境: Python {sys.version}

文件说明:
- {self.game_name}.exe: 主程序
- assets/: 游戏资源文件
- sounds/: 游戏音效文件

系统要求:
- Windows 7/10/11
- 无需安装 Python
- 50MB 可用空间

控制说明:
- 移动: WASD 或方向键
- 暂停: P 键
- 退出: ESC 键

© 2023 Find 1134 - 保留所有权利
        """.strip()
        
        version_file = release_path / "VERSION.txt"
        with open(version_file, 'w', encoding='utf-8') as f:
            f.write(version_info)
        print("✅ 创建版本信息文件: VERSION.txt")
        
    def verify_build(self, zip_path):
        """验证构建结果"""
        print(f"\n🔍 验证构建结果...")
        
        checks = [
            (zip_path.exists(), f"发布包 {zip_path.name}"),
            (zip_path.stat().st_size > 1024 * 1024, "发布包大小合理"),  # 至少 1MB
        ]
        
        all_passed = True
        for check, description in checks:
            if check:
                print(f"✅ {description} - 正常")
            else:
                print(f"❌ {description} - 异常")
                all_passed = False
                
        if all_passed:
            print("🎉 所有验证通过！")
        else:
            print("⚠️  部分验证未通过，请检查构建过程")
            
        return all_passed
        
    def print_summary(self, zip_path, success):
        """打印构建总结"""
        print("\n" + "="*60)
        if success:
            print("🎊 构建完成！")
            print(f"📦 发布文件: {zip_path}")
            print(f"📁 文件大小: {zip_path.stat().st_size // 1024 // 1024} MB")
            print(f"⏰ 总耗时: {datetime.now().strftime('%H:%M:%S')}")
        else:
            print("💥 构建失败！")
            print("💡 请检查错误信息并重试")
        print("="*60)
        
    def run(self):
        """运行完整的构建流程"""
        self.print_header()
        
        # 执行构建步骤
        steps = [
            ("环境检查", self.check_environment),
            ("清理工作", self.clean_previous_builds),
            ("构建游戏", self.build_game),
            ("创建发布包", self.create_release_package),
        ]
        
        success = True
        zip_path = None
        
        for step_name, step_func in steps:
            if not success:  # 如果前面步骤失败，跳过后续
                break
                
            print(f"\n{'='*40}")
            print(f"步骤: {step_name}")
            print(f"{'='*40}")
            
            try:
                result = step_func()
                if step_name == "创建发布包" and result:
                    zip_path = result
                success = success and result
            except Exception as e:
                print(f"❌ 步骤 '{step_name}' 执行异常: {e}")
                success = False
                
        # 验证和总结
        if success and zip_path:
            self.verify_build(zip_path)
            
        self.print_summary(zip_path if success else None, success)
        
        return success

def main():
    """主函数"""
    try:
        builder = GameBuilder()
        success = builder.run()
        
        # 等待用户按键退出
        if success:
            input("\n🎮 按回车键退出...")
        else:
            input("\n❌ 按回车键退出...")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  用户中断构建过程")
    except Exception as e:
        print(f"\n💥 发生未预期错误: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()
