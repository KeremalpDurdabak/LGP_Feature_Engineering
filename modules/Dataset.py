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
                data = data.sample(n=tau, replace=False)
            elif sampling_strategy == 'equal':
                samples_per_class = tau // len(cls.target_labels)
                remaining_samples = tau % len(cls.target_labels)
                sampled_data = []

                for label in cls.target_labels:
                    class_data = data[data['insider'] == label]
                    n_samples = samples_per_class + (1 if remaining_samples > 0 else 0)
                    remaining_samples -= 1
                    sampled_data.append(class_data.sample(n=n_samples, replace=True))

                data = pd.concat(sampled_data).sample(frac=1).reset_index(drop=True)
            elif sampling_strategy == 'stratified':
                # Stratified sampling
                X = data[feature_columns]
                y = data['insider']
                X_sample, _, y_sample, _ = train_test_split(X, y, train_size=tau, stratify=y, random_state=42)
                data = pd.concat([X_sample, y_sample], axis=1)

        # Split the dataset into train and test sets
        cls.X_train, cls.X_test, cls.y_train, cls.y_test = train_test_split(
            data[feature_columns], data['insider'], test_size=0.2)