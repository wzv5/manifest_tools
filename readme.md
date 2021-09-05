# Manifest Tools

一组用于操作 Windows PE manifest 资源的工具。

* mtadd：向 exe 中添加 manifest 资源
  * 可传入一个或多个 manifest 文件名
  * 引用 `manifests` 目录中的文件只需传入文件名，如 `ui`
  * `base` 为简便参数，用于替代 `nouac ui win10`
* mtget：读取指定 exe 中的 manifest 资源
* mtnouac：禁止指定 exe 自动申请管理员权限（替换 `requireAdministrator` 为 `asInvoker`）

依赖 Windows SDK 中的 `mt.exe`，优先在当前目录下寻找，如果不存在，则自动寻找本地安装的 Windows SDK。
