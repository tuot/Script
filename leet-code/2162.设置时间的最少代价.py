#
# @lc app=leetcode.cn id=2162 lang=python3
#
# [2162] 设置时间的最少代价
#

# @lc code=start
class Solution:
    def minCostSetTime(self, startAt: int, moveCost: int, pushCost: int, targetSeconds: int) -> int:
        way = []
        if targetSeconds < 60:
            way.append(str(targetSeconds))
        else:
            if targetSeconds <= 99:
                way.append(str(targetSeconds))
            for i in range(1, 100):
                has_second = targetSeconds - i*60
                if has_second > 99:
                    continue
                elif has_second < 0:
                    break
                else:
                    second_str = "0" + \
                        str(has_second) if has_second < 10 else str(has_second)
                    way.append(str(i) + second_str)
        result = []
        for i in way:
            res = len(i) * pushCost
            if int(i[0]) != startAt:
                res += moveCost
            for j in range(1, len(i)):
                if i[j] != i[j-1]:
                    res += moveCost
            result.append(res)
        return min(result)


# @lc code=end

# 150   2 20  1 70
a = [5, 15, 20, 365]
b = Solution().minCostSetTime(*a)
print(b)
