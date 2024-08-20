def output_diffs(res_msg, ans_msg):
    res_lines = res_msg.split('\n')
    ans_lines = ans_msg.split('\n')
    if len(res_lines) < 10 and len(ans_lines) < 10 and len(res_msg) < 100 and len(ans_msg) < 100:
        return f"Response:\n{res_msg}\nAnswer:\n{ans_msg}"
    else:
        min_len = min(len(res_msg), len(ans_msg))
        for i in range(min_len):
            if res_msg[i] != ans_msg[i]:
                return f"Difference at index {i} is '{res_msg[max(0, i - 10):min(i + 10, min_len)]}'"
        return "Strings are identical" if len(res_msg) == len(ans_msg) else \
            f"Difference starts at index {min_len}:\nResponse after index {min_len}:\n" \
            f"{res_msg[max(0, min_len - 5): min(len(res_msg), min_len + 5)]}\n" \
            f"Answer after index {min_len}:\n{ans_msg[max(0, min_len - 5): min(len(ans_msg), min_len + 5)]}"
