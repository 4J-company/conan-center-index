import os

from conan import ConanFile
from conan.tools.cmake import cmake_layout
from conan.tools.cmake import CMakeDeps
from conan.tools.cmake import CMakeToolchain
from conan.tools.cmake import CMake
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy, rmdir, get
from conan.api.conan_api import ConanAPI

class MrUtils(ConanFile):
    name = "mr-utils"
    license = "MIT"

    description = "Collection of C++ utilities for 4J projects"

    author = "4J-Company"
    homepage = "https://4j-company.github.io/subprojects/mr-utils/"
    url = "https://github.com/4J-company/mr-utils"

    topics = ("utilities")

    settings = ("os", "compiler", "build_type", "arch")

    options = {
        "target": ["library", "tests", "benchmark", "all"],
    }
    default_options = {
        "target": "library",
    }

    package_type = "header-library"
    exports_sources = "CMakeLists.txt", "include/*", "cmake/deps.cmake"

    def validate(self):
        check_min_cppstd(self, "20")

    def requirements(self):
        self.requires("libassert/2.1.4")
        self.requires("spdlog/1.15.3")

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.27]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version])

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generator = "Ninja"
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

