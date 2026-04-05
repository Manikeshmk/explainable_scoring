#!/usr/bin/env python3
"""
combine_analytics.py
Combines multiple analytics JSON files from different classes into one master file
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def load_json(filepath):
    """Load JSON file safely"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return None

def merge_analytics_data(data_list):
    """
    Merge multiple analytics JSON files
    
    Handles formats:
    - Object-based (email keys): {email: {data}, ...}
    - Array-based: [{student_name, email, data}, ...]
    """
    merged = {
        'timestamp': datetime.now().isoformat(),
        'total_students': 0,
        'classes': [],
        'anomalies': {},
        'peer_comparison': {},
        'concept_mastery': {},
        'momentum': {},
        'learning_curves': {},
        'coverage_metrics': {},
    }
    
    class_info = {}
    
    for idx, data in enumerate(data_list):
        if not data:
            continue
        
        class_name = data.get('class_name', f'Class_{idx+1}')
        class_info[class_name] = {
            'timestamp': data.get('timestamp', 'unknown'),
            'student_count': data.get('student_count', 0)
        }
        
        # Merge each section
        sections = ['anomalies', 'peer_comparison', 'concept_mastery', 'momentum', 'learning_curves', 'coverage_metrics']
        
        for section in sections:
            section_data = data.get(section, {})
            
            if not section_data:
                continue
            
            # Handle both formats
            if isinstance(section_data, dict):
                # Already in object format with email keys
                for email, item_data in section_data.items():
                    if isinstance(item_data, dict):
                        # Add class tracking
                        item_data['class'] = class_name
                        merged[section][email] = item_data
                        
            elif isinstance(section_data, list):
                # Array format - convert to object with email keys
                for item in section_data:
                    if isinstance(item, dict):
                        email = item.get('email', item.get('student_name', 'unknown'))
                        item['class'] = class_name
                        merged[section][email] = item
        
        merged['total_students'] += class_info[class_name]['student_count']
    
    merged['classes'] = class_info
    return merged

def combine_json_files(input_files, output_file='combined_analytics.json', class_names=None):
    """
    Combine multiple JSON files
    
    Usage:
        combine_json_files(
            ['class1.json', 'class2.json', 'class3.json'],
            output_file='all_classes.json',
            class_names=['Class A', 'Class B', 'Class C']
        )
    """
    
    print("\n" + "="*60)
    print("  Analytics JSON Combiner")
    print("="*60)
    
    # Load all files
    print(f"\n📂 Loading {len(input_files)} JSON files...")
    data_list = []
    
    for idx, filepath in enumerate(input_files):
        print(f"  [{idx+1}/{len(input_files)}] {filepath}...", end=" ")
        
        if not os.path.exists(filepath):
            print("❌ NOT FOUND")
            continue
        
        data = load_json(filepath)
        if data:
            # Add class name if provided
            if class_names and idx < len(class_names):
                data['class_name'] = class_names[idx]
            else:
                data['class_name'] = os.path.basename(filepath).replace('.json', '')
            
            data_list.append(data)
            print("✓")
        else:
            print("❌ FAILED")
    
    if not data_list:
        print("❌ No valid JSON files found!")
        return False
    
    print(f"\n✓ Successfully loaded {len(data_list)} files")
    
    # Merge data
    print("\n🔄 Merging analytics data...")
    merged = merge_analytics_data(data_list)
    
    # Save combined file
    print(f"\n💾 Saving combined file: {output_file}")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=2)
        print(f"✅ Saved successfully!")
    except Exception as e:
        print(f"❌ Error saving: {e}")
        return False
    
    # Print summary
    print("\n" + "="*60)
    print("  Summary")
    print("="*60)
    print(f"Total Classes: {len(merged['classes'])}")
    print(f"Total Students: {merged['total_students']}")
    print(f"\nClasses merged:")
    for class_name, info in merged['classes'].items():
        print(f"  • {class_name}: {info['student_count']} students ({info['timestamp']})")
    
    print(f"\nAnalytics sections combined:")
    for section in ['anomalies', 'peer_comparison', 'concept_mastery', 'momentum', 'learning_curves', 'coverage_metrics']:
        count = len(merged.get(section, {}))
        print(f"  • {section}: {count} records")
    
    print(f"\n📊 Output file: {os.path.abspath(output_file)}")
    print("="*60 + "\n")
    
    return True

if __name__ == '__main__':
    # Example 1: Combine specific files
    if len(sys.argv) > 2:
        input_files = sys.argv[1:-1]
        output_file = sys.argv[-1]
        combine_json_files(input_files, output_file)
    else:
        # Default example
        print("Usage: python combine_analytics.py class1.json class2.json class3.json output.json\n")
        
        # Or use it like this:
        files = [
            'grading_results_analytics_classA.json',
            'grading_results_analytics_classB.json', 
            'grading_results_analytics_classC.json'
        ]
        class_names = ['Class A (Morning)', 'Class B (Afternoon)', 'Class C (Evening)']
        
        # Only run if files exist
        if all(os.path.exists(f) for f in files):
            combine_json_files(files, 'all_classes_combined.json', class_names)
        else:
            print("⚠️  No analytics files found to combine")
