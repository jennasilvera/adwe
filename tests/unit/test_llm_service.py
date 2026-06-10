from adwe.services.llm import LLMError, generate_text, llm_available


def test_llm_disabled_by_default():
    assert llm_available() is False


def test_generate_text_requires_enabled_llm():
    try:
        generate_text("hello")
    except LLMError as exc:
        assert "LLM is not enabled" in str(exc)
    else:
        raise AssertionError("expected LLMError")
