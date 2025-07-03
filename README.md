# Range Tree Implementation - 1D and 2D

A comprehensive implementation of Range Tree data structures for efficient range queries in 1D and 2D spaces, with performance analysis and visualization tools.

## Description

This project implements Range Tree data structures from scratch for both 1D and 2D cases. Range trees are balanced binary search trees that enable efficient range queries - finding all points within a specified range in logarithmic time.

The implementation provides:
- **1D Range Tree** - for queries on a single dimension
- **2D Range Tree** - for rectangular range queries in 2D space  
- **Performance benchmarking** - time and memory usage analysis
- **Interactive visualization** - graphical representation of query results
- **Scalability testing** - analysis across different dataset sizes

The project demonstrates the theoretical time complexities:
- **1D Range Tree**: O(log n + k) query time, O(n) space
- **2D Range Tree**: O(log² n + k) query time, O(n log n) space

Where n is the number of points and k is the number of points in the result.

## Features

### 🌳 **Data Structure Implementation**
- **Balanced Binary Trees** - automatically balanced tree construction
- **Recursive Range Queries** - efficient logarithmic-time searches
- **Duplicate Handling** - automatic removal of duplicate points
- **Memory-Efficient Storage** - optimized node structure

### 📊 **1D Range Tree Capabilities**
- **Point Storage** - handles integer coordinates
- **Range Queries** - find all points in [x_min, x_max]
- **Binary Search Integration** - uses bisect for efficient searching
- **Sorted Point Arrays** - maintains sorted lists for fast queries

### 🎯 **2D Range Tree Capabilities**
- **Hierarchical Structure** - primary tree on x-coordinates, secondary on y-coordinates
- **Rectangular Queries** - find all points in [x_min, x_max] × [y_min, y_max]
- **Fractional Cascading** - optimized with auxiliary 1D trees
- **Point Collection** - recursive gathering of subtree points

### 🔍 **Performance Analysis**
- **Build Time Measurement** - tree construction performance
- **Query Time Measurement** - range query execution time
- **Memory Usage Profiling** - RAM consumption analysis
- **Scalability Testing** - performance across different dataset sizes

### 📈 **Visualization Tools**
- **1D Query Visualization** - line plots with range highlighting
- **2D Query Visualization** - scatter plots with rectangular ranges
- **Memory Usage Plots** - comparative memory analysis charts
- **Interactive Range Display** - visual feedback for query results
