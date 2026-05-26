"""
在线更新检查模块
从 GitHub Releases 获取最新版本信息
"""

import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any


class UpdateChecker:
    """更新检查器"""

    def __init__(self, repo_owner: str, repo_name: str, current_version: str):
        """
        初始化更新检查器

        Args:
            repo_owner: GitHub 仓库所有者
            repo_name: GitHub 仓库名称
            current_version: 当前应用版本
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.api_url = (
            f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        )

    def check_for_updates(self, timeout: int = 10) -> Dict[str, Any]:
        """
        检查是否有新版本

        Args:
            timeout: 请求超时时间（秒）

        Returns:
            包含更新信息的字典:
            {
                'has_update': bool,  # 是否有更新
                'latest_version': str,  # 最新版本号
                'current_version': str,  # 当前版本号
                'release_url': str,  # 发布页面 URL
                'download_url': str,  # 下载 URL
                'release_notes': str,  # 更新说明
                'published_at': str,  # 发布时间
                'error': str  # 错误信息（如果有）
            }
        """
        result = {
            "has_update": False,
            "latest_version": "",
            "current_version": self.current_version,
            "release_url": "",
            "download_url": "",
            "release_notes": "",
            "published_at": "",
            "error": "",
        }

        try:
            # 创建请求
            req = urllib.request.Request(
                self.api_url,
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "VV-TODO-App",
                },
            )

            # 发送请求
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status != 200:
                    result["error"] = f"HTTP 错误: {response.status}"
                    return result

                # 解析响应
                data = json.loads(response.read().decode("utf-8"))

                # 提取版本信息
                latest_version = data.get("tag_name", "").lstrip("v")
                result["latest_version"] = latest_version
                result["release_url"] = data.get("html_url", "")
                result["release_notes"] = data.get("body", "")
                result["published_at"] = data.get("published_at", "")

                # 查找 Windows 可执行文件下载链接
                assets = data.get("assets", [])
                for asset in assets:
                    name = asset.get("name", "").lower()
                    if name.endswith(".exe") or "windows" in name:
                        result["download_url"] = asset.get("browser_download_url", "")
                        break

                # 如果没有找到特定的 exe 文件，使用发布页面 URL
                if not result["download_url"]:
                    result["download_url"] = result["release_url"]

                # 比较版本号
                result["has_update"] = self._compare_versions(
                    latest_version, self.current_version
                )

        except urllib.error.HTTPError as e:
            result["error"] = f"HTTP 错误: {e.code} - {e.reason}"
        except urllib.error.URLError as e:
            result["error"] = f"网络错误: {str(e.reason)}"
        except json.JSONDecodeError:
            result["error"] = "解析响应数据失败"
        except Exception as e:
            result["error"] = f"未知错误: {str(e)}"

        return result

    def _compare_versions(self, version1: str, version2: str) -> bool:
        """
        比较两个版本号

        Args:
            version1: 版本号1（最新版本）
            version2: 版本号2（当前版本）

        Returns:
            如果 version1 > version2 返回 True，否则返回 False
        """
        try:
            # 移除可能的 'v' 前缀
            v1 = version1.lstrip("v").strip()
            v2 = version2.lstrip("v").strip()

            # 分割版本号
            parts1 = [int(x) for x in v1.split(".") if x.isdigit()]
            parts2 = [int(x) for x in v2.split(".") if x.isdigit()]

            # 补齐长度
            max_len = max(len(parts1), len(parts2))
            parts1.extend([0] * (max_len - len(parts1)))
            parts2.extend([0] * (max_len - len(parts2)))

            # 逐位比较
            for p1, p2 in zip(parts1, parts2):
                if p1 > p2:
                    return True
                elif p1 < p2:
                    return False

            return False

        except Exception:
            # 如果比较失败，返回 False
            return False

    def get_release_page_url(self) -> str:
        """获取 GitHub Releases 页面 URL"""
        return f"https://github.com/{self.repo_owner}/{self.repo_name}/releases"


# 示例用法
if __name__ == "__main__":
    # 测试更新检查
    checker = UpdateChecker("rpvvn", "VV_TODO", "3.1")
    result = checker.check_for_updates()

    print("检查更新结果:")
    print(f"当前版本: {result['current_version']}")
    print(f"最新版本: {result['latest_version']}")
    print(f"有更新: {result['has_update']}")
    print(f"发布页面: {result['release_url']}")
    print(f"下载链接: {result['download_url']}")
    print(f"发布时间: {result['published_at']}")
    if result["error"]:
        print(f"错误: {result['error']}")
    if result["release_notes"]:
        print(f"\n更新说明:\n{result['release_notes']}")
