# 虎嗅热点新闻抓取工具

抓取虎嗅「24 小时快讯」与「首页推荐文章」，输出为 JSON 与 HTML 两种格式。

## 使用

```bash
# 安装依赖
pip install -r requirements.txt

# 运行（同时生成 output/huxiu_hot_YYYYMMDD_HHMMSS.json 与 .html）
python -m huxiu_scraper.run

# 指定输出路径（会生成同名的 .json 与 .html）
python -m huxiu_scraper.run --output /path/to/out.json
```

## 输出格式

- **JSON**：`moment_feed`（24 小时快讯）、`home_recommended`（首页推荐），便于程序处理。
- **HTML**：与 JSON 同名的 `.html` 文件，用浏览器打开即可简洁查看数据（快讯摘要 + 推荐标题与链接）。

## 注意

- 仅用于学习与个人使用，请遵守虎嗅网 robots.txt 与使用条款。
- 请求间已加延时；若遇 403/429，可自行配置代理或降低请求频率（修改 `huxiu_scraper/config.py` 中的 `REQUEST_DELAY_SECONDS`）。
