import pickle
import numpy as np
import os
from datetime import datetime

print("🗑️  Starting Fresh Face Recognition Setup...")
print("=" * 50)

# Create backup directory with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = f"data/backup_complete_{timestamp}"
os.makedirs(backup_dir, exist_ok=True)

# Backup existing data if it exists
if os.path.exists('data/faces_data.pkl'):
    print("📦 Backing up existing face data...")
    with open('data/faces_data.pkl', 'rb') as f:
        old_faces = pickle.load(f)
    with open(f'{backup_dir}/faces_data_backup.pkl', 'wb') as f:
        pickle.dump(old_faces, f)
    print(f"✅ Face data backed up: {old_faces.shape[0]} samples")

if os.path.exists('data/names.pkl'):
    print("📦 Backing up existing names data...")
    with open('data/names.pkl', 'rb') as f:
        old_names = pickle.load(f)
    with open(f'{backup_dir}/names_backup.pkl', 'wb') as f:
        pickle.dump(old_names, f)
    print(f"✅ Names data backed up: {len(old_names)} labels")
    print(f"✅ People were: {set(old_names)}")

# Delete old training data files
print("\n🗑️  Removing old training data...")
if os.path.exists('data/faces_data.pkl'):
    os.remove('data/faces_data.pkl')
    print("✅ Deleted faces_data.pkl")

if os.path.exists('data/names.pkl'):
    os.remove('data/names.pkl')
    print("✅ Deleted names.pkl")

# Create fresh empty files (optional - addFaces.py will create them)
print("\n🆕 System ready for fresh face training!")
print("=" * 50)
print("📋 Next Steps:")
print("1. Run: python addFaces.py")
print("2. Enter the first person's name")
print("3. Collect 100 face samples")
print("4. Repeat for each person you want to add")
print("5. Run: python test.py to start recognition")
print("=" * 50)
print(f"💾 All old data backed up to: {backup_dir}")
print("✅ Fresh start ready!")
