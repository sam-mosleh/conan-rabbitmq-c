import os

from conans import CMake, ConanFile, tools


class RabbitmqcConan(ConanFile):
    name = "rabbitmq-c"
    version = "0.10.0"
    license = "https://github.com/alanxz/rabbitmq-c/blob/master/LICENSE-MIT"
    author = "Sam Mosleh sam.mosleh@ut.ac.ir"
    url = "https://github.com/sam-mosleh/conan-rabbitmq-c"
    homepage = "https://github.com/alanxz/rabbitmq-c"
    description = """This is a RabbitMQ C client package.
    A fully featured, portable rabbitmq-c library."""

    topics = ("rabbitmq-c", "rabbitmq", "message queue")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "ssl": [True, False]}
    default_options = {"shared": False, "ssl": True}
    generators = "cmake"
    exports_sources = "CMakeLists.txt"
    sources_folder = "sources"
    _cmake = None

    def configure(self):
        if self.options.ssl:
            self.options["openssl"].shared = self.options.shared

    def requirements(self):
        if self.options.ssl:
            self.requires.add("openssl/1.1.1d")

    def source(self):
        download_url = "{}/archive/v{}.tar.gz".format(self.homepage,
                                                      self.version)
        tools.get(download_url)
        os.rename("{}-{}".format(self.name, self.version), self.sources_folder)

    def _configure_cmake(self):
        if self._cmake is not None:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions['ENABLE_SSL_SUPPORT'] = self.options.ssl
        self._cmake.definitions['BUILD_EXAMPLES'] = False
        self._cmake.definitions['BUILD_TESTS'] = False
        self._cmake.definitions['BUILD_TOOLS'] = False
        self._cmake.definitions['ENABLE_DOC'] = False

        self._cmake.definitions['BUILD_SHARED_LIBS'] = self.options.shared
        self._cmake.definitions['BUILD_STATIC_LIBS'] = not self.options.shared
        self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy("*.h", dst="include", src=self.name)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = [
                "rabbitmq.4" if self.options.shared else "librabbitmq.4"
            ]
            self.cpp_info.system_libs.extend(["crypt32", "ws2_32"])
        else:
            self.cpp_info.libs = ["rabbitmq"]
            self.cpp_info.system_libs.append("pthread")
        if not self.options.shared:
            self.cpp_info.defines.append("AMQP_STATIC")
