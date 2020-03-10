from conans import CMake, ConanFile, tools
import os

class RabbitmqcConan(ConanFile):
    name = "rabbitmq-c"
    version = "0.10.0"
    license = "https://github.com/alanxz/rabbitmq-c/blob/master/LICENSE-MIT"
    author = "Sam Mosleh sam.mosleh@ut.ac.ir"
    url = "https://github.com/sam-mosleh/conan-rabbitmq-c"

    description = """This is a RabbitMQ C client package.
    A fully featured, portable rabbitmq-c library."""

    topics = ("rabbitmq-c", "rabbitmq", "message queue")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "ssl": [True, False]}
    default_options = {"shared": False, "ssl": True}
    generators = "cmake"
    exports_sources = "CMakeLists.txt"
    file_name = name + ".tar.gz"
    unzipped_folder = "{}-{}".format(name, version)
    sources_folder = "sources"
    github_user = "alanxz"
    github_repo = "rabbitmq-c"

    def configure(self):
        if self.options.ssl:
            self.options["openssl"].shared = self.options.shared
        if self.settings.compiler == "Visual Studio":
            del self.settings.compiler.runtime

    def requirements(self):
        if self.options.ssl:
            self.requires.add("openssl/1.1.1d")

    def source(self):
        download_url = "https://github.com/{}/{}/archive/v{}.tar.gz".format(
            self.github_user, self.github_repo, self.version)
        tools.download(download_url, self.file_name)
        tools.unzip(self.file_name)
        os.rename(self.unzipped_folder, self.sources_folder)

    def build(self):
        cmake = CMake(self)

        if self.options.ssl:
            cmake.definitions['ENABLE_SSL_SUPPORT'] = "ON"
            cmake.definitions['OPENSSL_ROOT_DIR'] = self.deps_cpp_info["openssl"].rootpath
        else:
            cmake.definitions['ENABLE_SSL_SUPPORT'] = "OFF"

        cmake.definitions['BUILD_EXAMPLES'] = "OFF"
        cmake.definitions['BUILD_TESTS'] = "OFF"
        cmake.definitions['BUILD_TOOLS'] = "OFF"
        cmake.definitions['ENABLE_DOC'] = "OFF"

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
                self.cpp_info.libs = ["librabbitmq.4", "crypt32", "ws2_32.lib.lib"]
        else:
            self.cpp_info.libs = ["rabbitmq", "pthread"]
