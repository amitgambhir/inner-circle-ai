import re
from dataclasses import dataclass, field


@dataclass
class BriefingItem:
    number: int
    title: str
    bottom_line: str
    recommendation: str
    file_path: str
    agent: str

    def format_telegram(self) -> str:
        urgent = "🚨 " if "[URGENT]" in self.title else ""
        return (
            f"{urgent}*Item {self.number}: {self._escape(self.title)}*\n\n"
            f"*Bottom line:* {self._escape(self.bottom_line)}\n"
            f"*Recommendation:* {self._escape(self.recommendation)}\n"
            f"📁 `{self.file_path}`"
        )

    @staticmethod
    def _escape(text: str) -> str:
        for char in ["_", "[", "]", "(", ")", "~", ">", "#", "+", "-", "=", "|", "{", "}"]:
            text = text.replace(char, f"\\{char}")
        return text


@dataclass
class Briefing:
    date: str
    items: list = field(default_factory=list)
    summary: str = ""


def parse_briefing(content: str) -> Briefing:
    date_match = re.search(r"# CEO Briefing — (\d{4}-\d{2}-\d{2})", content)
    date = date_match.group(1) if date_match else ""

    item_pattern = re.compile(
        r"### (\d+)\. (.+)\n"
        r"\*\*Bottom line:\*\* (.+)\n"
        r"\*\*Ada's recommendation:\*\* (.+)\n"
        r"\*\*File:\*\* `(.+?)`",
        re.MULTILINE,
    )

    items = []
    for match in item_pattern.finditer(content):
        number = int(match.group(1))
        title = match.group(2).strip()
        bottom_line = match.group(3).strip()
        recommendation = match.group(4).strip()
        file_path = match.group(5).strip()

        agent_match = re.search(r"outbox/(\w+)/", file_path)
        agent = agent_match.group(1) if agent_match else ""

        items.append(BriefingItem(
            number=number, title=title, bottom_line=bottom_line,
            recommendation=recommendation, file_path=file_path, agent=agent,
        ))

    summary = ""
    status_match = re.search(r"## Status Update\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    if status_match:
        summary += status_match.group(1).strip()

    flags_match = re.search(r"## Flags\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    if flags_match:
        summary += "\n\n" + flags_match.group(1).strip()

    return Briefing(date=date, items=items, summary=summary.strip())
