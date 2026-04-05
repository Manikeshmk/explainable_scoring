"""
Stanford SQuAD Dataset Download and Preparation
Downloads and converts SQuAD to ExplainGrade format
"""

import json
import pandas as pd
import urllib.request
import os
from pathlib import Path


def download_squad_dataset(version='dev', subset_size=None):
    """
    Download Stanford SQuAD dataset
    
    Args:
        version: 'dev' or 'train'
        subset_size: Limit to N articles (None for all)
    
    Returns:
        DataFrame with columns: question, desired_answer, student_answer, context
    """
    print(f"📥 Downloading SQuAD {version} dataset...")
    
    url = f'https://raw.githubusercontent.com/rajpurkar/SQuAD-explorer/master/dataset/{version}-v2.0.json'
    
    try:
        filename = f'squad_{version}_raw.json'
        urllib.request.urlretrieve(url, filename)
        print(f"✓ Downloaded: {filename}")
    except Exception as e:
        print(f"✗ Download failed: {e}")
        return None
    
    # Convert to DataFrame
    with open(filename) as f:
        squad_data = json.load(f)
    
    rows = []
    article_count = 0
    
    for article in squad_data['data']:
        if subset_size and article_count >= subset_size:
            break
        
        article_title = article.get('title', 'Unknown')
        
        for paragraph in article['paragraphs']:
            context = paragraph['context']
            
            for qa in paragraph['qas']:
                question = qa['question']
                
                if qa['answers']:
                    # Use first answer as reference
                    reference = qa['answers'][0]['text']
                    
                    rows.append({
                        'question': question,
                        'desired_answer': reference,
                        'student_answer': reference,  # Perfect answer
                        'context': context[:500],  # Truncate for display
                        'domain': 'General Knowledge',
                        'source': 'Stanford SQuAD',
                        'article': article_title,
                        'expected_score': 10  # Perfect answer scores 10
                    })
        
        article_count += 1
    
    df = pd.DataFrame(rows)
    
    # Save as CSV
    output_file = f'squad_{version}_converted.csv'
    df.to_csv(output_file, index=False)
    print(f"✓ Converted to CSV: {output_file}")
    print(f"  Total Q&A pairs: {len(df)}")
    print(f"  Articles: {article_count}")
    
    return df


def create_test_variations(df, variation_count=3):
    """
    Create answer variations (wrong, partial, correct)
    to test grader robustness
    
    Args:
        df: DataFrame with Q&A pairs
        variation_count: Number of variations per answer
    
    Returns:
        DataFrame with variations
    """
    print(f"\n🔄 Creating answer variations...")
    
    variations = []
    
    for idx, row in df.head(100).iterrows():  # Use first 100 for testing
        question = row['question']
        reference = row['desired_answer']
        
        # 1. Perfect answer
        variations.append({
            'question': question,
            'desired_answer': reference,
            'student_answer': reference,
            'expected_score': 10,
            'variation_type': 'perfect',
            'context': row.get('context', ''),
            'source': 'SQuAD'
        })
        
        # 2. Partial answer (shortened)
        if len(reference) > 10:
            partial = reference[:len(reference)//2]
            variations.append({
                'question': question,
                'desired_answer': reference,
                'student_answer': partial,
                'expected_score': 6,
                'variation_type': 'partial',
                'context': row.get('context', ''),
                'source': 'SQuAD'
            })
        
        # 3. Paraphrased answer
        words = reference.split()
        if len(words) > 2:
            paraphrased = ' '.join(words[::-1])  # Reverse word order
            variations.append({
                'question': question,
                'desired_answer': reference,
                'student_answer': paraphrased,
                'expected_score': 5,
                'variation_type': 'paraphrased',
                'context': row.get('context', ''),
                'source': 'SQuAD'
            })
    
    var_df = pd.DataFrame(variations)
    var_df.to_csv('squad_test_variations.csv', index=False)
    print(f"✓ Created {len(var_df)} test variations")
    print(f"  - Perfect answers: {len(var_df[var_df['variation_type']=='perfect'])}")
    print(f"  - Partial answers: {len(var_df[var_df['variation_type']=='partial'])}")
    print(f"  - Paraphrased answers: {len(var_df[var_df['variation_type']=='paraphrased'])}")
    
    return var_df


def merge_with_mohler(squad_df=None):
    """
    Combine SQuAD with existing Mohler dataset
    for comprehensive testing
    
    Args:
        squad_df: SQuAD DataFrame (optional)
    
    Returns:
        Combined DataFrame
    """
    print("\n📦 Merging datasets...")
    
    try:
        # Load Mohler data
        mohler_df = pd.read_csv('mohler_dataset_edited.csv')
        mohler_df['domain'] = 'Software Engineering'
        
        if squad_df is not None:
            # Combine
            combined = pd.concat([
                mohler_df[['question', 'desired_answer', 'student_answer', 'score_avg', 'domain']],
                squad_df[['question', 'desired_answer', 'student_answer', 'domain']].head(50)
            ], ignore_index=True)
            
            combined.to_csv('combined_test_dataset.csv', index=False)
            print(f"✓ Combined dataset created")
            print(f"  - Mohler entries: {len(mohler_df)}")
            print(f"  - SQuAD entries: 50")
            print(f"  - Total: {len(combined)}")
            
            return combined
        else:
            return mohler_df
    
    except FileNotFoundError:
        print("✗ Mohler dataset not found")
        return None


def main():
    """Download and prepare all datasets"""
    print("=" * 60)
    print("Stanford SQuAD Dataset Download & Preparation")
    print("=" * 60)
    
    # Download dev set (smaller, faster)
    squad_dev = download_squad_dataset(version='dev', subset_size=20)
    
    if squad_dev is not None:
        # Create variations
        variations = create_test_variations(squad_dev)
        
        # Merge with Mohler
        combined = merge_with_mohler(squad_dev)
        
        print("\n" + "=" * 60)
        print("✅ SETUP COMPLETE")
        print("=" * 60)
        print("\nGenerated files:")
        print("  1. squad_dev_converted.csv - SQuAD test data")
        print("  2. squad_test_variations.csv - Test variations")
        print("  3. combined_test_dataset.csv - Mohler + SQuAD")
        print("\nReady to test with local_grader.py!")
        print("\nExample usage:")
        print("  python local_grader.py")
        print("  python metrics.py  # Calculate performance scores")
    else:
        print("\n✗ Setup failed")


if __name__ == "__main__":
    main()
