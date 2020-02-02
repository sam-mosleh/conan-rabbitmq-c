from conans import CMake, ConanFile, tools


class RabbitmqcConan(ConanFile):
    name = "rabbitmq-c"
    version = "0.10.0"
    license = "https://github.com/alanxz/rabbitmq-c/blob/master/LICENSE-MIT"
    author = "Sam Mosleh sam.mosleh@ut.ac.ir"
    default_user = "sam-mosleh"
    url = "https://github.com/sam-mosleh/conan-rabbitmq-c"

    description = """This is a RabbitMQ C client package.
    A fully featured, portable rabbitmq-c library."""

    topics = ("rabbitmq-c", "rabbitmq")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "ssl": [True, False]}
    default_options = {"shared": False, "ssl": True}
    generators = "cmake"
    file_name = name + ".tar.gz"
    unzipped_folder = "{}-{}".format(name, version)

    @property
    def default_channel(self):
        return "testing"

    def requirements(self):
        if not self.options.ssl:
            self.requires.add("OpenSSL/1.0.2m@conan/stable")

    def source(self):
        download_url = "https://github.com/alanxz/rabbitmq-c/archive/v{}.tar.gz".format(
            self.version)
        tools.download(download_url, self.file_name)
        tools.unzip(self.file_name)

    def build(self):
        cmake = CMake(self)

        if not self.options.ssl:
            cmake.definitions['ENABLE_SSL_SUPPORT'] = "ON"
            cmake.definitions['OPENSSL_ROOT_DIR'] = self.deps_cpp_info[
                "OpenSSL"].rootpath
        else:
            cmake.definitions['ENABLE_SSL_SUPPORT'] = "OFF"

        cmake.definitions['BUILD_EXAMPLES'] = "OFF"
        cmake.definitions['BUILD_TESTS'] = "OFF"
        cmake.definitions['BUILD_TOOLS'] = "OFF"
        cmake.definitions['ENABLE_DOC'] = "OFF"

        if self.options.shared:
            cmake.definitions['BUILD_SHARED_LIBS'] = True
            cmake.definitions['BUILD_STATIC_LIBS'] = False
        else:
            cmake.definitions['BUILD_STATIC_LIBS'] = True
            cmake.definitions['BUILD_SHARED_LIBS'] = False

        cmake.configure(source_folder=self.unzipped_folder)
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
                self.cpp_info.libs = ["librabbitmq.4"]
        else:
            self.cpp_info.libs = ["rabbitmq", "rt"]

        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
        elif self.settings.os == "Windows":
            self.cpp_info.libs.append("ws2_32.lib")

            # Need to link with crypt32 as well for OpenSSL
            if not self.options.ssl:
                self.cpp_info.libs.append("crypt32")
