close all, clear all, clc

cd ('D:\OneDrive\School\4A\BME 461\Mobitrack\data\Nov17');
files = {'RA_flx_full', 'LA_flx_full_good', 'RA_flx_small', 'LA_flx_small', 'RA_noise_1', 'LA_noise_1', 'RA_noise_2','LA_noise_2', 'LA_noise_3'};
features = [];
labels = [];

% Load and segment data
for i = 1:length(files)
    file = files(i);
    file = file{1};
    data = load(strcat(file, '.mat'));
    
    [t, roll, pitch] = preprocessData(data);

    % Segment
    segment_inds = segmentData(t, roll, pitch);
    segments = extractSegments(t, roll, pitch, segment_inds);

    % Features
    features_from_file = extract_Features(segments);
    
    
    % Labels
    labels_from_file = csvread(strcat(file, '_labels.csv'));
    
    labels = [labels; labels_from_file];
    features = [features; features_from_file];
end

%% Visualize Features
feature_1 = 2;
feature_2 = 13;

signal_features = [features(labels>0,feature_1), features(labels>0,feature_2)];
noise_features = [features(labels<1,feature_1), features(labels<1,feature_2)];

figure, hold on,
scatter(signal_features(:,1), signal_features(:,2), 'g');
scatter(noise_features(:,1), noise_features(:,2), 'r');
title('Feature Space', 'fontweight', 'bold');
legend('Exercise', 'Noise');
xlabel(strcat('Feature ', int2str(feature_1)));
ylabel(strcat('Feature ', int2str(feature_2)));

%% Train SVM
SVMModel = fitcsvm(features, labels, 'KernelFunction', 'linear');


