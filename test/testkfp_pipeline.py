from digitalhub_core_kfp.dsl import pipeline_context


def myhandler(ref):
    #     project = dhcore.get_project("project-kfp2")

    #     s1 = step(name="step1",
    #             project=project.name, function="function-dbt", action="transform",
    #             inputs=[{"employees": ref}], outputs=[{"output_table": "e60"}])

    #     s2 = step(name="step2",
    #             project=project.name, function="function-dbt", action="transform",
    #             inputs=[{"employees": s1.outputs['e60']}], outputs=[{"output_table": "employees_pipeline"}])

    with pipeline_context() as pc:
        s1 = pc.step(
            name="step1",
            function="function-dbt",
            action="transform",
            inputs=[{"employees": ref}],
            outputs=[{"output_table": "e60"}],
        )

        s2 = pc.step(
            name="step2",
            function="function-dbt",
            action="transform",
            inputs=[{"employees": s1.outputs["e60"]}],
            outputs=[{"output_table": "employees_pipeline"}],
        )

        return s2.outputs["employees_pipeline"]
