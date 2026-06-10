def test_agent_audit_event_names():
    expected = {
        "agent.repository_analyzed",
        "agent.plan_created",
        "agent.patch_proposed",
    }

    assert "agent.repository_analyzed" in expected
    assert "agent.plan_created" in expected
    assert "agent.patch_proposed" in expected
