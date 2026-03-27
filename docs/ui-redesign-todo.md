# Aniday Class UI Redesign Todo

## Phase 1. System Foundation

- [x] 建立 `Design Context` 并固化到 `AGENTS.md`
- [x] 盘点管理端与家长端主要页面、表格、表单、弹窗和状态
- [x] 抽离全局 design tokens，统一颜色、字号、间距、圆角、阴影、动效
- [x] 接入标题字体与正文字体方案，定义中文排版层级和数字样式
- [x] 建立浅色主题与深色主题 token 映射
- [x] 实现主题切换、主题持久化和首屏无闪烁策略
- [x] 统一 Element Plus 二次主题覆写策略

## Phase 2. Admin Shell And Core Pages

- [x] 重做管理端 `Layout`
- [x] 重做管理端登录页
- [x] 重做 Dashboard
- [x] 建立通用列表页母版
- [x] 重做 `Students`
- [x] 重做 `Scores`
- [x] 重做 `Attendance`
- [x] 重做 `Rankings` 与 `Analysis` 的视觉框架

## Phase 3. Admin Secondary Pages

- [x] 重做 `Classes`
- [x] 重做 `Users`
- [x] 重做 `Subjects`
- [x] 重做 `Semesters`
- [x] 重做 `Logs`
- [x] 重做 `Points` 与 `PointsDisplay` 的系统主题接入
- [x] 重做 `Homework`
- [x] 重做 `Notifications`
- [x] 重做 `Settings`

## Phase 4. Parent Portal

- [x] 建立家长端移动端设计系统
- [x] 重做家长端登录页
- [x] 重做家长端首页 `Home`
- [x] 重做家长端 `Scores`
- [x] 重做家长端 `Notifications`
- [x] 重做家长端 `Homework`

## Phase 5. QA Focus

- [x] 完成全站响应式适配基线
- [x] 完成可访问性与主题验收基线
- [x] 输出视觉回归检查清单

## Visual Regression Checklist

- [ ] 登录页、Layout、Dashboard、Students、Scores、Attendance、Parent Home 桌面与移动端截图比对
- [ ] Light/Dark 两个主题下表格、弹窗、抽屉、图表、表单控件可读性确认
- [ ] 空状态、加载态、接口失败、长文本、超长用户名验证
- [ ] 焦点态、键盘可达性、减少动效策略检查
