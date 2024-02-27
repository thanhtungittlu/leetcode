
import copy


def productExceptSelf(nums):
    n = len(nums)
    left_products = [1] * n
    right_products = [1] * n
    left_product = 1
    for i in range(1, n):
        left_product *= nums[i-1]
        left_products[i] = left_product
    right_product = 1
    for i in range(n-2,-1,-1):
        right_product *= nums[i+1]
        right_products[i] = right_product

    res = [left_products[i] * right_products[i] for i in range(n)]
    return res



nums = [2,4,1,4]
print(productExceptSelf(nums))
