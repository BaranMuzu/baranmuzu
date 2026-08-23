# hi hello
# this is mainly inherited from daveberry's readme
# ok bye

import json
import re
import urllib.request

WAKATIME_URL = "https://wakatime.com/share/@BaranMuzu/d7220c14-02cb-4217-8684-453e65f5545a.json"
WAKATIME_SPACES = " " * 8

PROJECTS_FORMAT = "list" # "table", "list"
PROJECTS_SPACES = " " * 4

GITHUB_SPACES = " " * 8
GITHUB_USERNAME = "baranmuzu"

def replaceSection(something, section, content, readme, spaces):
    return re.sub(
        rf"<!--START OF {something} {section}-->.*?<!--END OF {something} {section}-->",
        f"<!--START OF {something} {section}-->\n{content}\n{spaces[:-2]}<!--END OF {something} {section}-->",
        readme,
        flags=re.DOTALL,
    )

def loadProjects():
    with open("projects.json", "r") as f:
        projects = json.load(f)
    with open("README.md", "r") as f:
        readme = f.read()

    if PROJECTS_FORMAT == "table":
        projectNames = "\n".join(f'{PROJECTS_SPACES}<td><a href="{p["url"]}">{p["name"]}</a></td>' for p in projects)
        projectDescriptions = "\n".join(f'{PROJECTS_SPACES}<td>{p["description"]}</td>' for p in projects)
        projectImages = "\n".join(f'{PROJECTS_SPACES}<td><img src="{p["imageURL"]}" alt="{p["name"]}"></td>' for p in projects)

        readme = replaceSection("PROJECTS", "NAMES", projectNames, readme, PROJECTS_SPACES)
        readme = replaceSection("PROJECTS", "DESCRIPTIONS", projectDescriptions, readme, PROJECTS_SPACES)
        readme = replaceSection("PROJECTS", "IMAGE", projectImages, readme, PROJECTS_SPACES)
    elif PROJECTS_FORMAT == "list":
        projectFormat = "\n".join(f'{PROJECTS_SPACES}<li> <img src="{p["imageURL"]}" alt="{p["name"]}" width="24" height="24"> <a href="{p["url"]}">{p["name"]}</a>: <span>{p["description"]}</span> </li>' for p in projects)
        readme = replaceSection("PROJECTS", "NAMES", projectFormat, readme, PROJECTS_SPACES)

    with open("README.md", "w") as f:
        f.write(readme)

def loadWakatime():
    with urllib.request.urlopen(WAKATIME_URL) as f:
        data = json.load(f)
        limitedData = data["data"]
    with open("README.md", "r") as f:
        readme = f.read()

    ignoredLanguages = [
        "Markdown",
        "HTML",
        "CSS",
        "JSON",
        "YAML",
        "Other",
        "Text",
        "TOML",
        "git ignore",
        "RPMSpec",
        "XML",
        "Git Config",
        "jsonc",
        "go mod",
        "Desktop file",
        "Image (svg)",
        "TSConfig",
        "CSV",
        "INI",
        "conf",
        "Java Properties",
        "TableGen",
        "Apache Config",
        "CMake",
        "systemd",
        "Checksums"
    ]

    limitedData = [d for d in limitedData if d["name"] not in ignoredLanguages][:6]

    wakatimeLanguages = "\n".join(f'{WAKATIME_SPACES}<td><b>{d["name"]}</b></td>' for d in limitedData)
    wakatimeTime = "\n".join(f'{WAKATIME_SPACES}<td>{d["text"]}</td>' for d in limitedData)
    readme = replaceSection("WAKATIME", "LANGUAGES", wakatimeLanguages, readme, WAKATIME_SPACES)
    readme = replaceSection("WAKATIME", "TIME", wakatimeTime, readme, WAKATIME_SPACES)

    with open("README.md", "w") as f:
        f.write(readme)

def loadGithub():
    with open("README.md", "r") as f:
        readme = f.read()

    GITHUB_TOTAL_COMMITS_URL = f"https://api.github.com/search/commits?q=author:{GITHUB_USERNAME}&per_page=1"
    GITHUB_TOTAL_PR_URL = f"https://api.github.com/search/issues?q=author:{GITHUB_USERNAME}+type:pr&per_page=1"
    GITHUB_TOTAL_ISSUES_URL = f"https://api.github.com/search/issues?q=author:{GITHUB_USERNAME}+type:issue&per_page=1"
    GITHUB_TOTAL_REPOS_URL = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100"

    with urllib.request.urlopen(GITHUB_TOTAL_COMMITS_URL) as f:
        githubData = json.load(f)
    totalCommits = githubData["total_count"]
    readme = replaceSection("GITHUB", "TOTALCOMMITS", f"{GITHUB_SPACES}<td>{totalCommits}</td>", readme, GITHUB_SPACES)

    with urllib.request.urlopen(GITHUB_TOTAL_PR_URL) as f:
        githubData = json.load(f)
    totalPRs = githubData["total_count"]
    readme = replaceSection("GITHUB", "PRS", f"{GITHUB_SPACES}<td>{totalPRs}</td>", readme, GITHUB_SPACES)

    with urllib.request.urlopen(GITHUB_TOTAL_ISSUES_URL) as f:
        githubData = json.load(f)
    totalIssues = githubData["total_count"]
    readme = replaceSection("GITHUB", "ISSUES", f"{GITHUB_SPACES}<td>{totalIssues}</td>", readme, GITHUB_SPACES)

    with urllib.request.urlopen(GITHUB_TOTAL_REPOS_URL) as f:
        githubData = json.load(f)
    totalReposStars = sum(r['stargazers_count'] for r in githubData)
    readme = replaceSection("GITHUB", "REPOSSTARS", f"{GITHUB_SPACES}<td>{totalReposStars}</td>", readme, GITHUB_SPACES)

    with open("README.md", "w") as f:
        f.write(readme)

try:
    # loadProjects() -- projects is not needed because baran doesn't share his project in his github...
    loadWakatime()
    loadGithub()
except Exception as e:
    print(e)