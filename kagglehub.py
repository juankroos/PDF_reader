import kagglehub

# Download latest version
path = kagglehub.dataset_download("abd0kamel/asl-citizen")

print("Path to dataset files:", path)