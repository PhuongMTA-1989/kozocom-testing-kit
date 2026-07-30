# Prompt Testing

Thư mục này chứa các prompt hỗ trợ quy trình QA/Testing.

| File | Mục đích |
|---|---|
| `prompt_01_generate_requirements.txt` | Phân tích requirement và xác định phạm vi kiểm thử. |
| `prompt_02_generate_test_cases.txt` | Sinh manual test case từ requirement. |
| `prompt_03_generate_api_tests.txt` | Sinh test case hoặc kịch bản kiểm thử API. |
| `prompt_04_generate_test_data.txt` | Tạo test data phục vụ kiểm thử. |
| `prompt_05_convert_manual_to_automation.txt` | Chuyển manual test case thành kịch bản automation. |

## Cách sử dụng

1. Mở file prompt phù hợp với mục đích.
2. Thay các phần nằm trong dấu `[]` bằng thông tin dự án thực tế.
3. Dán prompt vào công cụ AI đang sử dụng.
4. Kiểm tra và điều chỉnh kết quả trước khi dùng cho dự án.

> Lưu ý: Không đưa thông tin nhạy cảm như mật khẩu, token, dữ liệu khách hàng hoặc thông tin Production vào prompt.
