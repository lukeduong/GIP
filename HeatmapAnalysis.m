clear all
close all
workspace;  % Make sure the workspace panel is showing.
format long g;
format compact;
fontSize = 16;

% Get the name of the image the user wants to use.
FileName = 'NitrogenTrialPic.jpg';
folder = pwd;
fullFileName = fullfile(folder, FileName);

% Read in demo image.
rgbImage = imread(fullFileName);
% Get the dimensions of the image.
[rows, columns, numberOfColorChannels] = size(rgbImage);

figure
imshow(rgbImage, []);
impixelinfo;
axis on;
caption = sprintf('Original Color Image\n%s', FileName);
title(caption, 'FontSize', fontSize, 'Interpreter', 'None');
hp = impixelinfo(); % Set up status line to see values when you mouse over the image.

% Get an indexed image.
numberOfColorClasses = 7;
[indexedImage, customColorMap] = rgb2ind(rgbImage, numberOfColorClasses);

figure
imshow(indexedImage, []);
colormap(customColorMap);
colorbar;
caption = sprintf('Color Segmentation Mask Image');
title(caption, 'FontSize', fontSize, 'Interpreter', 'None');
impixelinfo;
axis('on', 'image');
drawnow;

figure
hObject = histogram(indexedImage, 'normalization', 'probability');
grid on;
caption = sprintf('Area Fractions Of Each Color Class');
xlabel('Class Number', 'FontSize', fontSize);
ylabel('Area Fraction', 'FontSize', fontSize);
title(caption, 'FontSize', fontSize, 'Interpreter', 'None');
xticks(0 : numberOfColorClasses - 1);
