# Dataset.py
import pandas as pd
from sklearn.model_selection import train_test_split
from modules.Parameter import Parameter

class Dataset:
    target_labels = None
    feature_count = None
    feature_names = None
    X_train = None
    X_test = None
    y_train = None
    y_test = None

    @classmethod
    def load_dataset(cls, path, sampling_strategy=None, tau=200):
        # Load the dataset
        data = pd.read_csv(f'datasets/{path}')
        
        # Extract target feature unique labels
        cls.target_labels = data['insider'].unique()
        
        # Feature count (excluding the target feature)
        cls.feature_count = data.shape[1] - 1  # subtracting the target column
        
        # Map feature names to F0, F1, F2, ...
        feature_columns = [f'F{i}' for i in range(cls.feature_count)]
        cls.feature_names = feature_columns
        data.columns = feature_columns + ['insider']

        # Apply sampling strategy if specified
        if sampling_strategy:
            if sampling_strategy == 'random':
                data = data.sample(n=tau, replace=False, random_state=42)
            elif sampling_strategy == 'stratified':
                # If a class label has less than tau instances, it needs to re-use the instances
                counts = data['insider'].value_counts()
                sample_df_list = []
                for label in cls.target_labels:
                    n_samples = min(counts[label], tau)
                    sampled_data = data[data['insider'] == label].sample(n=n_samples, replace=True, random_state=42)
                    sample_df_list.append(sampled_data)
                data = pd.concat(sample_df_list).sample(frac=1).reset_index(drop=True)  # Shuffle the dataset
        
        # Split the dataset into train and test sets
        cls.X_train, cls.X_test, cls.y_train, cls.y_test = train_test_split(
            data[feature_columns], data['insider'], test_size=0.2, random_state=42)