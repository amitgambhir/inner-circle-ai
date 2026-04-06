import os
import pytest
from unittest.mock import patch


def test_load_config_from_env():
    env = {
        "TELEGRAM_BOT_TOKEN": "test-token-123",
        "TELEGRAM_CEO_CHAT_ID": "99999",
        "DEFAULT_PROJECT": "my-project",
    }
    with patch.dict(os.environ, env, clear=False):
        from bot.config import load_config

        cfg = load_config()
        assert cfg.bot_token == "test-token-123"
        assert cfg.ceo_chat_id == 99999
        assert cfg.default_project == "my-project"


def test_load_config_defaults():
    env = {
        "TELEGRAM_BOT_TOKEN": "test-token-123",
        "TELEGRAM_CEO_CHAT_ID": "99999",
    }
    with patch.dict(os.environ, env, clear=False):
        os.environ.pop("DEFAULT_PROJECT", None)
        from importlib import reload
        import bot.config

        reload(bot.config)
        cfg = bot.config.load_config()
        assert cfg.default_project == "inner-circle-mgmt"


def test_load_config_missing_token():
    env = {"TELEGRAM_CEO_CHAT_ID": "99999"}
    with patch.dict(os.environ, env, clear=True):
        os.environ.pop("TELEGRAM_BOT_TOKEN", None)
        from importlib import reload
        import bot.config

        reload(bot.config)
        with pytest.raises(ValueError, match="TELEGRAM_BOT_TOKEN"):
            bot.config.load_config()


def test_load_config_missing_chat_id():
    env = {"TELEGRAM_BOT_TOKEN": "test-token"}
    with patch.dict(os.environ, env, clear=True):
        os.environ.pop("TELEGRAM_CEO_CHAT_ID", None)
        from importlib import reload
        import bot.config

        reload(bot.config)
        with pytest.raises(ValueError, match="TELEGRAM_CEO_CHAT_ID"):
            bot.config.load_config()


def test_agent_definitions():
    from bot.config import AGENTS, AGENT_ORDER

    assert len(AGENTS) == 5
    assert AGENT_ORDER == ["curie", "tesla", "ogilvy", "nightingale", "ada"]
    assert AGENTS["ada"]["title"] == "Ada, Chief of Staff"
    assert AGENTS["curie"]["title"] == "Curie, Head of Research"


def test_project_paths(tmp_path):
    from bot.config import project_paths

    paths = project_paths("inner-circle-mgmt", base_dir=str(tmp_path))
    assert paths["project_dir"] == str(tmp_path / "projects" / "inner-circle-mgmt")
    assert paths["outbox_ada"] == str(
        tmp_path / "projects" / "inner-circle-mgmt" / "outbox" / "ada"
    )
    assert paths["escalations"] == str(
        tmp_path / "projects" / "inner-circle-mgmt" / "escalations"
    )
