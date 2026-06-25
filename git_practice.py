"""
git_practice.py

一个用于练习 Git 操作的示例 Python 文件。
内容包含多个独立的小模块（数据结构、算法、工具函数等），
你可以随意修改、增删，然后用 git 来练习 add / commit / diff / log / branch 等操作。

作者: 练习用
"""

from __future__ import annotations

import math
import random
import datetime
from dataclasses import dataclass, field
from typing import Iterable, Callable, Any


# ----------------------------------------------------------------------------
# 第一部分：基础数学工具
# ----------------------------------------------------------------------------
def is_prime(n: int) -> bool:
    """判断一个整数是否为素数。"""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    print('123')
    return True


def primes_up_to(limit: int) -> list[int]:
    """返回小于等于 limit 的所有素数（埃拉托色尼筛法）。"""
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
#    wetqewrefasdfas
    return [i for i, ok in enumerate(sieve) if ok]


def gcd(a: int, b: int) -> int:
    """求最大公约数（欧几里得算法）。"""
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a: int, b: int) -> int:
    """求最小公倍数。"""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def factorial(n: int) -> int:
    """计算阶乘（递归实现）。"""
    if n < 0:
        raise ValueError("阶乘的参数必须为非负整数")
    return 1 if n <= 1 else n * factorial(n - 1)


def fibonacci(n: int) -> list[int]:
    """返回前 n 个斐波那契数。"""
    seq: list[int] = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq


# ----------------------------------------------------------------------------
# 第二部分：字符串处理工具
# ----------------------------------------------------------------------------
def reverse_words(text: str) -> str:
    """反转句子中单词的顺序。"""
    return " ".join(reversed(text.split()))


def is_palindrome(text: str) -> bool:
    """判断字符串是否为回文（忽略大小写和非字母数字字符）。"""
    cleaned = [c.lower() for c in text if c.isalnum()]
    return cleaned == cleaned[::-1]


def count_chars(text: str) -> dict[str, int]:
    """统计每个字符出现的次数。"""
    result: dict[str, int] = {}
    for ch in text:
        result[ch] = result.get(ch, 0) + 1
    return result


def to_snake_case(text: str) -> str:
    """把驼峰命名转换为蛇形命名。"""
    out: list[str] = []
    for i, ch in enumerate(text):
        if ch.isupper() and i > 0:
            out.append("_")
        out.append(ch.lower())
    return "".join(out)


# ----------------------------------------------------------------------------
# 第三部分：排序算法
# ----------------------------------------------------------------------------
def bubble_sort(items: list[int]) -> list[int]:
    """冒泡排序（返回新列表，不修改原列表）。"""
    arr = items[:]
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def quick_sort(items: list[int]) -> list[int]:
    """快速排序（递归实现）。"""
    if len(items) <= 1:
        return items
    pivot = items[len(items) // 2]
    left = [x for x in items if x < pivot]
    middle = [x for x in items if x == pivot]
    right = [x for x in items if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def merge_sort(items: list[int]) -> list[int]:
    """归并排序。"""
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])
    return _merge(left, right)


def _merge(left: list[int], right: list[int]) -> list[int]:
    """合并两个有序列表。"""
    result: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ----------------------------------------------------------------------------
# 第四部分：数据类示例（一个简单的学生成绩管理）
# ----------------------------------------------------------------------------
@dataclass
class Student:
    """学生信息。"""

    name: str
    age: int
    scores: dict[str, float] = field(default_factory=dict)

    def average(self) -> float:
        """计算平均分。"""
        if not self.scores:
            return 0.0
        return sum(self.scores.values()) / len(self.scores)

    def best_subject(self) -> str | None:
        """返回分数最高的科目。"""
        if not self.scores:
            return None
        return max(self.scores, key=self.scores.get)


class Classroom:
    """班级，管理多个学生。"""

    def __init__(self, name: str) -> None:
        self.name = name
        self.students: list[Student] = []

    def add_student(self, student: Student) -> None:
        self.students.append(student)

    def class_average(self) -> float:
        if not self.students:
            return 0.0
        return sum(s.average() for s in self.students) / len(self.students)

    def top_student(self) -> Student | None:
        if not self.students:
            return None
        return max(self.students, key=lambda s: s.average())

    def __len__(self) -> int:
        return len(self.students)


# ----------------------------------------------------------------------------
# 第五部分：一些常用的高阶函数工具
# ----------------------------------------------------------------------------
def chunk(items: list[Any], size: int) -> list[list[Any]]:
    """把列表按固定长度切分成多个子列表。"""
    if size <= 0:
        raise ValueError("size 必须为正整数")
    return [items[i:i + size] for i in range(0, len(items), size)]


def flatten(nested: Iterable[Any]) -> list[Any]:
    """把嵌套列表展开成一维列表。"""
    result: list[Any] = []
    for item in nested:
        if isinstance(item, (list, tuple)):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def retry(times: int) -> Callable:
    """一个简单的重试装饰器。"""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error: Exception | None = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001
                    last_error = exc
                    print(f"第 {attempt} 次尝试失败: {exc}")
            if last_error:
                raise last_error
        return wrapper

    return decorator


# ----------------------------------------------------------------------------
# 第六部分：随机数据生成（方便做演示）
# ----------------------------------------------------------------------------
SUBJECTS = ["语文", "数学", "英语", "物理", "化学"]
NAMES = ["张三", "李四", "王五", "赵六", "钱七", "孙八"]


def random_student(seed: int | None = None) -> Student:
    """生成一个随机学生。"""
    if seed is not None:
        random.seed(seed)
    name = random.choice(NAMES)
    age = random.randint(15, 18)
    scores = {sub: round(random.uniform(60, 100), 1) for sub in SUBJECTS}
    return Student(name=name, age=age, scores=scores)


def build_demo_classroom(count: int = 5) -> Classroom:
    """构造一个示例班级。"""
    room = Classroom("练习班")
    for i in range(count):
        room.add_student(random_student(seed=i))
    return room


# ----------------------------------------------------------------------------
# 主程序入口
# ----------------------------------------------------------------------------
def main() -> None:
    print("=" * 50)
    print("Git 练习用示例程序")
    print(f"运行时间: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
    print("=" * 50)

    print("\n[素数] 100 以内的素数:")
    print(primes_up_to(100))

    print("\n[斐波那契] 前 10 个:")
    print(fibonacci(10))

    print("\n[排序] 对随机列表排序:")
    data = [random.randint(1, 50) for _ in range(10)]
    print("原始:", data)
    print("快排:", quick_sort(data))

    print("\n[字符串] 回文检测:")
    for word in ["上海自来水来自海上", "hello", "level"]:
        print(f"  {word!r} -> {is_palindrome(word)}")

    print("\n[班级] 示例班级统计:")
    room = build_demo_classroom()
    print(f"  班级人数: {len(room)}")
    print(f"  班级平均分: {room.class_average():.2f}")
    top = room.top_student()
    if top:
        print(f"  最高分学生: {top.name} (平均分 {top.average():.2f})")


if __name__ == "__main__":
    main()
