---
created: 2024-04-10T00:00:00.000Z
---

| 英文函数名                                         | 中文名            | 描述                                     |
| --------------------------------------------- | -------------- | -------------------------------------- |
| `dv.current()`                                | 当前页面信息         | 获取当前脚本正在执行的页面的信息。                      |
| `dv.pages(source)`                            | 页面信息数组         | 返回一个页面对象数据数组，包含匹配给定条件的页面信息。            |
| `dv.pagePaths(source)`                        | 页面路径数组         | 返回一个路径数据数组，包含匹配给定条件的页面的路径。             |
| `dv.page(path)`                               | 页面对象           | 将简单的路径或链接映射为完整页面对象，包含页面的所有字段。          |
| `dv.el(element, text)`                        | 渲染HTML元素       | 在指定的HTML元素内渲染任意文本。                     |
| `dv.header(level, text)`                      | 渲染标题           | 以指定级别渲染文本作为标题。                         |
| `dv.paragraph(text)`                          | 渲染段落           | 以段落形式渲染任意文本。                           |
| `dv.span(text)`                               | 渲染跨度           | 以跨度形式渲染任意文本。                           |
| `dv.list(elements)`                           | 渲染列表           | 渲染一个元素列表。                              |
| `dv.taskList(tasks, groupByFile)`             | 渲染任务列表         | 以列表形式渲染Task对象。                         |
| `dv.table(headers, elements)`                 | 渲染表格           | 渲染一个表格，`headers`为表头，`elements`为表格内容的行。 |
| `dv.markdownTable(headers, values)`           | 渲染Markdown表格   | 与`dv.table()`等效，返回Markdown格式的表格。       |
| `dv.markdownList(values)`                     | 渲染Markdown列表   | 与`dv.list()`等效，返回Markdown格式的列表。        |
| `dv.markdownTaskList(tasks)`                  | 渲染Markdown任务列表 | 与`dv.taskList()`等效，返回Markdown格式的任务列表。  |
| `dv.array(value)`                             | 数据数组转换         | 将给定的值或数组转换为Dataview数据数组。               |
| `dv.fileLink(path, [embed?], [display-name])` | 文件链接转换         | 将文本路径转换为Dataview链接对象。                  |
| `dv.date(text)`                               | 日期转换           | 将文本和链接转换为DateTime对象。                   |
| `dv.duration(text)`                           | 持续时间转换         | 将文本转换为Duration对象。                      |
| `dv.io.csv(path, [origin-file])`              | 加载CSV ⌛        | 异步加载给定路径的CSV文件，返回一个数据对象数组。             |
| `dv.io.load(path, [origin-file])`             | 加载文件内容 ⌛       | 异步加载指定路径的文件内容。                         |
