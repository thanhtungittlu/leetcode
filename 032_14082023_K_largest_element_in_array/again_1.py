import heapq

"""
Trong Python, heapq là một thư viện cung cấp các chức năng để làm việc với các cấu trúc dữ liệu heap (ngăn xếp ưu tiên). Heap là một dạng cấu trúc dữ liệu có thứ tự đặc biệt, trong đó phần tử đầu tiên (đỉnh heap) luôn có giá trị nhỏ nhất (trong heap tối thiểu) hoặc lớn nhất (trong heap tối đa).

Thư viện heapq trong Python cung cấp các chức năng để thao tác với các heap như:

heapify(iterable): Chuyển đổi một iterable thành một heap trong chỗ.
heappush(heap, element): Thêm một phần tử vào heap và duy trì tính chất heap.
heappop(heap): Loại bỏ và trả về phần tử nhỏ nhất (đầu heap) và duy trì tính chất heap.
heappushpop(heap, element): Thêm một phần tử vào heap, sau đó loại bỏ và trả về phần tử nhỏ nhất.
heapreplace(heap, element): Loại bỏ và trả về phần tử nhỏ nhất, sau đó thêm một phần tử vào heap.
heapq.nlargest(n, iterable): Trả về danh sách chứa n phần tử lớn nhất từ iterable.
heapq.nsmallest(n, iterable): Trả về danh sách chứa n phần tử nhỏ nhất từ iterable.
"""



def findKthLargest(nums, k):
    """
    :type nums: List[int]
    :type k: int
    :rtype: int
    """
    listLarget = heapq.nlargest(k,nums)
    return listLarget[-1]


nums = [3,2,1,5,6,4] 
k = 2

print(findKthLargest(nums,k))