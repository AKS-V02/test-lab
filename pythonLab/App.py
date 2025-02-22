from typing import List


class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        n: List[int] = []
        for i in nums:
            if i in n:
                return True
            else:
                n.append(i)
        return False
            
print(Solution.hasDuplicate(self="", nums=[1,2,3,4]))