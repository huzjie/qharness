# Key Redaction

# 密钥脱敏

正则抹掉 sk/token/secret/password/Bearer/ghp_ 等敏感串。

## 复用要点

日志和审计落盘前必须先脱敏；测试里要断言日志不含明文密钥。
