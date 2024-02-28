def maxProduct(nums: list) -> int:
    # Initialize max_product and min_product to the first element
    max_product = min_product = result = nums[0]
    
    for num in nums[1:]:
        # If num is negative, swap max_product and min_product
        if num < 0:
            max_product, min_product = min_product, max_product
        
        # Update max_product and min_product for the current element
        max_product = max(num, max_product * num)
        min_product = min(num, min_product * num)
        
        # Update the overall result
        result = max(result, max_product)
    
    return result


nums = [2,-5,-2,-4,3]
print(maxProduct(nums))