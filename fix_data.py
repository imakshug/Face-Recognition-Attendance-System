import pickle
import numpy as np
import os

print("Fixing face recognition data...")

# Load existing data
with open('data/faces_data.pkl', 'rb') as f:
    faces = pickle.load(f)

with open('data/names.pkl', 'rb') as f:
    names = pickle.load(f)

print(f"Original - Faces: {faces.shape}, Names: {len(names)}")
print(f"Unique names: {set(names)}")

# Clean names - remove any corrupted entries
clean_names = []
valid_names = {'Pragati', 'Anshita', 'Akshita', 'Shivi'}  # Add other valid names here

for name in names:
    if isinstance(name, str) and name in valid_names:
        clean_names.append(name)

print(f"Clean names length: {len(clean_names)}")
print(f"Clean unique names: {set(clean_names)}")

# Determine the minimum length to match
min_length = min(len(faces), len(clean_names))
print(f"Using minimum length: {min_length}")

# Truncate both to the same length
faces_fixed = faces[:min_length]
names_fixed = clean_names[:min_length]

print(f"Fixed - Faces: {faces_fixed.shape}, Names: {len(names_fixed)}")

# Backup original files
if not os.path.exists('data/backup/'):
    os.makedirs('data/backup/')

# Backup
with open('data/backup/faces_data_backup.pkl', 'wb') as f:
    pickle.dump(faces, f)
with open('data/backup/names_backup.pkl', 'wb') as f:
    pickle.dump(names, f)

# Save fixed data
with open('data/faces_data.pkl', 'wb') as f:
    pickle.dump(faces_fixed, f)

with open('data/names.pkl', 'wb') as f:
    pickle.dump(names_fixed, f)

print("✅ Data fixed successfully!")
print(f"✅ Final - Faces: {faces_fixed.shape}, Names: {len(names_fixed)}")
print("✅ Original data backed up to data/backup/")

# Verify the fix
with open('data/faces_data.pkl', 'rb') as f:
    test_faces = pickle.load(f)
with open('data/names.pkl', 'rb') as f:
    test_names = pickle.load(f)

print(f"✅ Verification - Faces: {test_faces.shape}, Names: {len(test_names)}")
if len(test_faces) == len(test_names):
    print("✅ Data is now synchronized!")
else:
    print("❌ Still mismatched - manual intervention needed")
