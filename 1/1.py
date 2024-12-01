from collections import Counter

def read_file():
    with open("1.in", mode="r") as f:
        content = f.read()
        nums = [int(n) for n in content.split()]
        return nums

def get_distance(left, right):
    assert (len(left) == len(right))
    total_distance = 0
    for (n1, n2) in zip(left, right):
        total_distance += abs(n1 - n2)
    return total_distance

def get_similarity(left, right):
    counts = Counter(right)
    total_similarity = 0
    for num in left:
        total_similarity += (num * counts[num])
    return total_similarity

def main():
    nums = read_file()
    i = 0
    left_nums = list()
    right_nums = list()
    while (i < len(nums)):
        is_left = (i & 1 == 0)
        if (is_left):
            left_nums.append(nums[i])
        else:
            right_nums.append(nums[i])
        i += 1
    left_nums.sort()
    right_nums.sort()
    #get_distance(left_nums, right_nums)
    return get_similarity(left_nums, right_nums)

if __name__ == "__main__":
    print(main())
    
