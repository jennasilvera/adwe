from adwe.core.config import settings


def test_llm_config_defaults_disabled():
    assert settings.llm_enabled is False
    assert settings.llm_model
    assert settings.llm_base_url
