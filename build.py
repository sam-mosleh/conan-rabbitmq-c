from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="rabbitmq-c:shared")
    if platform.system() == "Windows":
        builder.builds = [(settings, options, env_vars, build_requires) for settings, options, env_vars, build_requires in builder.builds if options.get("rabbitmq-c:shared")]
    builder.run()
