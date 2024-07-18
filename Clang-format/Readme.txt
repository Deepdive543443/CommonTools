这个文件夹包含了clang format 14.0.6 和17.0.6两个版本的build，以及一个根据代码规范修改过的配置文件.config（待完善）
可以运行在Ubuntu1806 LTS环境下，可以在VSCode中配合插件高效率地格式化 C/C++ 代码

编译方式参考 
(Win MSVC)：
cmake -DCMAKE_INSTALL_PREFIX=install -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DLLVM_TARGETS_TO_BUILD="" -DLLVM_INCLUDES_EXAMPLES=OFF -DLLVM_INCLUDES_TESTS=OFF -DLLVM_INCLUDES_DOCS=OFF -DLLVM_ENABLE_PROJECTS=clang -A x64 -Thost=x64 ..\llvm

(GCC)：
https://github.com/Tencent/ncnn/blob/824b79a3144cca500e099b232d6c1bf1ff0d43b3/.github/workflows/code-format.yml#L34
