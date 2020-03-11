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

    def configure(self):
        if self.options.ssl:
            self.options["openssl"].shared = self.options.shared
        if self.settings.compiler == "Visual Studio":
            del self.settings.compiler.runtime

    def requirements(self):
        if self.options.ssl:
            self.requires.add("openssl/1.1.1d")

    def source(self):
        download_url = "{}/archive/v{}.tar.gz".format(self.homepage,
                                                      self.version)
        tools.get(download_url)
        os.rename("{}-{}".format(self.name, self.version), self.sources_folder)

    def build(self):
        cmake = CMake(self)

        cmake.definitions['ENABLE_SSL_SUPPORT'] = self.options.ssl
        if self.options.ssl:
            cmake.definitions['OPENSSL_ROOT_DIR'] = self.deps_cpp_info[
                "openssl"].rootpath

        cmake.definitions['BUILD_EXAMPLES'] = False
        cmake.definitions['BUILD_TESTS'] = False
        cmake.definitions['BUILD_TOOLS'] = False
        cmake.definitions['ENABLE_DOC'] = False

        cmake.definitions['BUILD_SHARED_LIBS'] = self.options.shared
        cmake.definitions['BUILD_STATIC_LIBS'] = not self.options.shared

        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include", src=self.name)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            if self.options.shared:
                self.cpp_info.libs = ["rabbitmq.4"]
            else:
                self.cpp_info.libs = ["librabbitmq.4", "crypt32", "ws2_32"]
        else:
            self.cpp_info.libs = ["rabbitmq", "pthread"]
