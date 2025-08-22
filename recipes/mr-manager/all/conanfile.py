import os

from conan import ConanFile
from conan.tools.cmake import cmake_layout
from conan.tools.cmake import CMakeDeps
from conan.tools.cmake import CMakeToolchain
from conan.tools.cmake import CMake
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy, rmdir, get
from conan.api.conan_api import ConanAPI

class MrManager(ConanFile):
    name = "mr-manager"
    license = "MIT"

    description = "Wait-Free object manager with per-type memory pools"

    author = "Michael Tsukanov (mt6@4j-company.ru)"
    url = "https://github.com/4j-company/mr-manager"

    settings = "os", "compiler", "build_type", "arch"

    package_type = "header-library"

    implements = ["auto_header_only"]

    def validate(self):
        if not any(remote.name.lower() == "4j-company" for remote in ConanAPI().remotes.list()):
            raise Exception("Required remote '4J-company' is missing. Please add it manually. For details, see https://github.com/4J-company/conan-center-index")

        check_min_cppstd(self, "20")
        check_min_cppstd(self, "23")

    def requirements(self):
        self.requires("folly/2024.08.12.00")

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.27]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version])

    def generate(self):
        toolchain = CMakeToolchain(self)
        toolchain.presets_prefix = "mr-manager"
        toolchain.generate()
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

