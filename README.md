# 4J-company Conan Center Index

This is a repo with conan packages for 4J-company's projects. It contains packages' recipes and follows the original [conan-center-index](https://github.com/conan-io/conan-center-index)'s structure.

To use 4J-company's packages:
- clone this repo
```
git clone https://github.com/4J-company/conan-center-index.git
```
- setup conan remote
```
conan remote add 4J-company ./conan-center-index --type local-recipes-index
```
- now you can consume packages as usual.

**Note:** for forked packages, `-4j` is added to package version to indicate 4J-company's fork.