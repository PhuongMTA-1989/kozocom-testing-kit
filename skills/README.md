# QC Testing Skills

Thư mục này chứa các skill hỗ trợ quy trình QA/Testing theo định dạng Kozocom.

## Danh sách skills

### `generate-kozocom-testcase`

Tạo file testcase Excel theo template Kozocom từ requirement, user story, UI flow, API specification hoặc bug report.

**Thành phần:**

- `SKILL.md`: Hướng dẫn sử dụng skill.
- `assets/kozocom-testcase-template.xlsx`: Template file testcase.
- `references/input-schema.md`: Cấu trúc thông tin đầu vào.
- `references/template-mapping.md`: Quy tắc mapping dữ liệu vào template.
- `scripts/render_testcase_workbook.py`: Script hỗ trợ tạo và kiểm tra file testcase.

### `generate-kozocom-checklist`

Tạo file checklist Excel phục vụ kiểm thử, QA handover hoặc kiểm tra mức độ sẵn sàng trước khi release.

**Thành phần:**

- `SKILL.md`: Hướng dẫn sử dụng skill.
- `assets/checklist-template.xlsx`: Template file checklist.
- `references/input-schema.md`: Cấu trúc thông tin đầu vào.
- `scripts/render_checklist_workbook.py`: Script hỗ trợ tạo và kiểm tra file checklist.

### `log-bug`

Tạo bug report rõ ràng, có thể tái hiện và phù hợp để nhập lên Backlog.

**Output bao gồm:**

- Issue title
- Test item và thông tin môi trường
- Preconditions
- Steps to reproduce
- Actual result
- Expected result
- Severity, impact và workaround
- Evidence

## Cấu trúc thư mục

```text
skills/
├── generate-kozocom-testcase/
├── generate-kozocom-checklist/
├── log-bug/
└── README.md
```

## Cài đặt và sử dụng skills

Folder `skills/` trong repository này là nơi lưu trữ và chia sẻ skill. Để AI tool tự nhận diện skill, hãy copy folder skill cần dùng vào đúng thư mục của tool đó.

### Claude Code

Copy folder skill vào `.claude/skills/` của project:

```text
your-project/
└── .claude/
    └── skills/
        └── log-bug/
            └── SKILL.md
```

Hoặc cài cho tất cả project trên máy:

```text
~/.claude/skills/log-bug/
```

Mở Claude Code tại project và gọi skill:

```text
/log-bug
```

### Codex

Copy folder skill vào `.agents/skills/` của project:

```text
your-project/
└── .agents/
    └── skills/
        └── log-bug/
            └── SKILL.md
```

Hoặc cài cho tất cả project trên máy:

```text
~/.agents/skills/log-bug/
```

Mở Codex tại project và gọi skill:

```text
$log-bug
```

Ví dụ:

```text
$log-bug Create a Backlog bug report from this screenshot and test result.
```

### Các AI tool khác

Nếu tool không hỗ trợ tự động nạp skill từ thư mục:

1. Mở file `SKILL.md` của skill cần dùng.
2. Đính kèm hoặc sao chép nội dung file vào cuộc trò chuyện.
3. Cung cấp requirement, testcase, screenshot, log hoặc dữ liệu đầu vào liên quan.
4. Đính kèm thêm file trong `assets/`, `references/` hoặc `scripts/` khi cần.

## Lưu ý bảo mật

Không đưa mật khẩu, API token, dữ liệu khách hàng, thông tin cá nhân hoặc dữ liệu Production chưa được che giấu vào prompt, testcase, checklist hoặc bug report.
