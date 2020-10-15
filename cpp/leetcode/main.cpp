#include <iostream>
#include <vector>
#include <algorithm>

std::vector<std::vector<int>> threeSum(std::vector<int> &nums) {
    std::vector<std::vector<int>> ans;
    if (nums.size() < 3) return ans;
    std::sort(nums.begin(), nums.end());
    if (nums[0] > 0 || nums[nums.size() - 1] < 0) {
        return ans;
    }
    int i = 0;
    while (i < nums.size()) {
        if (nums[i] > 0) break;
        int left = i + 1, right = nums.size() - 1;
        while (left < right) {

            long long y = static_cast<long long>(nums[i]);
            long long x = static_cast<long long>(nums[left]);
            long long z = static_cast<long long>(nums[right]);
            if (x + y > 0 - z)
                right--;
            else if (x + y < 0 - z)
                left++;
            else {
                ans.push_back({nums[i], nums[left], nums[right]});
                // 相同的left和right不应该再次出现，因此跳过
                while (left < right && nums[left] == nums[left + 1])
                    left++;
                while (left < right && nums[right] == nums[right - 1])
                    right--;
                left++;
                right--;
            }
        }
        // 避免nums[i]作为第一个数重复出现
        while (i + 1 < nums.size() && nums[i] == nums[i + 1])
            i++;
        i++;
    }
    return ans;
}


std::vector<std::vector<int>> fourSum(std::vector<int> &nums, int target) {
    std::vector<std::vector<int>> ans;
    if (nums.size() < 4) {
        return ans;
    }
    std::sort(nums.begin(), nums.end());
    if (nums[0] > target || nums[nums.size() - 1] < target) {
        return ans;
    }

    for (int i = 0; i < nums.size(); i++) {
        if (nums[i] > target) {
            break;
        }
        if (i > 0 && nums[i] == nums[i - 1]) {
            continue;
        }
//        if (i + 1 < nums.size() && nums[i] == nums[i + 1]) {
//            continue;
//        }

        for (int j = i + 1; j < nums.size(); j++) {
            if (j > i + 1 && nums[j] == nums[j - 1]) {
                continue;
            }
//            if (j + 1 < nums.size() && nums[j] == nums[j + 1]) {
//                continue;
//            }
            int c = j + 1;
            int d = nums.size() - 1;

            while (c < d) {
                int sum = nums[i] + nums[j] + nums[c] + nums[d];
                if (sum < target) {
//                    if (nums[c] == nums[c + 1]) {
//                        c++;
//                    }
                    c++;
                } else if (sum > target) {
//                    if (nums[d] == nums[d - 1]) {
//                        d--;
//                    }
                    d--;
                } else {
                    ans.emplace_back(std::vector<int>{nums[i], nums[j], nums[c], nums[d]});
                    if (nums[c] == nums[c + 1]) {
                        c++;
                    }
                    if (nums[d] == nums[d - 1]) {
                        d--;
                    }
                    c++;
                    d--;
                }
            }
        }
    }

    return ans;
}


int main() {
//    std::vector<int> nums{1, 0, -1, 0, -2, 2};
//    std::vector<int> nums{0, 0, 0, 0};
//    std::vector<int> nums{-3, -2, -1, 0, 0, 1, 2, 3};
    std::vector<int> nums{1, -2, -5, -4, -3, 3, 3, 5};
    auto res = fourSum(nums, 0);

    return 0;
}