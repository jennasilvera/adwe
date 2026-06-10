async def run_workflow(ctx, workflow_id: str):
    await record_heartbeat()

    async with AsyncSessionLocal() as session:
        workflow = await session.scalar(
            select(Workflow).where(Workflow.id == workflow_id)
        )

        if workflow is None:
            return

        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.utcnow()
        await session.commit()

        try:
            result = workflow_graph.invoke(
                {"repository_url": workflow.repository_url}
            )

            workflow.repository_analysis = result.get(
                "repository_analysis"
            )
            workflow.implementation_plan = result.get(
                "implementation_plan"
            )
            workflow.code_modification = result.get(
                "code_modification"
            )

            await record_audit_event(
                session=session,
                workflow_id=workflow.id,
                event_type="agent.repository_analyzed",
                payload={
                    "file_count": result.get(
                        "repository_analysis",
                        {},
                    ).get("file_count"),
                },
            )

            await record_audit_event(
                session=session,
                workflow_id=workflow.id,
                event_type="agent.plan_created",
                payload={
                    "recommended_steps": result.get(
                        "implementation_plan",
                        {},
                    ).get(
                        "recommended_next_steps",
                        [],
                    ),
                },
            )

            code_modification = (
                result.get("code_modification") or {}
            )

            await record_audit_event(
                session=session,
                workflow_id=workflow.id,
                event_type="agent.patch_proposed",
                payload={
                    "summary": code_modification.get(
                        "summary"
                    ),
                    "target_file": code_modification.get(
                        "target_file"
                    ),
                },
            )

            diff = (
                code_modification.get("patch")
                or code_modification.get("diff")
            )

            if diff:
                session.add(
                    Patch(
                        workflow_id=workflow.id,
                        file_path=code_modification.get(
                            "target_file",
                            "README.md",
                        ),
                        diff=diff,
                        status=PatchStatus.PROPOSED,
                        summary=code_modification.get(
                            "summary"
                        ),
                        files_changed=(
                            [
                                code_modification.get(
                                    "target_file"
                                )
                            ]
                            if code_modification.get(
                                "target_file"
                            )
                            else None
                        ),
                        reasoning=(
                            "Selected from repository "
                            "analysis and implementation "
                            "plan."
                        ),
                    )
                )

            workflow.status = WorkflowStatus.COMPLETED
            workflow.completed_at = datetime.utcnow()

        except Exception as exc:
            logger.exception(
                "workflow_failed workflow_id=%s",
                workflow_id,
            )

            workflow.retry_count += 1
            workflow.last_error = str(exc)
            workflow.completed_at = datetime.utcnow()

            if workflow.retry_count < MAX_WORKFLOW_RETRIES:
                workflow.status = WorkflowStatus.PENDING

                await session.commit()

                await ctx["redis"].enqueue_job(
                    "run_workflow",
                    workflow.id,
                    _defer_by=workflow.retry_count * 30,
                )

                return

            workflow.status = WorkflowStatus.FAILED

        await session.commit()
