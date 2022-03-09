# Quiz) 팩토리얼을 구하는 재귀함수를 작성하시오.
# - 팩토리얼 : 주어진 수보다 작거나 같은 모든 양의 정수의 곱
#      n! = n x (n - 1) x (n - 2) x ... 1

#  예) 4! = 4 x 3 x 2 x 1 = 24
#      3! = 3 x 2 x 1 = 6
#      2! = 2 x 1 = 2
#      1! = 1
#      0! = 1

# 힌트
# 1) n! = n x (n - 1)! 과 같다.
# 2) 4! = 4 x (4 - 1)! 과 같다.
# 3) 1! 과 0! 은 1 이다.

def factorial(n):
    if n > 1:
        return n * factorial(n - 1)
    else:
        return 1

result = factorial(4)
print(result) # 24