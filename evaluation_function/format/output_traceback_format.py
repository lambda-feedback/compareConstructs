def output_diffs(res_msg, ans_msg):
    res_lines = [res_line.strip() for res_line in res_msg.split('\n')]
    ans_lines = [ans_line.strip() for ans_line in ans_msg.split('\n')]
    min_len = min(len(res_lines), len(ans_lines))
    for i in range(min_len):
        diff_idx = find_difference_index(res_lines[i], ans_lines[i])
        if diff_idx != -1:
            res_around_diff = '\n'.join(res_lines[max(0, i - 5):min(i + 5, min_len)])
            ans_around_diff = '\n'.join(ans_lines[max(0, i - 5):min(i + 5, min_len)])
            return f"Difference occurs in line {i} after index {diff_idx}:\nResponse:\n{res_around_diff}\n" \
                   f"Expected:\n{ans_around_diff}"

    if min_len == len(res_lines):
        ans_after_diff = '\n'.join(ans_lines[min_len:min(min_len + 5, len(ans_lines))])
        return f"Answer includes your response but not the same:\nAfter line {min_len}, " \
               f"Expected:\n{ans_after_diff}"
    else:
        res_after_diff = '\n'.join(res_lines[min_len:min(min_len + 5, len(res_lines))])
        return f"Your response includes answer but not the same:\nAfter line {min_len}, " \
               f"the response should be deleted:\n" \
               f"{res_after_diff}"


def find_difference_index(str1, str2):
    min_len = min(len(str1), len(str2))

    for i in range(min_len):
        if str1[i] != str2[i]:
            return i

    if len(str1) != len(str2):
        return min_len

    return -1
