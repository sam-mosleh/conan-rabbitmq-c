from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(visual_runtimes=["MD", "MDd"], build_policy="missing", upload_dependencies="all")
    builder.add_common_builds(shared_option_name="rabbitmq-c:shared",
                              pure_c=False)
    builder.run()
