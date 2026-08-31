#!/usr/bin/env python3
"""
Script to automatically update README.md with current repository statistics.
Fetches star counts from GitHub API and conditionally displays them (only if > 0).
"""

import os
import re
import requests
from typing import Dict, Optional

# Repository data with links and descriptions
REPOS = {
    "ProjectManagementSystem": {
        "desc": "ASP.NET Core Web API with Domain Driven Design & Clean Architecture",
        "category": "aspnet"
    },
    "CarRentalAPI": {
        "desc": "Web API for Car Rental System",
        "category": "aspnet"
    },
    "MyPostcodeApi": {
        "desc": "Web API for Malaysian postcodes",
        "category": "aspnet"
    },
    "Fuel-Cost-Calculator": {
        "desc": "Blazor WebAssembly App",
        "category": "aspnet"
    },
    "PCSX2-Game-Cover-Downloader": {
        "desc": "PS2 cover art downloader utility",
        "category": "console_ps2"
    },
    "PS2-Manager": {
        "desc": "Desktop tool for managing PS2 disc images",
        "category": "console_ps2"
    },
    "PS3Dec-GUI": {
        "desc": "GUI for PS3Dec ISO decryption",
        "category": "console_ps3"
    },
    "PS3_UPDATE-Remover": {
        "desc": "Remove PS3_UPDATE folder from PS3 backups",
        "category": "console_ps3"
    },
    "Simple-Eboot-Resigner": {
        "desc": "Resign retail PS3 Eboot to lower firmware",
        "category": "console_ps3"
    },
    "PS4-PKG-Tool": {
        "desc": "Manage and perform operations on PS4 PKG files",
        "category": "console_ps4"
    },
    "PS4-Dump-Checker": {
        "desc": "Validate PS4 flash dumps",
        "category": "console_ps4"
    },
    "PS4-Dump-Extractor": {
        "desc": "Extract PS4 dump including sflash0 files",
        "category": "console_ps4"
    },
    "PS4-Firmware-Checker": {
        "desc": "Check latest PS4 firmware versions",
        "category": "console_ps4"
    },
    "PS4-BT_WIFI-PATCHER": {
        "desc": "Patcher for BT_WIFI (TORUS) firmware",
        "category": "console_ps4"
    },
    "sflash0unpack": {
        "desc": "Unpacks sflash0 files from PS4 flash dumps",
        "category": "console_ps4"
    },
    "PS5-Firmware-Checker": {
        "desc": "WinForms app to check & download latest PS5 firmware",
        "category": "console_ps5"
    },
    "PS5-Backward-Compatibility-Check": {
        "desc": "Check PS5 backward compatibility status",
        "category": "console_ps5"
    },
    "PS5TrophyExtract0r": {
        "desc": "Extract NpTrophy v2 data files from PS5 games",
        "category": "console_ps5"
    },
    "Playstation-Error-Code-Checker": {
        "desc": "Check error codes of PlayStation console devices",
        "category": "console_other"
    },
    "CFW2OFW-TO-PKG": {
        "desc": "Convert CFW/OFW games to PKG format",
        "category": "console_other"
    },
    "OrbisPkgTool": {
        "desc": "Orbis package tool",
        "category": "console_other"
    },
    "Huawei-Router-Tool": {
        "desc": "Tool to interact with Huawei router using API",
        "category": "huawei"
    },
    "HuaweiAPI": {
        "desc": "Huawei API library",
        "category": "huawei"
    },
    "Huawei-B618-AIO-Tool": {
        "desc": "All-in-one tool for Huawei B618 router",
        "category": "huawei"
    },
    "Huawei-WEBUI-Mod": {
        "desc": "Extract WEBUI from router firmware",
        "category": "huawei"
    },
    "File-Splitter-Joiner": {
        "desc": "Windows utility to split/join files >4GB",
        "category": "desktop"
    },
    "Safemoon-Tracker": {
        "desc": "Crypto tracking application for SafeMoon",
        "category": "desktop"
    },
    "Simple-Network-Config": {
        "desc": "Ethernet network configuration toggle utility",
        "category": "desktop"
    },
    "DarkUI": {
        "desc": "Dark themed control and docking library for .NET WinForms",
        "category": "desktop"
    },
    "Shopee-Autobuy-Bot": {
        "desc": "Automation for purchasing products on Shopee",
        "category": "bots"
    },
    "TouchnGo-Bot": {
        "desc": "TouchnGo automation bot",
        "category": "bots"
    },
    "Shopee-Collection-Scan": {
        "desc": "Scan and display upcoming Shopee Payday Sale items",
        "category": "bots"
    },
    "SonyStoreMalaysiaBot": {
        "desc": "Monitor and auto-checkout products at Sony Store Malaysia",
        "category": "bots"
    },
    "Selenium-Automation": {
        "desc": "Web automation using Selenium Framework",
        "category": "testing"
    },
    "FluentSelenium": {
        "desc": "Fluent API wrapper for Selenium WebDriver in C#",
        "category": "testing"
    },
    "Yet-Another-Proxy-Tool": {
        "desc": "Scrape and verify proxies from multiple sources",
        "category": "testing"
    },
    "JavaBankingApp": {
        "desc": "Banking application (Java newbie project)",
        "category": "java"
    },
    "JavaCarRentalApp": {
        "desc": "Car rental application",
        "category": "java"
    },
    "balong-usbload-english": {
        "desc": "English translation of Balong USBLoad",
        "category": "misc"
    },
    "ESP8266-Dumper": {
        "desc": "ESP8266 firmware dumper utility",
        "category": "misc"
    },
    "ESP8266-exploit-host": {
        "desc": "ESP8266 exploit host utilities",
        "category": "misc"
    },
    "ps4errorcode": {
        "desc": "PS4 error code database",
        "category": "misc"
    },
    "csv-to-html-table": {
        "desc": "Convert CSV files to searchable, filterable HTML tables",
        "category": "misc"
    },
    "Face-Detection": {
        "desc": "Face detection project",
        "category": "misc"
    },
    "ai-agents-for-beginners": {
        "desc": "11 Lessons to Get Started Building AI Agents",
        "category": "misc"
    },
    "cs-video-courses": {
        "desc": "Curated list of Computer Science courses with video lectures",
        "category": "misc"
    },
    "lgdxrobot-cloud": {
        "desc": "Robot management system with focus on flexibility and security",
        "category": "misc"
    },
    "prompt-eng-interactive-tutorial": {
        "desc": "Anthropic's Interactive Prompt Engineering Tutorial",
        "category": "misc"
    },
}

def fetch_star_count(repo_name: str, token: Optional[str] = None) -> Optional[int]:
    """
    Fetch star count for a repository using GitHub API.
    
    Args:
        repo_name: Repository name
        token: GitHub token for API authentication
    
    Returns:
        Star count or None if fetch fails
    """
    url = f"https://api.github.com/repos/pearlxcore/{repo_name}"
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get("stargazers_count", 0)
    except Exception as e:
        print(f"⚠️  Failed to fetch stars for {repo_name}: {e}")
        return None

def format_repo_line(repo_name: str, desc: str, stars: Optional[int]) -> str:
    """
    Format a repository line with conditional star display.
    Stars only shown if > 0.
    
    Args:
        repo_name: Repository name
        desc: Repository description
        stars: Star count (can be None or 0)
    
    Returns:
        Formatted markdown line
    """
    link = f"[{repo_name}](https://github.com/pearlxcore/{repo_name})"
    line = f"- {link} - {desc}"
    
    # Only add stars if greater than 0
    if stars and stars > 0:
        line += f" | ⭐ {stars}"
    
    return line

def generate_readme_section(star_data: Dict[str, int]) -> str:
    """
    Generate the repository categories section for README.
    
    Args:
        star_data: Dictionary mapping repo names to star counts
    
    Returns:
        Formatted markdown section
    """
    # Organize repos by category
    categories = {
        "aspnet": {"title": "🌐 ASP.NET & Web API Projects", "repos": []},
        "console": {"title": "🎮 Console & Gaming Tools", "subs": {
            "console_ps2": "#### PlayStation 2",
            "console_ps3": "#### PlayStation 3",
            "console_ps4": "#### PlayStation 4",
            "console_ps5": "#### PlayStation 5",
            "console_other": "#### Other Console",
        }, "repos": []},
        "huawei": {"title": "📱 Huawei Router Projects", "repos": []},
        "desktop": {"title": "🖥️ Desktop Applications", "repos": []},
        "bots": {"title": "🤖 Automation & Bot Projects", "repos": []},
        "testing": {"title": "🧪 Testing & Selenium Projects", "repos": []},
        "java": {"title": "☕ Java Projects", "repos": []},
        "misc": {"title": "🔧 Miscellaneous & Learning Projects", "repos": []},
    }
    
    # Group repos by category
    for repo_name, repo_info in REPOS.items():
        cat = repo_info["category"]
        stars = star_data.get(repo_name, 0)
        line = format_repo_line(repo_name, repo_info["desc"], stars)
        
        # Handle console subcategories
        if cat.startswith("console_"):
            if "subs_data" not in categories["console"]:
                categories["console"]["subs_data"] = {}
            if cat not in categories["console"]["subs_data"]:
                categories["console"]["subs_data"][cat] = []
            categories["console"]["subs_data"][cat].append(line)
        else:
            categories[cat]["repos"].append(line)
    
    # Build markdown
    markdown = "## 📂 Repository Categories\n\n"
    
    for cat_key, cat_data in categories.items():
        title = cat_data["title"]
        
        if cat_key == "console":
            # Special handling for console with subcategories
            total_console = sum(len(repos) for repos in cat_data.get("subs_data", {}).values())
            markdown += f"<details>\n<summary><b>{title} ({total_console} repos)</b></summary>\n\n"
            
            # Add subcategories
            for sub_key in ["console_ps2", "console_ps3", "console_ps4", "console_ps5", "console_other"]:
                if sub_key in cat_data.get("subs_data", {}):
                    markdown += f"{cat_data['subs']}\n"
                    for repo_line in cat_data["subs_data"][sub_key]:
                        markdown += f"{repo_line}\n"
                    markdown += "\n"
        else:
            repo_count = len(cat_data["repos"])
            if repo_count > 0:
                markdown += f"<details>\n<summary><b>{title} ({repo_count} repos)</b></summary>\n\n"
                for repo_line in cat_data["repos"]:
                    markdown += f"{repo_line}\n"
        
        markdown += "</details>\n\n"
    
    # Add stats table
    markdown += "---\n\n## 📊 Repository Statistics\n\n"
    markdown += "| Category | Count | Top Repo |\n"
    markdown += "|----------|-------|----------|\n"
    markdown += "| 🌐 ASP.NET & Web API | 4 | ProjectManagementSystem (⭐ 1) |\n"
    markdown += "| 🎮 Console & Gaming | 17 | **PS4-PKG-Tool (⭐ 455)** |\n"
    markdown += "| 📱 Huawei Router | 4 | Huawei-Router-Tool (⭐ 169) |\n"
    markdown += "| 🖥️ Desktop Applications | 4 | Simple-Network-Config (⭐ 3) |\n"
    markdown += "| 🤖 Automation & Bots | 4 | **Shopee-Autobuy-Bot (⭐ 97)** |\n"
    markdown += "| 🧪 Testing & Selenium | 3 | Selenium-Automation / FluentSelenium / Yet-Another-Proxy-Tool (⭐ 3) |\n"
    markdown += "| ☕ Java Projects | 2 | JavaBankingApp (⭐ 2) |\n"
    markdown += "| 🔧 Misc & Learning | 10 | ESP8266-Dumper (⭐ 9) |\n"
    markdown += "| **TOTAL** | **~48 repos** | **Total ⭐ 1,077** |\n\n"
    
    return markdown

def update_readme(new_section: str):
    """
    Update README.md with new repository section.
    Replaces content between markers.
    
    Args:
        new_section: New markdown section to insert
    """
    readme_path = "README.md"
    
    if not os.path.exists(readme_path):
        print(f"❌ {readme_path} not found!")
        return
    
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Markers for section replacement
    start_marker = "## 📂 Repository Categories"
    end_marker = "## Languages"
    
    if start_marker in content and end_marker in content:
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)
        
        # Replace section
        new_content = content[:start_idx] + new_section + content[end_idx:]
        
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print("✅ README.md updated successfully!")
    else:
        print("❌ Could not find section markers in README.md")

def main():
    """Main function to fetch stats and update README."""
    print("🚀 Fetching repository statistics...")
    
    token = os.getenv("GITHUB_TOKEN")
    star_data = {}
    
    for repo_name in REPOS.keys():
        stars = fetch_star_count(repo_name, token)
        if stars is not None:
            star_data[repo_name] = stars
            print(f"  ✓ {repo_name}: ⭐ {stars}")
        else:
            print(f"  ⚠️  {repo_name}: Could not fetch")
    
    print("\n📝 Generating README section...")
    new_section = generate_readme_section(star_data)
    
    print("📤 Updating README.md...")
    update_readme(new_section)
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()
