from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(build_policy="missing",
                                 upload_dependencies="all")
    builder.add_common_builds(shared_option_name="rabbitmq-c:shared",
                              pure_c=False,
                              build_all_options_values=["rabbitmq-c:ssl"])
    builder.run()
