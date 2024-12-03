import unittest 

def read_file(filename):
    with open(filename, mode="r") as f:
        content = f.read().strip()
        return content

def is_safe_report_increasing(report):
    min_diff = 1
    max_diff = 3
    for i in range(1, len(report)):
        cur = report[i]
        prev = report[i-1]
        diff = abs(cur - prev)
        if (not (min_diff <= diff <= max_diff)):
            return False
        if (prev > cur):
            return False
    return True

def is_safe_report_decreasing(report):
    min_diff = 1
    max_diff = 3
    for i in range(1, len(report)):
        cur = report[i]
        prev = report[i-1]
        diff = abs(cur - prev)
        if (not (min_diff <= diff <= max_diff)):
            return False
        if (prev < cur):
            return False
    return True

def is_safe_report(report):
    return (
        is_safe_report_increasing(report) or
        is_safe_report_decreasing(report)
    )

def is_safe_report_dampen(report):
    for i in range(len(report)):
        dampened_report = report.copy()
        dampened_report.pop(i)
        if (is_safe_report(dampened_report)):
            return True
    return False

def main():
    content = read_file("2.in")
    reports = [[int(n) for n in report.split()] for report in content.split("\n")]
    num_safe_reports = 0
    for report in reports:
        if (is_safe_report_dampen(report)):
            num_safe_reports += 1
    return num_safe_reports

if __name__ == "__main__":
    result = main()
    print(result)
