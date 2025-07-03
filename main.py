import random
import time
import matplotlib.pyplot as plt
import numpy as np
from memory_profiler import memory_usage
import bisect

class Node1D:
    """Node for 1D range tree"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.sorted_points = [value]  

class RangeTree1D:
    """1D Range Tree implementation"""
    def __init__(self, points):

        self.points = sorted(list(set(points)))
        if not self.points:
            self.root = None
        else:
            self.root = self._build_tree(self.points)

    def _build_tree(self, points):
        """Build a balanced 1D range tree recursively"""
        if not points:
            return None
        
        median_idx = len(points) // 2
        node = Node1D(points[median_idx])
        
        node.left = self._build_tree(points[:median_idx])
        node.right = self._build_tree(points[median_idx+1:])
        
        if node.left:
            node.sorted_points = node.left.sorted_points + node.sorted_points
            print(node.sorted_points)
        if node.right:
            node.sorted_points = node.sorted_points + node.right.sorted_points
            print(node.sorted_points)
        
        return node
    
    def range_query(self, x_min, x_max):
        """Find all points in the range [x_min, x_max]"""
        if not self.root:
            return []
        
        return self._range_query(self.root, x_min, x_max)
    
    def _range_query(self, node, x_min, x_max):
        """Recursive range query implementation"""
        if not node:
            return []
        
        if node.value < x_min:
            return self._range_query(node.right, x_min, x_max)
        
        if node.value > x_max:
            return self._range_query(node.left, x_min, x_max)
        
        result = []
        
        left_idx = bisect.bisect_left(node.sorted_points, x_min)
        right_idx = bisect.bisect_right(node.sorted_points, x_max)
        
        result = node.sorted_points[left_idx:right_idx]
        return result

class Node2D:
    """Node for 2D range tree"""
    def __init__(self, point):
        self.point = point  # (x, y)
        self.left = None
        self.right = None
        self.y_tree = None

class RangeTree2D:
    """2D Range Tree implementation"""
    def __init__(self, points):
        self.points = [tuple(p) for p in points]
        self.points = sorted(list(set(self.points)))  
        if not self.points:
            self.root = None
        else:
            self.root = self._build_tree(self.points)
    
    def _build_tree(self, points):
        """Build a balanced 2D range tree recursively"""
        if not points:
            return None
        
        points.sort(key=lambda p: p[0])
        
        median_idx = len(points) // 2
        node = Node2D(points[median_idx])
        
        node.left = self._build_tree(points[:median_idx])
        node.right = self._build_tree(points[median_idx+1:])
        
        subtree_points = []
        if node.left:
            self._collect_points(node.left, subtree_points)
            print(self._collect_points(node.left, subtree_points))
        subtree_points.append(node.point)
        if node.right:
            self._collect_points(node.right, subtree_points)
            print(self._collect_points(node.left, subtree_points))
        
        y_points = [p[1] for p in subtree_points]
        node.y_tree = RangeTree1D(y_points)
        
        return node
    
    def _collect_points(self, node, points_list):
        """Helper to collect all points in a subtree"""
        if not node:
            return
        points_list.append(node.point)
        self._collect_points(node.left, points_list)
        self._collect_points(node.right, points_list)
    
    def range_query(self, x_min, x_max, y_min, y_max):
        """Find all points in the 2D range [x_min, x_max] × [y_min, y_max]"""
        if not self.root:
            return []
        
        candidates = []
        self._range_query(self.root, x_min, x_max, y_min, y_max, candidates)
        return candidates
    
    def _range_query(self, node, x_min, x_max, y_min, y_max, result):
        """Recursive 2D range query implementation"""
        if not node:
            return
        
        x = node.point[0]
        
        if x_min <= x <= x_max:
            # 1. Check current node
            y = node.point[1]
            if y_min <= y <= y_max:
                result.append(node.point)
            
            # 2. Search left subtree
            self._range_query(node.left, x_min, x_max, y_min, y_max, result)
            
            # 3. Search right subtree
            self._range_query(node.right, x_min, x_max, y_min, y_max, result)
        
        elif x < x_min:
            self._range_query(node.right, x_min, x_max, y_min, y_max, result)
        
        else: 
            self._range_query(node.left, x_min, x_max, y_min, y_max, result)

def test_1d_range_tree(n_points=50):
    """Test 1D range tree implementation and visualize results"""
    points = [random.randint(20, 100) for _ in range(n_points)]
    
    start_build = time.time()
    tree = RangeTree1D(points)
    build_time = time.time() - start_build
    
    x_min, x_max = 30, 70
    
    start_query = time.time()
    result = tree.range_query(x_min, x_max)
    query_time = time.time() - start_query
    
    print(f"1D Range Tree Results (n={n_points}):")
    print(f"Build time: {build_time:.6f} seconds")
    print(f"Query time: {query_time:.6f} seconds")
    print(f"Found {len(result)} points in range [{x_min}, {x_max}]")
    
    # Visualize the results
    plt.figure(figsize=(10, 4))
    
    # Plot all points
    plt.plot(points, [0] * len(points), 'bo', label='All Points')
    
    # Plot points in range
    plt.plot(result, [0] * len(result), 'ro', label='Points in Range')
    
    # Plot range limits
    plt.axvline(x=x_min, color='g', linestyle='--', label=f'x_min = {x_min}')
    plt.axvline(x=x_max, color='r', linestyle='--', label=f'x_max = {x_max}')
    
    plt.title('1D Range Query Results')
    plt.legend()
    plt.xlabel('Value')
    plt.yticks([])
    plt.grid(True, alpha=0.3)
    plt.show()
    
    return tree, result

def test_2d_range_tree(n_points=50):
    """Test 2D range tree implementation and visualize results"""
    points = [(random.randint(20, 100), random.randint(20, 100)) for _ in range(n_points)]
    
    start_build = time.time()
    tree = RangeTree2D(points)
    build_time = time.time() - start_build
    
    x_min, x_max = 30, 70
    y_min, y_max = 40, 80
    
    start_query = time.time()
    result = tree.range_query(x_min, x_max, y_min, y_max)
    query_time = time.time() - start_query
    
    print(f"2D Range Tree Results (n={n_points}):")
    print(f"Build time: {build_time:.6f} seconds")
    print(f"Query time: {query_time:.6f} seconds")
    print(f"Found {len(result)} points in range [{x_min}, {x_max}] × [{y_min}, {y_max}]")
    
    # Visualize the results
    plt.figure(figsize=(8, 8))
    
    # Extract x and y coordinates
    all_x = [p[0] for p in points]
    all_y = [p[1] for p in points]
    
    result_x = [p[0] for p in result]
    result_y = [p[1] for p in result]
    
    # Plot all points
    plt.scatter(all_x, all_y, color='blue', label='All Points')
    
    # Plot points in range
    plt.scatter(result_x, result_y, color='red', label='Points in Range')
    
    # Plot range limits
    plt.axvline(x=x_min, color='g', linestyle='--', label=f'x_min = {x_min}')
    plt.axvline(x=x_max, color='g', linestyle='--', label=f'x_max = {x_max}')
    plt.axhline(y=y_min, color='r', linestyle='--', label=f'y_min = {y_min}')
    plt.axhline(y=y_max, color='r', linestyle='--', label=f'y_max = {y_max}')
    
    # Highlight the query range
    plt.fill([x_min, x_max, x_max, x_min, x_min],
             [y_min, y_min, y_max, y_max, y_min],
             alpha=0.1, color='green')
    
    plt.title('2D Range Query Results')
    plt.legend()
    plt.xlabel('X Value')
    plt.ylabel('Y Value')
    plt.grid(True, alpha=0.3)
    plt.show()
    
    return tree, result

def analyze_memory_usage():
    """Analyze memory usage for different dataset sizes"""
    sizes = [10, 50, 100, 200, 500, 1000]
    memory_1d = []
    memory_2d = []
    
    for size in sizes:
        # 1D tree memory usage
        points_1d = [random.randint(20, 100) for _ in range(size)]
        memory_usage_1d = memory_usage((RangeTree1D, (points_1d,)), max_usage=True)
        memory_1d.append(memory_usage_1d)
        
        # 2D tree memory usage
        points_2d = [(random.randint(20, 100), random.randint(20, 100)) for _ in range(size)]
        memory_usage_2d = memory_usage((RangeTree2D, (points_2d,)), max_usage=True)
        memory_2d.append(memory_usage_2d)
    
    # Plot memory usage
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, memory_1d, 'o-', label='1D Range Tree')
    plt.plot(sizes, memory_2d, 's-', label='2D Range Tree')
    plt.title('Memory Usage vs Data Size')
    plt.xlabel('Number of Points')
    plt.ylabel('Memory Usage (MB)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    return sizes, memory_1d, memory_2d

# Run the tests
if __name__ == "__main__":
    print("Testing 1D Range Tree...")
    tree_1d, results_1d = test_1d_range_tree(50)
    
    print("\nTesting 2D Range Tree...")
    tree_2d, results_2d = test_2d_range_tree(50)
    
    print("\nAnalyzing Memory Usage...")
    sizes, mem_1d, mem_2d = analyze_memory_usage()
    
