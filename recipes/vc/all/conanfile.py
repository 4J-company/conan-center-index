from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, replace_in_file, rmdir
from conan.tools.scm import Version, Git
import os

required_conan_version = ">=2.1"


class VcConan(ConanFile):
    name = "vc"
    description = "SIMD Vector Classes for C++."
    license = "BSD-3-Clause"
    version = "1.4.3-4j"
    topics = ("simd", "vectorization", "parallel", "sse", "avx", "neon")
    homepage = "https://github.com/4J-company/Vc"
    url = "https://github.com/4J-company/conan-center-index"
    package_type = "static-library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "fPIC": [True, False],
    }
    default_options = {
        "fPIC": True,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self, src_folder="src")

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, 11)

    def source(self):
        git = Git(self)
        git.clone("https://github.com/4J-company/Vc.git", ".")
        git.checkout("467f75b85bdf88c955b3925292b7be0f5efb20bd")

    def generate(self):
        tc = CMakeToolchain(self)
        if Version(self.version) < "1.4.5": # pylint: disable=conan-condition-evals-to-constant
            tc.cache_variables["CMAKE_POLICY_VERSION_MINIMUM"] = "3.5" # CMake 4 support

        if self.settings.os == "Macos" and self.settings.arch == "x86_64":
            # set a compatible baseline with macs from 2015 onwards
            tc.cache_variables["TARGET_ARCHITECTURE"] = "broadwell"
        tc.generate()

    def _patch_sources(self):
        cmakelists = os.path.join(self.source_folder, "CMakeLists.txt")
        replace_in_file(self, cmakelists, "AddCompilerFlag(\"-fPIC\" CXX_FLAGS libvc_compile_flags)", "")

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Vc")
        self.cpp_info.set_property("cmake_target_name", "Vc::Vc")
        self.cpp_info.libs = ["Vc"]
