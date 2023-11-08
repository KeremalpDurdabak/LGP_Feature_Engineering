import pandas as pd
from sklearn.model_selection import train_test_split

class Dataset:
    def __init__(self, dataset_name):
        # Initialize attributes
        self.target_labels = None
        self.feature_count = None
        self.feature_names = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
        # Load and process the dataset
        self.load_dataset(dataset_name)
        
    def load_dataset(self, dataset_name):
        # Load the dataset
        data = pd.read_csv(f'datasets/{dataset_name}')
        
        # Extract target feature unique labels
        self.target_labels = data['insider'].unique()
        
        # Feature count (excluding the target feature)
        self.feature_count = data.shape[1] - 1  # subtracting the target column
        
        # Map feature names to F0, F1, F2, ...
        feature_columns = [f'F{i}' for i in range(self.feature_count)]
        self.feature_names = feature_columns
        data.columns = feature_columns + ['insider']
        
        # Split the dataset into train and test sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            data[feature_columns], data['insider'], test_size=0.2, random_state=42)
