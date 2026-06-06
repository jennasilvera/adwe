from adwe.models.patch_summary_schema import PatchSummaryRead


def test_patch_summary_schema():
    summary = PatchSummaryRead(
        workflow_id="workflow-123",
        total=3,
        proposed=1,
        applied=1,
        rejected=1,
    )

    assert summary.total == 3
    assert summary.proposed == 1
    assert summary.applied == 1
    assert summary.rejected == 1
