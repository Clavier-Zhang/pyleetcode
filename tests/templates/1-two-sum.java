class Solution {
    public int[] twoSum(int[] nums, int target) {
        int[] result = new int[2];
        if (nums == null || nums.length < 2) return result;
        Map<Integer,Integer> m = new HashMap();
        for (int i = 0; i < nums.length; i++) {
            if (m.containsKey(target-nums[i])) {
                result[0] = m.get(target-nums[i]);
                result[1] = i;
                return result;
            }
            m.put(nums[i], i);
        }
        return result;
    }
}
/**
 * Test Area
 * This will not be submitted to Leetcode
 * Sample Test Case:
 * [2,7,11,15]
 * 9
 */
